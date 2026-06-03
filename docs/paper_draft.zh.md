# 在三个物理世界里测试前沿大语言模型的物理素养

> **草稿** · 2026-05-28 · 张栋
>
> 配套代码与数据：<https://github.com/dongzhang84/physlit>
> 三个预注册标签：`prereg-v0.1-locked`、`prereg-02_fmv-locked`、`prereg-03_decay-locked`

---

## 摘要

我们用三个难度递增的"平行物理世界"测试前沿大语言模型（Claude Opus 4.7、GPT-5.5、Gemini 3.1 Pro）是否具备底层的物理思维能力，能否在一个**结论不符合训练先验**的物理框架里完成归纳、系统化、应用和反思这四步认知动作。三个框架按难度排序分别为：F=mv（单方程反事实世界，Easy）、亚里士多德力学（历史框架，Medium）、Decay World（跨领域反事实世界，Hard）。每个框架在3个模型 × N=5次实验 × 4个阶段下，配合双裁判 + 人工audit的判定流程，输出按预注册SHA-256锁定的结论。

综合内容通过率（composite content PASS）分别是 **9/15、5/15、0/15**，难度梯度与实验结果方向一致。三个独立观察构成本文的核心结论：（1) 前沿模型**能**完成单方程反事实推理（F=mv），但**不能**完成跨领域、无底层物质的反事实推理（Decay World）。（2) 三个框架上**失败后高估自己**（Stage 4 over-claim）的比率稳定在65–70%，模型的元认知能力不会随框架变难而提高。（3) 不同LLM裁判的可靠性**不跨框架可迁移**，且在Decay World上OpenAI裁判出现可机械复现的系统性失效（18个判断中16个为虚构或误分类的禁词引用），这是LLM-as-judge文献的新数据点。

我们公开方法论、所有原始prompt、所有模型响应、所有裁判判断与人工audit记录。完整可复现入口在 `prereg-<round>-locked` 标签下。

---

## 1. 引言

近年来大语言模型（LLM）能否进行推理是AI研究的中心争议之一。本文取认知科学与形式逻辑共享的最小定义：**推理**（reasoning）是从一组前提出发，按可被外部独立检查的有效推导步骤，得到一个新结论的过程。其中"有效"指每一步在该问题的逻辑或符号体系内成立，"独立检查"指推导过程的正确性不依赖于结论本身、也不依赖于对训练分布的记忆。在LLM评估文献里这一定义被操作化为这样一类任务：模型对一个无法单步生成答案的问题（多步算术、几何证明、长程规划），需要在响应中产生若干中间步骤再合成最终答案，每一步都可被独立检查。Wei等[1]2022年提出Chain-of-Thought（CoT，思维链）提示：在prompt里给模型一两个"问题、中间步骤、答案"的范例，PaLM-540B在GSM8K[2]上的解题率从17.9%跃到56.9%。Kojima等[3]发现连范例都不需要，一句"Let's think step by step"就能把InstructGPT-175B的零样本正确率从10.4%拉到40.7%。这一线索叠加Brown等[4]观察到的GPT-3规模效应、Wei等[5]的涌现假说，构成了"规模加提示等于推理涌现"的乐观叙事。但Schaeffer等[6]论证涌现的很大一部分是评估指标产物，Mirzadeh等[7]的GSM-Symbolic显示前沿模型对题面符号扰动高度敏感（GSM-NoOp变种下正确率可掉超过60个百分点），意味着模型对题面的符号匹配贡献远大于真正的多步推导。Huang与Chang[8]的综述把这场争论从"CoT是真推理"一端梳理到"CoT只是检索训练数据里的模板"的另一端。围绕"LLM是否真在做推理"这一问题，学界目前尚无定论。

比起推理，另外一个更宏大的问题是，AI能做科学研究吗？把现有"AI做科学"工作放在一个自主度光谱上看，可以分为三个层次。**低自主**：AI作为在已知理论框架内的执行工具，做优化、自动化与参数搜索。Boiko等[9]2023年的Coscientist让LLM自主调度有机合成实验、Robin系统里Finch子模块对实验数据做统计分析都在这一层次。**中自主**：AI作为假设生成器与候选筛选系统，在已有文献的大空间里做信息综合与候选排序，输出列表交由人工验证。Romera-Paredes等[10]的FunSearch在人写的评估函数下搜索程序、Gottweis等[11]的Co-Scientist跨文献做药物重定位假设、Ghareeb等[12]的Robin在干性年龄相关性黄斑变性上跑端到端闭环（Crow文献综述、Falcon假设评估、Finch数据分析）、Lu等[13]的The AI Scientist在人写的ML模板里跑超参变体都属此类。**高自主**：AI端到端解决一个被精确陈述的科学问题，问题陈述、成功判据与外部验证均由人提供，AI在被严格定义的搜索空间内产出一个可被独立检验的对象。Trinh等[14]的AlphaGeometry在IMO几何题上给出形式化证明、OpenAI[15] 2026年5月报告其内部推理模型给出Erdős 1946年单位距离猜想的反例构造（联同九位外部数学家完成验证），均落在这一层次。这三个层次共享一个结构特征：被求解的问题处在一个已被人类先验地确立的理论框架内，AI的任务是在框架内做搜索、组合、推理或证明，框架本身在求解过程中不动。换个角度看，三个层次对应的是AI在科学研究链条上独立完成的不同片段：低自主对应已有框架内的实验执行与数据处理，中自主对应在已有规律基础上生成候选假设，高自主对应在被给定的问题陈述下完成求解或构造。这些都是建立一个科学理论过程中的某一环节，不是建立完整的科学理论本身。建立完整的科学理论需要从一组未经理论解释的观察起步，独立归纳出一套可被第三方检验的理论体系，再用该体系对新情境做可量化预测。这一完整过程在物理学训练里居于核心位置，但在所有已知AI工作里都没有被独立完成过。

