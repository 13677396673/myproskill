# Video Outline

> **主题**：`vintage-editorial`（复古编辑）—— 奶油底 + 厚体 Fraunces 斜体 + 暖陶强调色，有性格、会说话
> **总时长**：约 8 分 10 秒（口播 ~1960 字 ÷ 4 字/秒）
> **章节数**：8 章 / 66 步

---

## 1. coldopen — 开场：三个尴尬（8 steps · ~55s）

**信息池**：
- 三个尴尬场景：传统幻灯片 / 纯文字无画面 / 紫粉渐变+圆角卡片+emoji —— 来源 article L7-L11
- 核心问题：文章→看起来像视频的网页演示 —— 来源 article L11
- 输出：Vite+React+TS 项目，16:9 固定画幅 —— 来源 article L17
- 适用场景：公众号→B站/YouTube、产品演示、教程、路演demo —— 来源 article L22-L25
- ?auto=1 自动播放，一镜到底录屏无需对轨 —— 来源 article L19

**开发计划**：
- step 1 (~5s) — Hook：三个尴尬场景
- step 2 (~5s) — 传统幻灯片问题
- step 3 (~5s) — 纯文字画面问题
- step 4 (~5s) — AI味视觉问题
- step 5 (~7s) — 核心矛盾：把文章变成视频
- step 6 (~10s) — web-video-presentation介绍+输入输出
- step 7 (~8s) — auto模式：一镜到底无需对轨
- step 8 (~8s) — 适用场景列举

口播节选：
> 你遇到过这些尴尬吗？让 AI 帮你做演示视频，结果出来的是传统幻灯片。
> 这些问题指向同一个核心矛盾。

---

## 2. principles — 十条核心原则（12 steps · ~90s）

**信息池**：
- 方法论+协作流程，不是模板 —— 来源 article L31
- 1920×1080+transform:scale，无响应式 —— 来源 article L37-L38
- if(step===N) return <FullScene /> —— 来源 article L40
- 内在动作：数字递增、排名交换、流程节点点亮 —— 来源 article L41
- 口播节拍=step，--- 分段 —— 来源 article L42-L44
- 进度条/翻页控件 opacity:0 —— 来源 article L45

**开发计划**：
- step 1 (~7s) — 不是模板，是方法论+十条原则
- step 2 (~8s) — 16:9固定舞台
- step 3 (~5s) — 演示：1920×1080坐标系+transform scale
- step 4 (~7s) — 每步独占整屏：step纯函数
- step 5 (~5s) — 代码展示：if(step===N)简洁性
- step 6 (~10s) — 内容驱动动画 vs 入场动画兜底
- step 7 (~8s) — 内在动作：数字递增、排名交换
- step 8 (~8s) — 内在动作：流程点亮、对比切开
- step 9 (~8s) — 口播节拍=step：---分段定节奏
- step 10 (~7s) — 隐藏chrome基本原理
- step 11 (~8s) — 录屏效果对比（有/无chrome）
- step 12 (~7s) — 原则小结

口播节选：
> 这个 Skill 的核心不是模板，是一套方法论加协作流程。
> 第三，内容驱动动画。大部分 AI 生成的演示就是一套淡入效果反复用。

---

## 3. dual-source — 双源原则（6 steps · ~45s）

**信息池**：
- script定节奏+顺序，一句话一个step —— 来源 article L49-L55
- article定画面信息密度：数字/引用/案例/时间 —— 来源 article L49-L55
- "画面信息密度>口播信息密度" —— 来源 article L51
- "屏幕不仅仅是把口播打字打了一遍" —— 来源 article L56

**开发计划**：
- step 1 (~7s) — 两个信息源概述
- step 2 (~7s) — script定节奏：一句话一个step
- step 3 (~8s) — article定画面密度：数字、引用、案例
- step 4 (~8s) — 从原文挖细节：具体数字、出处时间
- step 5 (~8s) — 反面教材：只用口播稿做画面
- step 6 (~7s) — 就是PPT不是视频

口播节选：
> 每一章有两个信息源。口播稿决定节奏和顺序，原文决定画面信息密度。
> 如果只用口播稿做章节，屏幕等于把口播打字打了一遍。

---

## 4. workflow — 工作流与Checkpoint（8 steps · ~60s）

**信息池**：
- Phase1：一次产出script.md+outline.md —— 来源 article L64-L71
- 硬性自检协议 —— 来源 article L68
- Checkpoint Plan：五件事一次对齐 —— 来源 article L74-L82
- 三种模式：A逐章确认/B顺序/C并行 —— 来源 article L88-L96
- 第一章是强制anchor，必须主线程+用户验收 —— 来源 article L89

**开发计划**：
- step 1 (~5s) — 硬Checkpoint分段协作概览
- step 2 (~7s) — Phase1：一次产出两份文件+自检
- step 3 (~7s) — 硬性自检协议展示
- step 4 (~7s) — Checkpoint Plan：五件事对齐
- step 5 (~8s) — Phase2：脚手架一键生成
- step 6 (~8s) — 第一章强制anchor：主线程+验收
- step 7 (~8s) — 模式A：逐章确认（推荐）
- step 8 (~8s) — 模式B/C：顺序开发/并行

