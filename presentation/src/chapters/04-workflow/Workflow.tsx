import type { ChapterStepProps } from "../../registry/types";
import "./Workflow.css";

export default function Workflow({ step }: ChapterStepProps) {
  if (step === 0) {
    return (
      <div className="wf-scene scene-pad">
        <div className="masthead"><span className="brand">Process</span><span className="issue">工作流</span></div>
        <hr className="rule" style={{ marginTop: "var(--space-5)" }} />
        <div className="wf-cover-body">
          <div className="kicker">硬 Checkpoint 分段协作</div>
          <h1 className="wf-cover-h"><span className="serif-cn">不是闷头</span><span className="serif-it wf-accent">跑到底</span></h1>
        </div>
      </div>
    );
  }
  if (step === 1) {
    return (
      <div className="wf-scene scene-pad">
        <div className="wf-phase-hdr"><span className="hero-num wf-phase-num">P1</span><span className="kicker">内容编写</span></div>
        <hr className="rule" style={{ marginTop: "var(--space-5)" }} />
        <div className="wf-demo">
          <div className="wf-outputs">
            <div className="wf-file"><span className="wf-file-icon"><span className="wf-file-box" /></span><span className="wf-file-name kicker">script.md</span><span className="wf-file-desc serif-cn">口播稿</span></div>
            <div className="wf-file"><span className="wf-file-icon"><span className="wf-file-box" /></span><span className="wf-file-name kicker">outline.md</span><span className="wf-file-desc serif-cn">开发计划</span></div>
          </div>
          <div className="wf-caption serif-cn">一次产出两份文件，都要走自检</div>
        </div>
      </div>
    );
  }
  if (step === 2) {
    return (
      <div className="wf-scene wf-center-scene">
        <div className="wf-center-layout">
          <div className="kicker" style={{ marginBottom: "var(--space-4)" }}>自检协议</div>
          <h2 className="wf-feature-h"><span className="serif-cn">逐项核查</span><br /><span className="serif-it wf-accent">逐条修复</span></h2>
          <div className="wf-feature-sub serif-cn">改完才能进下一阶段</div>
        </div>
      </div>
    );
  }
  if (step === 3) {
    return (
      <div className="wf-scene scene-pad">
        <div className="wf-phase-hdr"><span className="hero-num wf-phase-num">CP</span><span className="kicker">Checkpoint Plan</span></div>
        <hr className="rule" style={{ marginTop: "var(--space-5)" }} />
        <div className="wf-demo">
          <div className="wf-checklist">
            <div className="wf-check-item"><span className="wf-check-bullet" />稿子</div>
            <div className="wf-check-item"><span className="wf-check-bullet" />计划</div>
            <div className="wf-check-item"><span className="wf-check-bullet" />主题</div>
            <div className="wf-check-item"><span className="wf-check-bullet" />素材</div>
            <div className="wf-check-item"><span className="wf-check-bullet" />模式</div>
          </div>
          <div className="wf-caption serif-cn">五件事一次对齐</div>
        </div>
      </div>
    );
  }
  if (step === 4) {
    return (
      <div className="wf-scene scene-pad">
        <div className="wf-phase-hdr"><span className="hero-num wf-phase-num">P2</span><span className="kicker">网页开发</span></div>
        <hr className="rule" style={{ marginTop: "var(--space-5)" }} />
        <div className="wf-demo">
          <div className="wf-code-icon">
            <div className="wf-code-line-small" /><div className="wf-code-line-small wf-cl-short" />
          </div>
          <div className="wf-caption serif-cn">脚手架一键生成项目</div>
        </div>
      </div>
    );
  }
  if (step === 5) {
    return (
      <div className="wf-scene wf-center-scene">
        <div className="wf-center-layout">
          <div className="kicker" style={{ marginBottom: "var(--space-4)" }}>第一章</div>
          <h2 className="wf-feature-h"><span className="serif-it wf-accent">强制 anchor</span></h2>
          <div className="wf-feature-sub serif-cn">主线程做完 + 用户验收</div>
        </div>
      </div>
    );
  }
  if (step === 6) {
    return (
      <div className="wf-scene scene-pad">
        <div className="wf-phase-hdr"><span className="hero-num wf-phase-num">A</span><span className="kicker">逐章确认</span></div>
        <hr className="rule" style={{ marginTop: "var(--space-5)" }} />
        <div className="wf-demo">
          <div className="wf-modes">
            <div className="wf-mode wf-mode-active"><span className="wf-mode-dot" /><span className="serif-cn">第 2 章</span></div>
            <div className="wf-mode-arrow serif-it">→</div>
            <div className="wf-mode"><span className="wf-mode-dot" /><span className="serif-cn">验收</span></div>
            <div className="wf-mode-arrow serif-it">→</div>
            <div className="wf-mode"><span className="wf-mode-dot" /><span className="serif-cn">第 3 章</span></div>
          </div>
          <div className="wf-caption serif-cn">每章做完暂停，风险可控</div>
        </div>
      </div>
    );
  }
  return (
    <div className="wf-scene wf-center-scene">
      <div className="wf-center-layout">
        <div className="kicker" style={{ marginBottom: "var(--space-4)" }}>模式 B / C</div>
        <h2 className="wf-feature-h"><span className="serif-cn">顺序开发</span><span className="serif-it wf-accent"> 或 </span><span className="serif-cn">并行</span></h2>
        <div className="wf-feature-sub serif-cn">subagent 多章同时开工</div>
      </div>
    </div>
  );
}