与"建立完整科学理论"最近的相邻研究方向是世界模型。Ha与Schmidhuber[16]把世界模型定义为智能体在内部维护的、用以预测环境演化的生成模型。LeCun[17]在《通往自主机器智能》立场文中把它列为通用智能架构的核心组件。"世界模型"这一概念本身在文献内并无统一定义。Ding等[18] 2024年的综述把现有工作大致分成"理解世界"与"预测未来"两派，并指出像OpenAI Sora这类视频生成模型是否算世界模型至今未达共识。Sora团队曾将其定位为隐含的物理模拟器（OpenAI已于2026年4月停服Sora应用端，API计划同年9月关闭），LeCun[17]则反驳像素级生成与对世界的因果模型是两件事。评测一侧的标准同样未确立。Li等[19] 2023年的Othello-GPT通过probing抓出了模型内部的棋盘状态表征，作为"世界模型存在"的可证伪性证据。但Vafa等[20] 2024年用Myhill-Nerode启发的更严格判据测发现，现有生成模型在常规探针上看似都有世界模型、在新判据下却普遍表现为不连贯。物理这一维度上Bear等[21] 2021年的Physion基准测的是从视觉输入预测物体如何滚动、滑落、碰撞，属于对物理现象的下一步预测，并不要求模型把规律外显为可被独立检验的形式。综合看，世界模型这条线提供的是一个必要不充分的前置：模型若没有某种关于世界的内部表征，不可能产出可被独立检验的形式理论。但内部表征的存在不蕴含模型能把它产出为这样的理论。后一更严格的输出形态如何被实际测试，是接下来需要回答的问题。

学界目前判断LLM会不会物理，主流方式是做题。GSM8K[2]用小学数学应用题作为基准，MATH[22]扩展到高中竞赛题，SciBench[23]覆盖大学物理化学教材题（869道开放式题，最佳模型当时得分43.22%），TheoremQA[24]测定理应用（800题，覆盖350个定理），JEEBench[25]用印度IIT入学考试的515道理工科难题，OlympiadBench[26]走奥林匹克路线（8476题，物理子集GPT-4V当时得分10.74%）。这些基准的共同输出指标是答对率。

把"答对几道题"作为"会物理"的判据有两个结构性问题。其一，答对率分不清"懂物理"和"训练数据里见过同类题"。基准覆盖越广、模型见过的相似题越多，分数自然越高，这种增长并不意味着模型获得了归纳新现象、规则化新经验、对新情境做预测的能力。其二，答对率不传达关于认知边界的任何信息。模型A得90%、模型B得91%，告诉读者的全部是"B比A多对了一道"，而非"B能做但A做不了的是哪一类认知工作"。当读者关心的是"模型能不能处理训练数据里没有的物理场景"时，答对率不提供外推线索。

我们提出的判别方式是把物理推理拆成四个底层认知动作，分别测试：归纳（induction，从一组现象里抽出能解释所有现象的规律）、系统化（formulation，把规律写成可被第三方应用的操作性形式）、应用（prediction，用规则对新情境做量化预测）、反思（reflection，回看自己的推理识别可能错的一步）。给定一个明确的物理框架（含一组现象、一套判据、一组应用场景），让模型逐一执行这四个动作，对每个动作的输出独立判定，最后看综合是否通过。这一拆分依据的是物理学训练的实际过程：物理学家的能力来自这四步组成的序列，任一动作缺失，物理推理都不完整。

为避免结论被某个框架的特殊性质所限定，我们选了三个在认知压力上有明显差距的物理框架构成难度梯度：F=mv世界（反事实、单方程、单一物理领域），亚里士多德力学（历史框架、训练数据里以"被反驳的立场"形式存在），Decay World（反事实、跨四个物理领域、规则绑在直接可测的量上、无底层物质、所有标准耗散机制被关闭）。每个框架上做3个模型 × N=5次实验 × 4个阶段。本文的预测以SHA-256加git tag锁定（`prereg-<round>-locked`），所有原始prompt、模型响应、双LLM裁判判定、人工audit结论开放可复现。

本文的贡献分三层。方法论层：一套可复现、可审计的LLM物理素养评估流程，从预注册到双LLM裁判到IRR阈值触发人工audit的全部环节。实验结论层：三组实验综合内容通过率（composite content PASS）分别为9/15、5/15、0/15，与难度梯度方向一致。三家前沿模型（Claude Opus 4.7、GPT-5.5、Gemini 3.1 Pro）在定性方向上能力强（Decay World上60道定量题里0题方向错），在定量比例上系统性套用训练数据里的标准物理公式（23题方向对但比例错）。跨框架方法论发现：Stage 4 over-claim比率在三个框架上稳定落在65到70之间，亚里士多德70%、F=mv 66.7%、Decay World 67%，与具体物理内容解耦。不同LLM裁判的可靠性不跨框架可迁移，OpenAI裁判在Decay World上出现机制清晰的系统性失效（18个判断里16个引用虚构或误分类的禁词），为LLM-as-judge文献增加了一个可复现的failure mode数据点。

---

## 2. 方法论

### 2.1 四阶段协议