口播节选：
> 整个工作流被设计成硬 Checkpoint 分段协作，而不是闷头跑到底。
> 第一章必须在主线程做，必须做到完整版本加用户验收。

---

## 5. themes — 主题系统（8 steps · ~60s）

**信息池**：
- 23套独立设计DNA，每套25~35个CSS token —— 来源 article L100-L101
- midnight-press：espresso底+火热橙，Instrument Serif italic —— 来源 article L103
- newsroom：奶油+墨黑衬线+旗红，0圆角 —— 来源 article L106
- terminal-green：纯黑+JetBrains Mono+CRT扫描线 —— 来源 article L107
- chalk-garden：石板黑板+手写体+粉笔黄+film grain —— 来源 article L108
- 主题切换是cp命令，章节代码一行不动 —— 来源 article L113

**开发计划**：
- step 1 (~5s) — 23套独立DNA，不单是换颜色
- step 2 (~7s) — 设计签名概念：线条性格+圆角哲学
- step 3 (~8s) — Midnight Press：咖啡底+橙+衬线+电影感
- step 4 (~8s) — Newsroom：报纸奶油+墨黑+旗红，0圆角
- step 5 (~8s) — Terminal Green：纯黑+等宽+CRT扫描线
- step 6 (~8s) — 更多主题：粉笔花园、包豪斯、双拼画布
- step 7 (~8s) — 每套25~35个CSS token
- step 8 (~7s) — 切换是cp命令，章节代码不动

口播节选：
> 主题系统我花了很多精力。一共二十三套独立设计 DNA。
> 比如 Midnight Press，暖色咖啡底加火热橙色，衬线字体，慢速电影感。

---

## 6. anti-ai — 反AI味（8 steps · ~60s）

**信息池**：
- 紫粉/蓝紫对角渐变背景 —— 来源 article L121
- 圆角卡片+彩色左边框装饰 —— 来源 article L122
- emoji当图标、假数据/假logo —— 来源 article L124-L128
- 去AI味五类：假共情/假深刻/自我标榜/万能模板/排比堆砌 —— 来源 article L197-L280
- "没有就承认没有，比fake强一百倍" —— 来源 article L129

**开发计划**：
- step 1 (~5s) — AI共通视觉指纹概述
- step 2 (~7s) — 紫粉渐变、圆角卡片
- step 3 (~7s) — emoji当图标、假数据假logo
- step 4 (~7s) — 明令禁止：缺素材就承认缺
- step 5 (~8s) — 去AI味五类：假共情、假深刻
- step 6 (~8s) — 自我标榜、万能模板
- step 7 (~8s) — 排比堆砌
- step 8 (~7s) — 唯一标准：真人会这么说吗

口播节选：
> AI 生成的网页有几种共通的视觉指纹，我在 CHAPTER-CRAFT 里明令禁止。
> 没有就承认没有，比 fake 强一百倍。

---

## 7. tech-arch — 技术架构（10 steps · ~75s）

**信息池**：
- useStepper hook，localStorage持久化 —— 来源 article L153-L157
- step纯函数，无useEffect，CSS keyframes —— 来源 article L153-L157
- 5处永不漂：script/outline/代码/chapters.ts/音频 —— 来源 article L158
- Auto模式：每段音频+200ms缓冲→下一步 —— 来源 article L161-L164
- Provider-agnostic：三函数契约，4个内置provider —— 来源 article L166-L168

**开发计划**：
- step 1 (~7s) — 技术架构概览
- step 2 (~8s) — step游标模型：useStepper+localStorage
- step 3 (~7s) — step纯函数+CSS keyframes声明式
- step 4 (~5s) — 五处永不漂示意图
- step 5 (~5s) — 源头都是narrations.ts
- step 6 (~8s) — Auto模式：参数启动自动播放
- step 7 (~8s) — 200ms缓冲+自动推进
- step 8 (~8s) — 动画比口播长被切断
- step 9 (~8s) — Provider-agnostic：三函数契约
- step 10 (~7s) — 内置四个provider+可扩展

口播节选：
> 全局 useStepper hook 管理章节和 step 游标。
> Auto 模式：每段音频播完加两百毫秒缓冲，自动推进下一步。

---

## 8. ending — 尾声：四点心得（6 steps · ~45s）

**信息池**：
- Checkpoint设计比提示词重要 —— 来源 article L191
- 先定原则再写代码 —— 来源 article L192
- 去AI味不是降质 —— 来源 article L193
- 主题系统换的是签名，不是颜色 —— 来源 article L113
- GitHub开源完整代码 —— 来源 article L196

**开发计划**：
- step 1 (~5s) — 四点心得引子
- step 2 (~8s) — Checkpoint > 提示词
- step 3 (~8s) — 先定原则再写代码
- step 4 (~8s) — 去AI味不是降质
- step 5 (~8s) — 主题系统换签名不是换颜色
- step 6 (~8s) — GitHub开源 + CTA

口播节选：
> 最后分享四点做 Agent Skill 的心得。
> 去 AI 味不是降质。把 AI 在朗诵换成人在聊天，信息量一个不少。

---

## 素材清单

### 所有章节
- ⚠️ 暂无外部素材。概念解说类，文字排版+动效为主
- ⚠️ 如需插图，可从 GitHub 仓库截 theme 示例图（非必须）
