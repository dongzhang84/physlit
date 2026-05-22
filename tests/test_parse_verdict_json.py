"""Tests for ``parse_verdict_json`` — the judge-response parser.

The 03_decay production run surfaced a failure mode in which Claude
judge "thinks out loud" by emitting a sequence of JSON drafts
separated by self-correction prose, converging on a final verdict.
The parser must return the final dict, not crash on the multi-object
output.
"""

from __future__ import annotations

from physlit.judges import parse_verdict_json


def test_single_json_object() -> None:
    raw = '{"verdict": "PASS", "evidence": null}'
    parsed, err = parse_verdict_json(raw)
    assert err is None
    assert parsed == {"verdict": "PASS", "evidence": null_value()}


def null_value() -> None:
    """Helper because the JSON literal ``null`` becomes Python ``None``."""
    return None


def test_json_object_with_leading_preamble() -> None:
    raw = 'Sure, here is my verdict:\n{"verdict": "FAIL"}'
    parsed, err = parse_verdict_json(raw)
    assert err is None
    assert parsed == {"verdict": "FAIL"}


def test_two_json_objects_returns_last() -> None:
    """The headline regression case: Claude judge emits a draft, then
    prose, then a final verdict. The parser returns the final dict."""
    raw = (
        '{"verdict": "FAIL", "reasoning": "first draft"}\n'
        "Wait, I need to reconsider.\n"
        '{"verdict": "PASS", "reasoning": "final answer"}'
    )
    parsed, err = parse_verdict_json(raw)
    assert err is None
    assert parsed is not None
    assert parsed["verdict"] == "PASS"


def test_three_json_objects_returns_last() -> None:
    raw = (
        '{"verdict": "PASS"}\n'
        "Hmm wait.\n"
        '{"verdict": "FAIL"}\n'
        "Actually rethinking.\n"
        '{"verdict": "PASS"}'
    )
    parsed, err = parse_verdict_json(raw)
    assert err is None
    assert parsed is not None
    assert parsed["verdict"] == "PASS"


def test_no_json_object() -> None:
    raw = "I am unable to provide a verdict."
    parsed, err = parse_verdict_json(raw)
    assert parsed is None
    assert err is not None and "no JSON" in err


def test_malformed_json_is_skipped_but_later_valid_returned() -> None:
    """A broken JSON-like blob followed by a real one should yield
    the real one."""
    raw = '{this is not valid json}\n{"verdict": "PASS", "evidence": null}'
    parsed, err = parse_verdict_json(raw)
    assert err is None
    assert parsed is not None
    assert parsed["verdict"] == "PASS"


def test_nested_json_in_string_value() -> None:
    """Top-level extraction must not be confused by ``{`` inside a
    string literal of a value."""
    raw = '{"verdict": "FAIL", "evidence": "the model said {foo: bar}"}'
    parsed, err = parse_verdict_json(raw)
    assert err is None
    assert parsed is not None
    assert "foo: bar" in parsed["evidence"]


def test_top_level_array_is_not_a_dict() -> None:
    """A bare JSON array is not an acceptable verdict shape."""
    raw = "[1, 2, 3]"
    parsed, _err = parse_verdict_json(raw)
    assert parsed is None