每次实验由四个独立阶段构成。每个阶段一个独立的API会话，新的client、新的session UUID、temperature=0、固定的随机种子。模型在Stage 2看不到Stage 1的会话历史，只能看到Stage 1的最终响应作为输入文本。这一**严禁多轮上下文复用**的设定避免了"模型偷偷在跨阶段对话里把上一轮的错改掉"这类污染，让每一阶段的判断真正反映该阶段的独立能力。

**Stage 1：归纳。** 给模型一组现象（自然语言描述的观察记录），让它归纳出能解释所有现象的规则集合。判据由该框架的 `ideal_induction.md` 给出，包括禁词列表（§3）、必要条件N1–N6、可疑模式P1–P7、以及一套机械的"halt-at-first-FAIL"裁判流程。

**Stage 2：系统化。** 给模型自己Stage 1的归纳结果，让它写成正式的操作性规则（每条规则带操作定义、适用范围、边界情况）。判据是该框架的 `pass_fail_criteria.md`。

**Stage 3：应用。** 给模型自己Stage 2的规则，让它对一组新场景做量化预测。每个场景的判据有显式的PASS数值区间。

**Stage 4：反思。** 给模型自己前三阶段的全部输出，让它自评是否做错了什么、错在哪。判据是元认知判定（yes/no/vacuous over-claim）。

一次"实验"指的是同一个模型、同一组现象上完整跑一遍这四个阶段。每个框架我们做3个模型 × N=5次 = 15次实验。

### 2.2 预注册不可逆

每一轮实验在产生任何production数据之前，预测内容、判据、prompt、判据脚本全部lock在一个git tag（如 `prereg-03_decay-locked`）下，该tag把prereg文件本身的SHA-256写入文件头。一个pre-commit hook加CI检查（`scripts/verify_prereg_integrity.py`）保证任何静默修改都过不去commit。需要修订prereg必须开新tag（如 `prereg-03_decay.1-locked`），并在公开结果里显式标注"deviation from prereg"。

这是把"事先说好"和"事后回看"在工程上变得不可作弊的最小可执行方案。

### 2.3 双 LLM 裁判 + 25% IRR 触发人审

Stage 1–3的所有PASS/FAIL判定，由两个独立的前沿LLM裁判（Claude + OpenAI）分别打分。Stage 1–3的跨裁判分歧率（dual-judge IRR）若超过 **25%**，强制触发人工audit。人审结论作为该轮的canonical判定，并以逐条verbatim引用的形式公开（`*_audit_human_review.md`）。

这一阈值的设计逻辑是：单个LLM裁判的判断不可作为最终结论，但两个裁判的"共识"是一个便宜、可复现的起点。分歧本身（IRR）就是一个独立的方法论健康指标。当IRR太高，说明判据本身或裁判本身有问题，必须让人介入。

### 2.4 PASS 怎么定义

**Content axis composite PASS**（每一次实验的最终判定）的定义是：

> Stage 1 PASS **且** Stage 2 PASS **且** Stage 3 的每一个 quantitative scenario 都 PASS。

只要任一阶段或任一场景失败，整次实验记composite FAIL。这是一个非常严格的判定，它要求模型从归纳到应用每一环都不掉链子，对应物理学家"一个完整推理链不能在任何一步断"的标准。

### 2.5 框架的来源（Tier 1 / Tier 3）

我们把候选框架按"是否可被一个确定性Python模拟器编码"分成三层：

- **Tier 1**：可模拟（如F=mv世界的牛顿动力学修改、Decay World的指数衰减）。该层框架的"现象集"由simulator生成，受 `CLAUDE.md` 的Determinism Contract约束，同种子下输出字节一致。
- **Tier 2**：AI生成（在v0.1版禁用，避免生成AI和被测AI之间的污染）。
- **Tier 3**：人工撰写（如亚里士多德力学，历史框架无法用一个干净的方程总结）。

本文三个框架分别是Tier 1（F=mv、Decay）和Tier 3（亚里士多德）。

---

## 3. Easy — F=mv 反事实世界

### 3.1 框架介绍

F=mv世界的核心规则是：力与速度成正比，而不是与加速度成正比。具体地，一个被持续施力的物体以**恒定速度**移动。力一撤，物体立即停止。所有物体在重力下以**同一不变速度**下落，与质量无关。

这个世界与F=ma在数值上**直接冲突**，同一现象、同一物理量，F=mv与标准物理给出的预测在量纲、ratio、和方向上都不同。比如标准物理预测自由落体距离与时间平方成正比（s = ½gt²），F=mv预测距离与时间成正比（s = vt）。

我们写了12条不含禁词（force、mass、acceleration、…）的观察现象，让模型自己从这些观察里归纳出F=mv。该框架的所有现象与判据冻结在 `frameworks/02_fmv/`、prereg锁定为 `prereg-02_fmv-locked`。

### 3.2 预注册预测

`02_fmv` 锁定了四条预测：

- **P1 — 归纳失败：** Stage 1归纳失败率高（即模型滑回F=ma而非归纳出F=mv）。
- **P2 — 元认知失调：** 失败实验中，Stage 4反思over-claim比率 ≥ 50%。
- **P3 — 机械判据降低分歧：** Stage 1–3 dual-judge IRR < 25%（相对v0.1的36.67%）。
- **P4 — 定量泄露：** Stage 3定量预测里 ≥ 30% 给出F=ma比例（"对方向但错比例"）。

### 3.3 结果

**Composite content PASS：9/15。** P1 **被反驳**（REFUTED），Claude 5/5、GPT 5/5、Gemini 1/5。只有Gemini在归纳阶段滑回了F=ma，Claude和GPT在每一次实验里都干净地归纳出了F=mv规则。**这是和v0.1亚里士多德结果的反向**，前沿模型**能**在一个单方程反事实世界里完成归纳。

