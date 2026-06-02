# PhysLit 论文中文 LaTeX 版

本目录是论文中文版的 LaTeX 源码。当前只包含引言一节（`\section{引言}`）作为模板验证用。后续章节按 `paper_draft.zh.md` 的内容逐节移植。

## 文件清单

- `main.tex` — 主文档，含 preamble、元数据、`\section{引言}`、`\bibliography{}`。
- `references.bib` — 引言所引 16 条文献（BibTeX 格式）。
- `figs/` — 图片目录（暂为空，后续章节加入）。

## 编译

中文支持依赖 `ctex` 包，必须用 **XeLaTeX**（或 LuaLaTeX）编译。`pdflatex` 不支持中文字体加载。

一键编译：

```bash
cd latex_cn
./build.sh
```

或手动跑四遍标准流程：

```bash
xelatex main.tex
bibtex main
xelatex main.tex
xelatex main.tex
```

或用 `latexmk` 一行搞定：

```bash
latexmk -xelatex main.tex
```

输出 `main.pdf` 即正文。

## 字体说明

当前用的是 **Fandol 字体**（`fontset=fandol`）。Fandol 是 TeX Live 自带的免费中文字体集，不依赖任何系统字体，跨 macOS / Linux / Windows 都能稳定编译。这是最不容易踩坑的选择。

如果想换成系统字体（视觉上更接近 macOS / Windows 原生中文），改 preamble 里 `\usepackage` 那一行：

```latex
% macOS：自动用 PingFang SC + Heiti SC（需要 macOS 13 以下的旧系统才稳）
\usepackage[UTF8, scheme=plain, fontset=mac]{ctex}

% Windows：自动用 SimSun + SimHei
\usepackage[UTF8, scheme=plain, fontset=windows]{ctex}

% Linux：用 Noto Sans CJK SC（需要先在系统装 noto-cjk）
\usepackage[UTF8, scheme=plain, fontset=ubuntu]{ctex}
```

**已知坑**：macOS 13 及以上版本 Apple 移除了部分老中文字体（Heiti SC、STSong 等），`fontset=mac` 在新系统上可能直接报 `CTeX fontset 'mac' is unavailable in current mode`。如果遇到这条错误，退回 `fontset=fandol` 即可。

## 中文引号

源码里直接打中文双引号（`"..."`）即可，`ctex` 会正确渲染为全角弯引号。若编译后出现引号方向不对，可改为显式的 `“...”` 字符或 LaTeX 的 ` ``...'' ` 形式。

## 排版约定（与 markdown draft 保持一致）

- 中文与数字、英文之间不留空格（`ctex` 自动处理粘连，源码内可以保留空格便于阅读）。
- 中文段落里的标点用全角。
- 数学符号（如 $F=mv$、$N=5$、百分号 `\%`）都用 LaTeX 数学环境或转义。
- 引用用 `\citep{key}`（圆括号格式）或 `\citet{key}`（行内式）。
