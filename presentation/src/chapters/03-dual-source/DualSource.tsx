import type { ChapterStepProps } from "../../registry/types";
import "./DualSource.css";

export default function DualSource({ step }: ChapterStepProps) {
  if (step === 0) {
    return (
      <div className="ds-scene scene-pad">
        <div className="masthead">
          <span className="brand">Design</span>
          <span className="issue">双源原则</span>
        </div>
        <hr className="rule" style={{ marginTop: "var(--space-5)" }} />
        <div className="ds-cover-body">
          <div className="kicker">两个信息源</div>
          <h1 className="ds-cover-h">
            <span className="serif-cn">口播稿定节奏</span>
            <br />
            <span className="serif-cn">原文定</span>
            <span className="serif-it ds-accent">画面密度</span>
          </h1>
        </div>
      </div>
    );
  }
  if (step === 1) {
    return (
      <div className="ds-scene scene-pad">
        <div className="ds-section-hdr">
          <span className="hero-num ds-sec-num">源 1</span>
          <span className="kicker">口播稿 · script.md</span>
        </div>
        <hr className="rule" style={{ marginTop: "var(--space-5)" }} />
        <div className="ds-demo">
          <div className="ds-flow">
            <div className="ds-flow-item ds-flow-active">
              <span className="ds-flow-step kicker">step 1</span>
              <span className="ds-flow-text serif-cn">一句话一个聚焦想法</span>
            </div>
            <div className="ds-flow-arrow serif-it">↓</div>
            <div className="ds-flow-item">
              <span className="ds-flow-step kicker">step 2</span>
              <span className="ds-flow-text serif-cn">下一个聚焦想法</span>
            </div>
            <div className="ds-flow-arrow serif-it">↓</div>
            <div className="ds-flow-item">
              <span className="ds-flow-step kicker">step 3</span>
              <span className="ds-flow-text serif-cn">再下一个</span>
            </div>
          </div>
          <div className="ds-caption serif-cn">决定节奏和顺序</div>
        </div>
      </div>
    );
  }
  if (step === 2) {
    return (
      <div className="ds-scene scene-pad">
        <div className="ds-section-hdr">
          <span className="hero-num ds-sec-num">源 2</span>
          <span className="kicker">原文 · article.md</span>
        </div>
        <hr className="rule" style={{ marginTop: "var(--space-5)" }} />
        <div className="ds-demo">
          <div className="ds-pool">
            <div className="ds-pool-item">
              <span className="ds-pool-tag kicker">数字</span>
              <span className="ds-pool-val serif-cn">准确率 47%</span>
            </div>
            <div className="ds-pool-item">
              <span className="ds-pool-tag kicker">引用</span>
              <span className="ds-pool-val serif-cn">"方法论比模板重要"</span>
            </div>
            <div className="ds-pool-item">
              <span className="ds-pool-tag kicker">案例</span>
              <span className="ds-pool-val serif-cn">23 套主题·25~35 CSS token</span>
            </div>
          </div>
          <div className="ds-caption serif-cn">决定画面信息密度</div>
        </div>
      </div>
    );
  }
  if (step === 3) {
    return (
      <div className="ds-scene ds-center-scene">
        <div className="ds-center-layout">
          <div className="kicker" style={{ marginBottom: "var(--space-5)" }}>
            双源在行动
          </div>
          <div className="ds-action-h">
            <span className="serif-cn">画面细节从</span>
            <span className="serif-it ds-accent">原文里挖</span>
          </div>
          <div className="ds-action-items">
            <span className="ds-action-tag">具体数字</span>
            <span className="ds-action-tag">引用原话</span>
            <span className="ds-action-tag">案例维度</span>
            <span className="ds-action-tag">出处时间</span>
          </div>
        </div>
      </div>
    );
  }
  if (step === 4) {
    return (
      <div className="ds-scene scene-pad">
        <div className="ds-section-hdr">
          <span className="hero-num ds-sec-num" style={{ color: "var(--text-faint)" }}>XX</span>
          <span className="kicker">反面教材</span>
        </div>
        <hr className="rule" style={{ marginTop: "var(--space-5)" }} />
        <div className="ds-demo">
          <div className="ds-wrong-demo">
            <div className="ds-wrong-line" />
            <div className="ds-wrong-line ds-wrong-short" />
            <div className="ds-wrong-line" />
          </div>
          <div className="ds-caption ds-caution serif-cn">只用口播稿做画面</div>
        </div>
      </div>
    );
  }
  return (
    <div className="ds-scene ds-center-scene">
      <div className="ds-center-layout">
        <div className="kicker" style={{ marginBottom: "var(--space-4)" }}>
          后果
        </div>
        <h2 className="ds-final-h">
          <span className="serif-it ds-accent">屏幕等于</span>
          <br />
          <span className="serif-cn">把口播打字打了一遍</span>
        </h2>
        <div className="ds-final-sub serif-cn">那是 PPT，不是视频</div>
      </div>
    </div>
  );
}