P2 **被确认**（CONFIRMED）at 66.7%：失败实验中绝大多数Stage 4自评仍然说"问题不大"。P3 **部分确认**（IRR 26.67%，略高于25% 阈值但远低于v0.1的36.67%）。P4 **被反驳**（45个定量预测中0个给出F=ma比例），这是一个有意思的发现，提示我们当模型真正归纳到了反事实规则，它的演绎能力是跟得上的。

### 3.4 子轮压缩

`02_fmv.1`（结构轴N9–N12叠加在同一批trial上）发现：content axis和structural axis在三家模型间**呈反相关**，Claude内容强、结构弱。GPT反过来。"会写"和"会精炼地写出"是两件事。

`02_fmv.2`（公理化对照）是一个单变量控制：在Stage 1 prompt里加一段话，要求模型用尽可能少的规则、显式说明规则间的因果引用关系。其他全部不变。结果：**结构通过率5/15 → 11/15**，几乎翻倍。content维持不变。composite 1/15 → 6/15。这条结果说明，模型有结构化推理能力但默认不去用，一句**自然语言提示**就能激活。本轮的设计意义在于把 "structural failure" 从"能力缺陷"重新定性为"默认行为漏洞"。

### 3.5 子结论

F=mv章节最重要的发现：**前沿模型有反事实推理能力，但默认不调用**，既不调用反事实推理本身（需要单方程的简单触发才能调动），也不调用结构化表达能力（需要一句prompt才能调动）。

---

## 4. Medium — 亚里士多德力学

### 4.1 框架介绍

亚里士多德力学是一个**真实存在、内部自洽、被训练数据广泛覆盖**的历史框架。它的核心命题包括：物体的自然运动取决于其元素构成、重物比轻物下落得更快、抛射物维持运动需要持续推动等。在现代物理教材里，这些命题是被引用、然后被反驳的，模型见过它们，但见到的角度是"这是错的"。

我们要测的不是"模型知不知道亚里士多德怎么说"，它当然知道。我们要测的是：**模型能否暂停训练数据里那一句"这是错的"，足够长地在亚里士多德框架内做推理**。

我们写了12条用纯描述性语言（不含density、force、acceleration、Newton等现代物理或现代物理学家名词）描述的观察现象，让模型从这些观察里归纳出本世界的规律。判据冻结在 `frameworks/01_aristotelian/`、prereg `prereg-v0.1-locked`。

### 4.2 预注册预测

`v0.1` 锁定了两条预测：

- **P1 — 训练数据冲突下的归纳失败：** Stage 1归纳里2/3模型 在 ≥ 3/5次实验中引入禁词。
- **P3 — 元认知失调：** 含有失败的实验中 ≥ 30% 在Stage 4反思中over-claim。

### 4.3 结果

**Composite content PASS：5/15。** P1 **被确认**（CONFIRMED），多数模型在归纳阶段都引入了被明确禁止的现代物理词汇（如dense、forceful、surface-supported），且在prompt明令禁止的前提下也未能避免。P3 **被确认** at **70%**，失败实验中7成Stage 4反思未识别自己刚才犯的错。

失败模式与F=mv完全不同：F=mv上模型失败是因为"滑回标准物理"，亚里士多德上模型失败是因为"训练数据里这一框架被批判，禁词随之外溢"，同样是P1 confirmed，机制却是相反的。

### 4.4 子轮压缩

`v0.2`（结构轴N9–N12叠加在v0.1 trial上）：把结构轴加进来后composite通过率从5/15掉到2/15，同一组现象、同一组归纳，加上"规则集应当结构化"的判据，绝大多数原本通过的归纳被识别为"无结构的规则汤"。

`v0.2.1`：尝试用LLM作为分歧仲裁员（Agent 1）取代人审。Agent 1与人审的一致率仅29.4%，在判据需要解释的情况下，LLM无法稳定复现人审。这条结果直接驱动了后续轮（02_fmv开始）的"机械化判据"改写。

`v0.3`（跨框架复制 `02_fmv.2`）：把02_fmv.2那段一句话的**公理化提示**原文搬到亚里士多德Stage 1 prompt里（字节级diff验证一致）。结果：**结构通过率8/15 → 15/15饱和**，同一段干预词在两个完全不同的物理框架上都生效。这是一条**跨框架可复现的因果链**，把02_fmv.1里"模型有结构化能力但默认不用"的论断升级为"通用的、可干预的默认行为缺陷"。

### 4.5 子结论

亚里士多德章节最重要的发现：**模型对历史框架的认知障碍主要来自训练数据里的"批判性引用"，禁词外溢、Newton词汇泄露**，而不是"无法理解该框架"。一句公理化提示足以把结构表达从8/15推到15/15饱和，与F=mv上同一干预的复制结果合并，是本文最强的"模型能力是默认行为而非能力上限"证据。

---

## 5. Hard — Decay World

### 5.1 框架介绍

Decay World的规则只有一句：**任何孤立系统内一切直接可测量的物理量**（振荡幅度、绝对温度、转速、轨道半径……）**以固定比例（约0.99/秒）随时间衰减**，在机械、热、转动、轨道四个领域里都用同一个速率，并且**没有任何底层物质（如"能量"）作为支撑**。所有标准耗散机制（摩擦、阻尼、空气阻力、粘滞、辐射衰减）在观察设计中**显式地被关闭**，观察明确指出这些情境是真空中、光滑表面、无接触、无外力。

