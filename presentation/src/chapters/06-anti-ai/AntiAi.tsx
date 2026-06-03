import type { ChapterStepProps } from "../../registry/types";
import "./AntiAi.css";

export default function AntiAi({ step }: ChapterStepProps) {
  if (step === 0) {
    return (
      <div className="ai-scene scene-pad">
        <div className="masthead"><span className="brand">Anti-AI</span><span className="issue">反 AI 味</span></div>
        <hr className="rule" style={{ marginTop: "var(--space-5)" }} />
        <div className="ai-cover-body">
          <div className="kicker">设计方法论中最硬的一刀</div>
          <h1 className="ai-cover-h"><span className="serif-it ai-accent">视觉指纹</span><span className="serif-cn">，全部禁止</span></h1>
        </div>
      </div>
    );
  }
  if (step === 1) {
    return (
      <div className="ai-scene ai-center-scene">
        <div className="ai-center-layout">
          <div className="kicker" style={{ marginBottom: "var(--space-4)" }}>禁止</div>
          <div className="ai-bad-grid">
            <div className="ai-bad-item" style={{ background: "linear-gradient(135deg, #a78bfa, #7c3aed)", borderRadius: "var(--r-sm)" }}>
              <span className="kicker ai-bad-label">紫粉渐变</span>
            </div>
            <div className="ai-bad-item" style={{ background: "var(--surface-2)", borderRadius: "12px", borderLeft: "4px solid #c084fc" }}>
              <span className="kicker ai-bad-label">彩色边框</span>
            </div>
            <div className="ai-bad-item" style={{ background: "var(--surface-2)", borderRadius: "999px" }}>
              <span className="kicker ai-bad-label">圆角药丸</span>
            </div>
          </div>
        </div>
      </div>
    );
  }
  if (step === 2) {
    return (
      <div className="ai-scene ai-center-scene">
        <div className="ai-center-layout">
          <div className="kicker" style={{ marginBottom: "var(--space-4)" }}>禁止</div>
          <div className="ai-bad-inline">
            <span className="ai-bad-chip">emoji 当图标</span>
            <span className="ai-bad-chip">假数据</span>
            <span className="ai-bad-chip">假 logo</span>
          </div>
        </div>
      </div>
    );
  }
  if (step === 3) {
    return (
      <div className="ai-scene ai-center-scene">
        <div className="ai-center-layout">
          <div className="kicker" style={{ marginBottom: "var(--space-4)" }}>原则</div>
          <h2 className="ai-rule-h"><span className="serif-cn">没有就</span><span className="serif-it ai-accent">承认没有</span></h2>
          <div className="ai-rule-sub serif-cn">比 fake 强一百倍</div>
        </div>
      </div>
    );
  }
  if (step === 4) {
    return (
      <div className="ai-scene ai-center-scene">
        <div className="ai-center-layout">
          <div className="kicker" style={{ marginBottom: "var(--space-4)" }}>口播稿 · 五类腔调</div>
          <div className="ai-fault-list">
            <span className="ai-fault-item" style={{ textDecoration: "line-through", opacity: 0.5 }}>假共情</span>
            <span className="ai-fault-item" style={{ textDecoration: "line-through", opacity: 0.5 }}>假深刻</span>
            <span className="ai-fault-item" style={{ textDecoration: "line-through", opacity: 0.5 }}>自我标榜</span>
          </div>
        </div>
      </div>
    );
  }
  if (step === 5) {
    return (
      <div className="ai-scene ai-center-scene">
        <div className="ai-center-layout">
          <div className="kicker" style={{ marginBottom: "var(--space-4)" }}>口播稿 · 五类腔调</div>
          <div className="ai-fault-list">
            <span className="ai-fault-item" style={{ textDecoration: "line-through", opacity: 0.5 }}>万能模板</span>
            <span className="ai-fault-item" style={{ textDecoration: "line-through", opacity: 0.5 }}>排比堆砌</span>
          </div>
        </div>
      </div>
    );
  }
  if (step === 6) {
    return (
      <div className="ai-scene ai-center-scene">
        <div className="ai-center-layout">
          <div className="kicker" style={{ marginBottom: "var(--space-4)" }}>口播稿</div>
          <div className="ai-clean-list">
            <span className="ai-clean-item serif-cn">短句 ≤ 20 字</span>
            <span className="ai-clean-item serif-cn">第二人称</span>
            <span className="ai-clean-item serif-cn">具体例子优先</span>
          </div>
        </div>
      </div>
    );
  }
  return (
    <div className="ai-scene ai-center-scene">
      <div className="ai-center-layout">
        <div className="kicker" style={{ marginBottom: "var(--space-4)" }}>黄金标准</div>
        <h2 className="ai-final-h">
          <span className="serif-it ai-accent">一个真人</span>
          <br />
          <span className="serif-cn">会这么说吗？</span>
        </h2>
      </div>
    </div>
  );
}
