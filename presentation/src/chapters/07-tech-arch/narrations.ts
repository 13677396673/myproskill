import type { Narration } from "../../registry/types";

export const narrations: Narration[] = [
  // step 0
  "技术架构三个设计。",
  // step 1
  "step 游标模型，useStepper 加 localStorage。",
  // step 2
  "没有 useEffect，全部 CSS keyframes 声明式完成。",
  // step 3
  "五处永远同步：口播稿、计划、代码、注册、音频。",
  // step 4
  "源头都是同一个 narrations.ts。",
  // step 5
  "Auto 模式，每段音频加两百毫秒缓冲。",
  // step 6
  "加个参数就能全自动播放。",
  // step 7
  "动画比口播长会被直接切断。倒逼节奏对齐。",
  // step 8
  "Provider-agnostic 音频，每个后端一个脚本，三函数契约。",
  // step 9
  "内置 Minimax、OpenAI、小米 MiMo。想换照着改就行。",
];