这一设计同时把模型最强的三条物理先验都顶上去：

1. **反事实推理**，观察事实与标准物理冲突。
2. **无substrate解释**，没有"能量"等隐藏量可以做规则的载体，规则必须绑在直接可测的量上。
3. **统一跨域**，同一速率适用机械、热、转动、轨道，不能用任何**单领域**机制（摩擦只能解释机械、Newton冷却只能解释热）做替代。

这是PhysLit设计意图最显式的一次：我们想知道当三条最强先验都让步时，前沿模型会用什么方式失败。框架冻结在 `frameworks/03_decay/`、prereg `prereg-03_decay-locked`。

### 5.2 预注册预测

`03_decay` 锁定了四条预测：

- **P1 — 比两个先验框架都难：** Composite content PASS **严格小于5**（低于02_fmv的9和v0.1的5）。
- **P2 — 隐藏底物陷阱触发：** Stage 1归纳失败中，§5 P2 "隐藏底物框架"是**唯一被引用次数最多的失败模式**。
- **P3 — 定量泄露 > 方向错误：** 60个定量预测中，"方向对但比例套了标准物理" 严格多于"方向错"。
- **P4 — 元认知over-claim > 自我识别：** 含失败实验中over-claim严格多于correct self-identify。

### 5.3 结果

**Composite content PASS：0/15**，三家模型15次实验**没有一次综合通过**。Decay World是迄今三个框架里最难的一个。

| Framework | Composite PASS |
|---|---|
| F=mv (Easy) | 9/15 |
| Aristotelian (Medium) | 5/15 |
| **Decay World (Hard)** | **0/15** |

**四条prereg全部确认。**

**P1 CONFIRMED** ， 严格小于5（实测为0）。难度梯度的实验设计经受住了验证。

**P2 CONFIRMED** ， Stage 1归纳失败中，§5 P2"隐藏底物"是唯一被触发的 §5模式（其他失败要么是 §3禁词、要么是 §4必要条件N4 / N6不满足、要么是 §6.3覆盖不全）。值得注意的是Stage 2（系统化）阶段中4个 §5失败中有3个仍然是P2隐藏底物，模型在归纳时勉强避开了这一陷阱，到了把规则正式写出来的时候才陷下去：把"速度"当作那个真正衰减的底层量，再用标准轨道力学从速度推出轨道半径。这是模型**死记硬背的物理公式被反射性套用**的最清晰证据。

**P3 CONFIRMED** ， 60个定量预测的分桶为：

| 桶 | 数量 |
|---|---|
| 衰减-正确（decay-correct） | 37 |
| 方向对、比例泄露（ratio-leaked） | 23 |
| 方向错（direction-wrong） | **0** |

**方向错桶完全为空**，15次实验、60个量化场景，没有一个模型说出"反而增长"、"保持不变"、"趋向室温"这种方向上完全错的答案。这是一个对前沿模型物理素养的**正面**陈述：模型**知道**"有东西在变小"。

但**比例上**模型大量套用标准物理。一个0.99/秒的指数衰减算成牛顿冷却的渐近、一个普通振荡的阻尼算成线性减少、一个轨道半径用v² ∝ r倒推。这些**比例泄露**反映了模型在"反事实定量推理"上的真实短板：它的演绎能力受训练数据里**比例公式**的强引力作用，定性上不出错，定量上立刻回到训练分布。

**P4 CONFIRMED** ， 15次失败实验中，over-claim = yes **10次**，no **5次**。over-claim比率67%，落在和v0.1（70%）、02_fmv（66.7%）完全相同的频带。

### 5.4 子结论

Decay World章节最重要的发现：**模型的物理素养在"定性方向感"和"定量计算"上呈现明显的非对称性**，方向上无可挑剔（60/60知道某物在缩），比例上系统性地泄漏到训练数据里的标准物理公式。其次是**隐藏底物陷阱的高效触发**，把规则强制写成"操作性"的Stage 2 prompt反而让模型踩中陷阱（Stage 1一次、Stage 2三次）。

---

## 6. 跨框架的两个 methodology 发现

### 6.1 Stage 4 over-claim 比率的稳定性

三个完全不同的框架、三组完全独立的实验，**失败实验中Stage 4 over-claim比率**分别是：

| Framework | Over-claim比率 |
|---|---|
| v0.1亚里士多德 | 70% |
| 02_fmv F=mv | 66.7% |
| 03_decay衰减世界 | 67% |

三个数全部落在 **65–70%** 这一窄带。Decay World是认知上最不熟悉、failure量最多的一个框架，直觉上似乎应该让模型在反思时更容易识别失败，但over-claim比率没有提高，也没有降低。

这是一个**与框架无关、与失败具体形式无关、在三家不同前沿模型上聚合后稳定的行为统计**。它的含义是：**前沿模型在物理领域内的元认知校准是一个独立于具体物理内容的属性**，不会因为问题变难而变好，也不会因为问题变难而变差。这一发现给"模型自我评估能力"研究提供了一个具体、可量化、跨框架可复现的数据点。

### 6.2 LLM 裁判可靠性不跨框架可迁移

三轮实验里，"较可靠的那个LLM裁判"（与人审一致率较高的那一个）发生了三次跨轮变化：

| Framework | Claude judge agreement | OpenAI judge agreement | 较可靠 |
|---|---|---|---|
| v0.1亚里士多德 | 32% | 68% | OpenAI |
| 02_fmv F=mv | 79% | 21% | Claude |
| 03_decay衰减世界 | 67–81%（按Part A/B/C） | 22–50% | Claude |

