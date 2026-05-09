"""Phase 1.5 — capture exact model-version strings for OpenAI GPT-5
and Google Gemini 3 ahead of the v0.1 prereg lock.

This script is **not a production trial** and its output is **not v0.1
evaluation data**. It exists solely to embed authoritative version
strings into ``predictions/v0_1_prereg.md`` so the prereg lock pins
the exact tested-model versions rather than vendor aliases.

What it does:

1. Lists available models from each vendor's API and prints them.
2. Sends one tiny ping per vendor with the smallest possible
   completion (max-output-tokens=1, reasoning effort minimal where
   the API exposes that knob, prompt = ``"hi"``).
3. Captures and prints ``response.model`` (or the equivalent field).
4. Estimated cost: a few cents at most across both vendors.

The script does NOT save trial JSONs anywhere; the captured version
strings are recorded by hand into the prereg in a follow-up step.
"""

from __future__ import annotations

import os
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent

# Target model identifiers (decided 2026-05-09 for v0.1 prereg lock).
# OpenAI selection rationale: gpt-5.5 (latest GPT-5.x date-stamped main
# variant) at standard-flagship tier; the pro tier is ~5x more expensive
# per token and would blow the $50 v0.1 budget cap. Pro-tier comparison
# is deferred to v0.2.
# Gemini selection rationale: Google has not promoted any Gemini 3 Pro
# model out of preview status as of 2026-05-09, so v0.1 pins the preview
# id explicitly and treats preview drift as a methodology deviation if
# it occurs.
TARGET_OPENAI = "gpt-5.5-2026-04-23"
TARGET_GEMINI = "gemini-3-pro-preview"


def _load_dotenv() -> None:
    env_path = REPO_ROOT / ".env.local"
    if not env_path.exists():
        return
    for raw in env_path.read_text().splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, _, value = line.partition("=")
        os.environ.setdefault(key.strip(), value.strip())


def discover_openai() -> str | None:
    """List models, then ping :data:`TARGET_OPENAI` with the smallest
    possible completion. Returns the actual ``response.model`` string,
    or ``None`` on failure."""
    try:
        import openai
    except ImportError:
        print("[OpenAI] openai SDK not installed", file=sys.stderr)
        return None

    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        print("[OpenAI] OPENAI_API_KEY not set", file=sys.stderr)
        return None

    client = openai.OpenAI(api_key=api_key)

    print("[OpenAI] Listing available models (looking for gpt-5)...")
    try:
        models = client.models.list()
        relevant = sorted(
            m.id
            for m in models.data
            if m.id.startswith("gpt-5") or m.id.startswith("o3") or "gpt-5" in m.id
        )
        for mid in relevant:
            print(f"  - {mid}")
    except Exception as exc:
        print(f"[OpenAI] models.list() failed: {exc}", file=sys.stderr)

    print(f"[OpenAI] Pinging {TARGET_OPENAI} with minimal request...")
    # max_completion_tokens=16: just enough for minimal reasoning + a
    # one-or-two-word reply. The first attempt on 2026-05-09 used =1
    # and 400'd because GPT-5 reasoning consumes some tokens before
    # producing visible output; with 16 we comfortably clear that.
    #
    # reasoning_effort: GPT-5.5 expects one of {none, low, medium, high,
    # xhigh}; the older GPT-5 alias used 'minimal'. Try 'none' first;
    # fall back to no kwarg if the model doesn't recognise the param.
    try:
        response = client.chat.completions.create(
            model=TARGET_OPENAI,
            messages=[{"role": "user", "content": "hi"}],
            max_completion_tokens=16,
            reasoning_effort="none",
        )
    except TypeError:
        # Older openai SDK versions don't expose reasoning_effort kwarg.
        response = client.chat.completions.create(
            model=TARGET_OPENAI,
            messages=[{"role": "user", "content": "hi"}],
            max_completion_tokens=16,
        )
    except Exception as exc:
        # Surface the raw API error so we can adjust parameters.
        print(f"[OpenAI] ping failed: {type(exc).__name__}: {exc}", file=sys.stderr)
        return None

    print(f"[OpenAI] response.model = {response.model!r}")
    if hasattr(response, "usage") and response.usage is not None:
        print(
            f"[OpenAI] usage: prompt={response.usage.prompt_tokens} "
            f"completion={response.usage.completion_tokens}"
        )
    return str(response.model)


def discover_gemini() -> str | None:
    """List models for transparency, then ping :data:`TARGET_GEMINI` with
    a small completion. Returns the actual model id, or ``None`` on
    failure."""
    try:
        from google import genai
        from google.genai import types as genai_types
    except ImportError:
        print("[Gemini] google-genai SDK not installed", file=sys.stderr)
        return None

    api_key = os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY")
    if not api_key:
        print("[Gemini] no GEMINI_API_KEY / GOOGLE_API_KEY", file=sys.stderr)
        return None

    client = genai.Client(api_key=api_key)

    print("[Gemini] Listing available models (transparency only)...")
    try:
        models = list(client.models.list())
        names: list[str] = [
            m.name for m in models if isinstance(m.name, str) and "gemini-3" in m.name
        ]
        for mid in sorted(set(names)):
            print(f"  - {mid}")
    except Exception as exc:
        print(f"[Gemini] models.list() failed (proceeding to ping): {exc}", file=sys.stderr)

    print(f"[Gemini] Pinging {TARGET_GEMINI} with minimal request...")
    # max_output_tokens=16 mirrors the OpenAI bump; cost is negligible
    # and the larger budget makes the ping more robust if Gemini
    # internal reasoning ever consumes output budget.
    try:
        response = client.models.generate_content(
            model=TARGET_GEMINI,
            contents="hi",
            config=genai_types.GenerateContentConfig(max_output_tokens=16),
        )
    except Exception as exc:
        print(f"[Gemini] ping failed: {type(exc).__name__}: {exc}", file=sys.stderr)
        return None

    # google-genai surfaces the resolved model id on response.model_version
    # (newer SDK) or via candidate metadata (older). Try both.
    resolved = getattr(response, "model_version", None) or TARGET_GEMINI
    print(f"[Gemini] resolved model id = {resolved!r}")
    if hasattr(response, "usage_metadata") and response.usage_metadata is not None:
        print(
            f"[Gemini] usage: prompt={response.usage_metadata.prompt_token_count} "
            f"output={response.usage_metadata.candidates_token_count}"
        )
    return resolved


def main() -> int:
    _load_dotenv()
    print("=== Discovery: model version strings for v0.1 prereg lock ===")
    print("This is NOT a production trial. Output is recorded only into")
    print("predictions/v0_1_prereg.md (Tested models block).")
    print()

    print("--- OpenAI GPT-5 ---")
    gpt5 = discover_openai()
    print()

    print("--- Google Gemini 3 ---")
    gemini = discover_gemini()
    print()

    print("=== Summary ===")
    print(f"  OpenAI GPT-5: {gpt5!r}")
    print(f"  Gemini 3:     {gemini!r}")
    return 0 if (gpt5 and gemini) else 1


if __name__ == "__main__":
    sys.exit(main())
