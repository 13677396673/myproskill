import type { Narration } from "../../registry/types";

export const narrations: Narration[] = [
  // step 0 — intro
  "它的核心不是模板，是十条原则加一套方法论。",
  // step 1 — 16:9 stage
  "第一，16 比 9 固定舞台。1920 乘 1080 坐标系，transform scale 缩放。没有响应式。",
  // step 2 — scale demo
  "这就是视频，不是网页。",
  // step 3 — step pure function
  "第二，每步独占整屏。if step 等于 N，返回对应场景。",
  // step 4 — simplicity
  "简单到不可能出错。",
  // step 5 — content-driven animation intro
  "第三，内容驱动动画。先找内在动作。",
  // step 6 — number increment
  "数字递增、排名交换。",
  // step 7 — flow
  "流程节点依次点亮。",
  // step 8 — pace = step
  "第四，口播节拍等于 step。稿子里用三个短横线切分一个想法。",
  // step 9 — hide chrome
  "第五，隐藏 chrome。进度条默认透明，鼠标悬浮才出现。",
  // step 10 — clean recording
  "录屏时没有任何浏览器痕迹。",
  // step 11 — summary
  "找不到才用入场动画。这决定了你是视频还是翻 PPT。",
];