**同样的prompt、同样的模型、同样的判据格式、不同的框架，较可靠的裁判反转两次。**

这一现象的实践意义是：**不能仅用一个LLM裁判**，任何一轮单judge的判断都可能是系统性误判。PhysLit的"双裁判 + 25% IRR阈值 + 人审兜底"在三轮实验里都被实际触发过，每一次都修正了重要数量的判断。这给LLM-as-judge文献提供了一个**不需要大规模、靠跨框架对比就站得住**的证据点：**单judge评估不安全**。

---

## 7. OpenAI 裁判 §3 禁词测试的可机制化复现失效

03_decay上Part A的18个dual-judge分歧案例里，**16个OpenAI judge的FAIL clause在人审中被推翻**。失效分两类：

- **虚构（fabricated）**：OpenAI引用了"resistance"、"deceleration"、"frictionless"、"damping"等具体的禁词作为FAIL依据，但**这些词根本不在模型响应里**，`evidence_check.py` 的substring检查直接捕获了这一点。
- **错分类（misclassified）**：OpenAI把响应里**真实出现**的 "fired"、"pulled"、"preserved"、"influences"、"factor"、"weight"、"insulation" 等普通词错认为是禁词列表里某词的形态变体。"weight" 不是mass，"factor" 不是force，但OpenAI在03_decay上系统性地这样分类。

### 7.1 失效机制

我们假设这一系统性失效的机制是：**当禁词列表长（20+ token）且响应主题与禁词语义高度重叠时，OpenAI裁判从字面substring匹配模式悄悄退化为语义关联模式**，尽管prompt在多处明确要求"literal token match"。

Decay World正好同时具备这两个条件：

1. **长禁词列表**：20+ tokens跨mechanism / mechanics / physicist names / equation forms四类。
2. **主题高语义重叠**：Decay World的描述本质上就是讲"这里没有摩擦、没有阻尼、没有黏滞"，响应里**不可避免地**要提及这些禁词的语义概念（即使用替代词），triggers OpenAI的语义关联反射。

同样的prompt在02_fmv上（禁词列表短得多、主题语义重叠较小）OpenAI工作得不错，agreement = 21%（不高但是另一种失效模式：verdict-field self-contradiction）。在03_decay这种压力测试下，OpenAI的失效率跳到16/18 = 89%。

### 7.2 对 LLM-as-judge 文献的贡献

这一发现的方法论价值在于它**可机制化复现**：

- 失效**有可识别条件**（长禁词列表 + 主题语义重叠）。
- 失效**可被工程化捕获**（`evidence_check.py` 抓substring不匹配的虚构引用。misclassification需要人审或第二个机制化检查）。
- 失效**与具体模型版本绑定**，但**机制本身**（语义关联 ≠ 字面匹配）大概率会迁移到任何前沿模型上的同类设置。

PhysLit在设计上把这一类失效防住的是**双裁判 + IRR > 25% 触发人审**这一保险，03_decay的IRR达到40%，触发了54个case的人工audit，所有OpenAI的虚构与错分类都被识别和修正。**没有这层兜底，03_decay的content判定会被系统性误判。**

---

## 8. 讨论

### 8.1 三组实验合并起来告诉我们的"模型物理素养"画像

按四个认知动作展开：

- **归纳能力**：在简单反事实（F=mv，单方程单领域）上**充分**，Claude与GPT各5/5。在历史框架（亚里士多德）和复杂反事实（Decay）上**部分到不充分**，失败的具体形式与框架性质相关（亚里士多德是禁词泄露与Newton词汇外溢、Decay是N4不满足与隐藏底物陷阱）。
- **系统化能力**：默认弱（structural axis在02_fmv 5/15、亚里士多德8/15），一句**公理化提示**就能拉到饱和（11/15、15/15）。这是一条"能力是默认行为而非能力上限"的清晰证据。
- **应用能力**：**定性方向上无错**（Decay上60/60知道方向）。**定量比例上系统性套用训练数据里的标准公式**（Decay上23/60套了ratio）。
- **反思能力**：稳定65–70% over-claim，与框架性质和难度无关，**与具体物理内容解耦**的元认知层失调。

把这四点合起来：**前沿模型有物理上的定性直觉，结构化推理能力存在但需要触发，定量演绎能力受训练数据公式强引力，元认知校准接近常数偏低**。

### 8.2 三个框架的难度梯度设计回头看

三组实验合起来说明，难度梯度的设计意图是站得住的，单方程反事实 → 历史框架 → 跨领域反事实 + 无substrate，每一步都引入了一项新的认知压力，每一步都看到了composite PASS的下降（9/15 → 5/15 → 0/15）。这一结构本身也是本文的方法论贡献，**在物理素养评估上，分难度做平行实验可以分离不同的认知压力，把模型的失败模式做归因**。

### 8.3 局限性

- **N=5/(model, stage)**：PhysLit报告所有数字都是描述性的，不主张统计显著性。某些细分桶的样本量是1（如03_decay Stage 1 §5 P2 = 1）。
- **三个框架不是15个**：原v1.0 ambition（15个框架）已经被显式放弃，转向methodology-first的迭代节奏。
- **三家前沿模型**：三家覆盖主流前沿但不是穷尽，后续研究应纳入更多模型族和更早期模型（看难度梯度是否在能力较弱的模型上"提前饱和"）。
- **两judge架构**：是地板而非天花板。某些场景（如03_decay上OpenAI的 §3系统性失效）暴露出双judge也可以同时偏掉，所以25% IRR + 人审是必要的最后一道兜底。

### 8.4 对评估基准设计的方法论启示

