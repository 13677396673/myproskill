import type { ChapterDef } from "./types";
import Coldopen from "../chapters/01-coldopen/Coldopen";
import { narrations as coldopenNarrations } from "../chapters/01-coldopen/narrations";
import Principles from "../chapters/02-principles/Principles";
import { narrations as principlesNarrations } from "../chapters/02-principles/narrations";
import DualSource from "../chapters/03-dual-source/DualSource";
import { narrations as dualSourceNarrations } from "../chapters/03-dual-source/narrations";
import Workflow from "../chapters/04-workflow/Workflow";
import { narrations as workflowNarrations } from "../chapters/04-workflow/narrations";
import Themes from "../chapters/05-themes/Themes";
import { narrations as themesNarrations } from "../chapters/05-themes/narrations";
import AntiAi from "../chapters/06-anti-ai/AntiAi";
import { narrations as antiAiNarrations } from "../chapters/06-anti-ai/narrations";
import TechArch from "../chapters/07-tech-arch/TechArch";
import { narrations as techArchNarrations } from "../chapters/07-tech-arch/narrations";
import Ending from "../chapters/08-ending/Ending";
import { narrations as endingNarrations } from "../chapters/08-ending/narrations";

export const CHAPTERS: ChapterDef[] = [
  {
    id: "coldopen",
    title: "开场：三个尴尬",
    narrations: coldopenNarrations,
    Component: Coldopen,
  },
  {
    id: "principles",
    title: "十条核心原则",
    narrations: principlesNarrations,
    Component: Principles,
  },
  {
    id: "dual-source",
    title: "双源原则",
    narrations: dualSourceNarrations,
    Component: DualSource,
  },
  {
    id: "workflow",
    title: "工作流与Checkpoint",
    narrations: workflowNarrations,
    Component: Workflow,
  },
  {
    id: "themes",
    title: "主题系统",
    narrations: themesNarrations,
    Component: Themes,
  },
  {
    id: "anti-ai",
    title: "反AI味",
    narrations: antiAiNarrations,
    Component: AntiAi,
  },
  {
    id: "tech-arch",
    title: "技术架构",
    narrations: techArchNarrations,
    Component: TechArch,
  },
  {
    id: "ending",
    title: "尾声：四点心得",
    narrations: endingNarrations,
    Component: Ending,
  },
];
