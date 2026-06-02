# PhysLit 论文中文 LaTeX 版

本目录是论文中文版的 LaTeX 源码。当前只包含引言一节（`\section{引言}`）作为模板验证用。后续章节按 `paper_draft.zh.md` 的内容逐节移植。

## 文件清单

- `main.tex` — 主文档，含 preamble、元数据、`\section{引言}`、`\bibliography{}`。
- `references.bib` — 引言所引 16 条文献（BibTeX 格式）。
- `figs/` — 图片目录（暂为空，后续章节加入）。

## 编译

中文支持依赖 `ctex` 包，必须用 **XeLaTeX**（或 LuaLaTeX）编译。`pdflatex` 不支持 UTF-8 中文。

标准编译流程（含 bib）：

```bash
cd latex_cn
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

`ctex` 用 `scheme=plain` 选项，不挂任何特定中文字体——在 macOS / Linux / Windows 上使用各自系统的默认中文字体（macOS 上一般是宋体或苹方）。若需指定字体（如全文用 PingFang SC），改 preamble：

```latex
\usepackage[UTF8, fontset=mac]{ctex}   % macOS 上自动用 PingFang SC + Heiti SC
\usepackage[UTF8, fontset=windows]{ctex}  % Windows 上自动用 SimSun + SimHei
```

## 中文引号

源码里直接打中文双引号（`"..."`）即可，`ctex` 会正确渲染为全角弯引号。若编译后出现引号方向不对，可改为显式的 `“...”` 字符或 LaTeX 的 ` ``...'' ` 形式。

## 排版约定（与 markdown draft 保持一致）

- 中文与数字、英文之间不留空格（`ctex` 自动处理粘连，源码内可以保留空格便于阅读）。
- 中文段落里的标点用全角。
- 数学符号（如 $F=mv$、$N=5$、百分号 `\%`）都用 LaTeX 数学环境或转义。
- 引用用 `\citep{key}`（圆括号格式）或 `\citet{key}`（行内式）。