- **per-question PASS rate ≠ cognitive evaluation**。把"答对几道题"作为指标的基准回答不了"模型懂不懂物理"。
- **Pre-reg + audit是地板而非天花板**。任何基准如果不预先SHA-256锁定判据，事后总是可以"按数据调整判据"。这不是道德问题，是工程问题，无可锁定的研究在长期可信度上会输给可锁定的。
- **LLM-as-judge有框架特异的失效模式**。本文展示的OpenAI §3失效是一个具体案例。任何依赖单一LLM裁判的评估都应当公开IRR、并准备好把IRR高的判断送审。

---

## 9. 相关工作

**物理领域LLM基准。** GSM8K、MATH、SciQ、PhysicsQA等基准把"答对一道物理题"作为判定单元。这一范式在覆盖度上有效，在"区分懂与不懂"上有结构性局限（§1.1）。本文不与之竞争具体题目集，而是提供一个**正交维度**，cognitive process的评估。

**反事实评估。** BIG-Bench、GLUE-X、各类counterfactual evaluation工作把"训练数据外推"作为评估目标。我们的三组实验都属于这一族。区别在于PhysLit把**整个**反事实世界（含完整观察、判据、应用场景）显式建构出来，且对"训练数据先验是否被压制"的过程做了归纳 → 系统化 → 应用 → 反思的四阶段分解。

**LLM-as-judge的可靠性研究。** 近期文献开始系统记录单judge评估的偏差与跨model agreement的限度。本文给这一文献增加了两个具体数据点：（a) 同一judge同一prompt跨framework可靠性反转。（b) 长禁词列表 + 主题语义重叠条件下，OpenAI judge从字面匹配滑入语义关联，并将该机制工程化为 `evidence_check.py` 的substring guard。

**元认知 / 自我评估。** 关于LLM在不同任务上自我评估校准能力的研究文献正在快速积累。本文报告的"三框架65–70% 稳定over-claim比率"是一个具体、可量化、框架无关的数据点。future work应当在更多框架与任务类型上检验这一稳定性。

---

## 10. 结论

我们用三个难度递增的物理世界对三家前沿大语言模型做了prereg + dual-judge + audit的完整四阶段实验。综合通过率9/15 → 5/15 → 0/15的难度梯度走出后，三个独立的、跨框架站得住的发现浮现：模型的物理素养**定性强而定量弱**、元认知校准**与框架无关且偏低**、不同LLM裁判的可靠性**不跨框架可迁移**。这三条结论分别对评估**模型能力**、评估**模型自我评估**、和评估**评估方法本身**给出了具体的可复现数据点。

PhysLit不是一个"打分基准"，它是一套关于**如何认真测试一个LLM是否懂物理**的方法论提案，配合一组让方法论本身经受住检验的具体数据。我们公开全部prompt、响应、判定与audit记录，邀请同行复现、质疑、扩展。

---

## 11. 参考文献

[1] J. Wei, X. Wang, D. Schuurmans, M. Bosma, B. Ichter, F. Xia, E. Chi, Q. Le, D. Zhou. Chain-of-Thought Prompting Elicits Reasoning in Large Language Models. *NeurIPS* 2022. arXiv: 2201.11903.

[2] K. Cobbe, V. Kosaraju, M. Bavarian, M. Chen, H. Jun, L. Kaiser, M. Plappert, J. Tworek, J. Hilton, R. Nakano, C. Hesse, J. Schulman. Training Verifiers to Solve Math Word Problems (GSM8K). arXiv: 2110.14168, 2021.

[3] T. Kojima, S. S. Gu, M. Reid, Y. Matsuo, Y. Iwasawa. Large Language Models are Zero-Shot Reasoners. *NeurIPS* 2022. arXiv: 2205.11916.

[4] T. B. Brown, B. Mann, N. Ryder, M. Subbiah, J. Kaplan, P. Dhariwal, et al. Language Models are Few-Shot Learners. *NeurIPS* 2020. arXiv: 2005.14165.

[5] J. Wei, Y. Tay, R. Bommasani, C. Raffel, B. Zoph, S. Borgeaud, D. Yogatama, M. Bosma, D. Zhou, D. Metzler, E. H. Chi, T. Hashimoto, O. Vinyals, P. Liang, J. Dean, W. Fedus. Emergent Abilities of Large Language Models. *Transactions on Machine Learning Research (TMLR)* 2022. arXiv: 2206.07682.

[6] R. Schaeffer, B. Miranda, S. Koyejo. Are Emergent Abilities of Large Language Models a Mirage? *NeurIPS* 2023. arXiv: 2304.15004.

[7] I. Mirzadeh, K. Alizadeh, H. Shahrokhi, O. Tuzel, S. Bengio, M. Farajtabar. GSM-Symbolic: Understanding the Limitations of Mathematical Reasoning in Large Language Models. arXiv: 2410.05229, 2024.

[8] J. Huang, K. C.-C. Chang. Towards Reasoning in Large Language Models: A Survey. arXiv: 2212.10403, 2023.

[9] D. A. Boiko, R. MacKnight, B. Kline, G. Gomes. Autonomous Chemical Research with Large Language Models. *Nature* 624, 570–578 (2023). DOI: 10.1038/s41586-023-06792-0.

[10] B. Romera-Paredes, M. Barekatain, A. Novikov, M. Balog, M. P. Kumar, E. Dupont, F. J. R. Ruiz, J. S. Ellenberg, P. Wang, O. Fawzi, P. Kohli, A. Fawzi. Mathematical Discoveries from Program Search with Large Language Models (FunSearch). *Nature* 625, 468–475 (2024). DOI: 10.1038/s41586-023-06924-6.

[11] J. Gottweis, V. Natarajan, et al. Towards an AI Co-Scientist: A Multi-Agent System for Hypothesis Generation. *Nature*, 2026 (published online 19 May 2026).

[12] A. E. Ghareeb, et al. Robin: A Multi-Agent System for Automating Scientific Discovery. *Nature*, 2026. DOI: 10.1038/s41586-026-10652-y.

[13] C. Lu, C. Lu, R. T. Lange, J. Foerster, J. Clune, D. Ha. The AI Scientist: Towards Fully Automated Open-Ended Scientific Discovery. arXiv: 2408.06292, 2024.

[14] T. H. Trinh, Y. Wu, Q. V. Le, H. He, T. Luong. Solving Olympiad Geometry without Human Demonstrations (AlphaGeometry). *Nature* 625, 476–482 (2024). DOI: 10.1038/s41586-023-06747-5.

[15] OpenAI. Disproof of the Erdős Unit Distance Conjecture. arXiv: 2605.20695, 2026. External verification co-authored by nine mathematicians.

[16] D. Ha, J. Schmidhuber. World Models. *NeurIPS* 2018. arXiv: 1803.10122.

[17] Y. LeCun. A Path Towards Autonomous Machine Intelligence (Position Paper, version 0.9). OpenReview, June 2022.

[18] J. Ding, et al. Understanding World or Predicting Future? A Comprehensive Survey of World Models. *ACM Computing Surveys*, 2025. arXiv: 2411.14499, 2024.

[19] K. Li, A. K. Hopkins, D. Bau, F. Viégas, H. Pfister, M. Wattenberg. Emergent World Representations: Exploring a Sequence Model Trained on a Synthetic Task. *ICLR* 2023. arXiv: 2210.13382.

[20] K. Vafa, J. Y. Chen, A. Rambachan, J. Kleinberg, S. Mullainathan. Evaluating the World Model Implicit in a Generative Model. *NeurIPS* 2024. arXiv: 2406.03689.

[21] D. M. Bear, E. Wang, D. Mrowca, F. J. Binder, H.-Y. F. Tung, R. T. Pramod, C. Holdaway, S. Tao, K. Smith, F.-Y. Sun, L. Fei-Fei, N. Kanwisher, J. B. Tenenbaum, D. L. K. Yamins, J. E. Fan. Physion: Evaluating Physical Prediction from Vision in Humans and Machines. *NeurIPS Datasets and Benchmarks* 2021. arXiv: 2106.08261.

[22] D. Hendrycks, C. Burns, S. Kadavath, A. Arora, S. Basart, E. Tang, D. Song, J. Steinhardt. Measuring Mathematical Problem Solving with the MATH Dataset. *NeurIPS Datasets and Benchmarks* 2021. arXiv: 2103.03874.

[23] X. Wang, Z. Hu, P. Lu, Y. Zhu, J. Zhang, S. Subramaniam, A. R. Loomba, S. Zhang, Y. Sun, W. Wang. SciBench: Evaluating College-Level Scientific Problem-Solving Abilities of Large Language Models. *ICML* 2024. arXiv: 2307.10635.

[24] W. Chen, M. Yin, M. Ku, P. Lu, Y. Wan, X. Ma, J. Xu, X. Wang, T. Xia. TheoremQA: A Theorem-driven Question Answering Dataset. *EMNLP* 2023. arXiv: 2305.12524.

[25] D. Arora, H. G. Singh, Mausam. Have LLMs Advanced Enough? A Challenging Problem Solving Benchmark for Large Language Models (JEEBench). *EMNLP* 2023. arXiv: 2305.15074.

[26] C. He, R. Luo, Y. Bai, S. Hu, Z. L. Thai, J. Shen, J. Hu, X. Han, Y. Huang, Y. Zhang, J. Liu, L. Qi, Z. Liu, M. Sun. OlympiadBench: A Challenging Benchmark for Promoting AGI with Olympiad-Level Bilingual Multimodal Scientific Problems. *ACL* 2024. arXiv: 2402.14008.

---

## 附录

### A. 三个框架的 pre-registration tag 与 SHA-256

| Framework | Tag | 主要prereg文件 |
|---|---|---|
| F=mv | `prereg-02_fmv-locked` | `predictions/02_fmv_prereg.md` |
| Aristotelian | `prereg-v0.1-locked` | `predictions/v0_1_prereg.md` |
| Decay World | `prereg-03_decay-locked` | `predictions/03_decay_prereg.md` |

各tag的SHA-256与对应文件头声明一致，由 `scripts/verify_prereg_integrity.py` 在CI和pre-commit hook双重检查。

### B. 三组实验的总成本

| 轮次 | 成本（USD） |
|---|---|
| v0.1 | ≈ 14 |
| v0.2（叠加分析、无新production trial） | ≈ 4 |
| 02_fmv | ≈ 17 |
| 02_fmv.1 | ≈ 4 |
| 02_fmv.2 | ≈ 5 |
| v0.3 | ≈ 7 |
| 03_decay | ≈ 25 |
| **累计** | **≈ 76** |

### C. 完整可复现入口

```bash
git clone https://github.com/dongzhang84/physlit
cd physlit
uv sync

# Decay World（最新、最完整一轮）：
git checkout prereg-03_decay-locked
uv run python scripts/run_03_decay.py
uv run python scripts/judge_03_decay.py
uv run python scripts/apply_03_decay.py
```

详细见 `README.md` "Reproducing the experiments" 段。
