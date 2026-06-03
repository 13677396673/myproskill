import type { ChapterStepProps } from "../../registry/types";
import "./Principles.css";

export default function Principles({ step }: ChapterStepProps) {
  /* Step 0 — Intro: magazine feature opener */
  if (step === 0) {
    return (
      <div className="pr-scene scene-pad">
        <div className="masthead">
          <span className="brand">Principles</span>
          <span className="issue">The Core</span>
        </div>
        <hr className="rule" style={{ marginTop: "var(--space-5)" }} />

        <div className="pr-cover-body">
          <div className="kicker">十条核心原则</div>
          <h1 className="pr-cover-h">
            <span className="serif-it pr-accent">方法论</span>
            <span className="serif-cn"> + 协作流程</span>
          </h1>
          <div className="pr-cover-sub serif-cn">
            脚手架只提供舞台原语和主题 token
          </div>
        </div>
      </div>
    );
  }

  /* Step 1 — Principle 1: 16:9 fixed stage */
  if (step === 1) {
    return (
      <div className="pr-scene scene-pad">
        <div className="pr-principle-hdr">
          <span className="hero-num pr-principle-num">01</span>
          <span className="kicker">16:9 固定舞台</span>
        </div>
        <hr className="rule" style={{ marginTop: "var(--space-5)" }} />

        <div className="pr-demo-area">
          <div className="pr-stage-demo">
            {/* 16:9 frame */}
            <div className="pr-frame">
              <div className="pr-frame-label">
                <span className="pr-frame-dim hero-num">1920</span>
                <span className="pr-frame-x serif-cn">×</span>
                <span className="pr-frame-dim hero-num">1080</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    );
  }

  /* Step 2 — Principle 1 demo: transform scale */
  if (step === 2) {
    return (
      <div className="pr-scene scene-pad">
        <div className="pr-principle-hdr">
          <span className="hero-num pr-principle-num">01</span>
          <span className="kicker">没有响应式</span>
        </div>
        <hr className="rule" style={{ marginTop: "var(--space-5)" }} />

        <div className="pr-demo-area">
          <div className="pr-scale-demo">
            <div className="pr-scale-source">
              <div className="pr-scale-inner">1920×1080</div>
            </div>
            <div className="pr-scale-arrow serif-it">→</div>
            <div className="pr-scale-target">
              <div className="pr-scale-inner pr-scale-shrunk">transform: scale()</div>
            </div>
          </div>
          <div className="pr-caption serif-cn">外层缩放适配任何视口</div>
        </div>
      </div>
    );
  }

  /* Step 3 — Principle 2: step pure function */
  if (step === 3) {
    return (
      <div className="pr-scene scene-pad">
        <div className="pr-principle-hdr">
          <span className="hero-num pr-principle-num">02</span>
          <span className="kicker">每步独占整屏</span>
        </div>
        <hr className="rule" style={{ marginTop: "var(--space-5)" }} />

        <div className="pr-demo-area">
          <div className="pr-code-block">
            <div className="pr-code-line">
              <span className="pr-code-kw">if</span>
              <span> (</span>
              <span className="pr-code-var">step</span>
              <span> === </span>
              <span className="pr-code-num">N</span>
              <span>)</span>
            </div>
            <div className="pr-code-line pr-code-indent">
              <span>return </span>
              <span className="pr-code-tag">&lt;FullScene</span>
              <span> </span>
              <span className="pr-code-var">/</span>
              <span className="pr-code-tag">&gt;</span>
            </div>
            <div className="pr-code-line">
              <span>───</span>
            </div>
            <div className="pr-code-line pr-code-indent">
              <span>return </span>
              <span className="pr-code-tag">&lt;NextScene</span>
              <span> </span>
              <span className="pr-code-var">/</span>
              <span className="pr-code-tag">&gt;</span>
            </div>
          </div>
        </div>
      </div>
    );
  }

  /* Step 4 — Principle 2: simplicity emphasis */
  if (step === 4) {
    return (
      <div className="pr-scene pr-center-scene">
        <div className="pr-center-layout">
          <div className="kicker" style={{ marginBottom: "var(--space-5)" }}>
            02 · step 纯函数
          </div>
          <div className="pr-simple-h">
            <span className="serif-cn">简单到</span>
            <br />
            <span className="serif-it pr-accent">不可能</span>
            <span className="serif-cn">出错</span>
          </div>
          <div className="pr-simple-sub serif-cn">
            没有定时器 · 没有命令式状态
          </div>
        </div>
      </div>
    );
  }

  /* Step 5 — Principle 3: content-driven animation intro */
  if (step === 5) {
    return (
      <div className="pr-scene scene-pad">
        <div className="pr-principle-hdr">
          <span className="hero-num pr-principle-num">03</span>
          <span className="kicker">内容驱动动画</span>
        </div>
        <hr className="rule" style={{ marginTop: "var(--space-5)" }} />

        <div className="pr-demo-area">
          <div className="pr-compare">
            <div className="pr-compare-side pr-compare-wrong">
              <div className="pr-compare-label">
                <span className="pr-label-badge pr-label-wrong">wrong</span>
                <span className="kicker">入场动画</span>
              </div>
              <div className="pr-compare-boxes">
                <div className="pr-compare-box" />
                <div className="pr-compare-box" />
                <div className="pr-compare-box" />
              </div>
              <div className="pr-compare-desc serif-cn">反复淡入</div>
            </div>
            <div className="pr-compare-vs serif-it">vs</div>
            <div className="pr-compare-side pr-compare-right">
              <div className="pr-compare-label">
                <span className="pr-label-badge pr-label-right">right</span>
                <span className="kicker">内在动作</span>
              </div>
              <div className="pr-compare-bar pr-bar-growth" />
              <div className="pr-compare-desc serif-cn">数字在动</div>
            </div>
          </div>
        </div>
      </div>
    );
  }

  /* Step 6 — Inner action: number increment */
  if (step === 6) {
    return (
      <div className="pr-scene pr-center-scene">
        <div className="pr-center-layout">
          <div className="kicker" style={{ marginBottom: "var(--space-5)" }}>
            内在动作
          </div>
          <div className="pr-counter-demo">
            <span className="hero-num pr-counter-num">87</span>
            <span className="pr-counter-arrow serif-it pr-accent">→</span>
            <span className="hero-num pr-counter-num pr-counter-num-next">156</span>
          </div>
          <div className="pr-counter-label serif-cn">数字递增</div>
        </div>
      </div>
    );
  }

  /* Step 7 — Inner action: swap / flow */
  if (step === 7) {
    return (
      <div className="pr-scene pr-center-scene">
        <div className="pr-center-layout">
          <div className="kicker" style={{ marginBottom: "var(--space-5)" }}>
            内在动作
          </div>
          <div className="pr-flow-demo">
            <div className="pr-flow-node pr-flow-active">
              <span className="pr-flow-dot" />
              <span className="pr-flow-label serif-cn">节点 A</span>
            </div>
            <div className="pr-flow-line" />
            <div className="pr-flow-node">
              <span className="pr-flow-dot pr-dot-inactive" />
              <span className="pr-flow-label serif-cn">节点 B</span>
            </div>
            <div className="pr-flow-line pr-line-dim" />
            <div className="pr-flow-node">
              <span className="pr-flow-dot pr-dot-inactive" />
              <span className="pr-flow-label serif-cn">节点 C</span>
            </div>
          </div>
          <div className="pr-counter-label serif-cn">流程节点依次点亮</div>
        </div>
      </div>
    );
  }

  /* Step 8 — Principle 4: pace = step */
  if (step === 8) {
    return (
      <div className="pr-scene scene-pad">
        <div className="pr-principle-hdr">
          <span className="hero-num pr-principle-num">04</span>
          <span className="kicker">口播节拍 = step</span>
        </div>
        <hr className="rule" style={{ marginTop: "var(--space-5)" }} />

        <div className="pr-demo-area">
          <div className="pr-pace-demo">
            <div className="pr-pace-segment">
              <span className="pr-pace-text serif-cn">一个聚焦想法</span>
              <span className="pr-pace-mark kicker">step 1</span>
            </div>
            <div className="pr-pace-divider">———</div>
            <div className="pr-pace-segment">
              <span className="pr-pace-text serif-cn">下一个想法</span>
              <span className="pr-pace-mark kicker">step 2</span>
            </div>
            <div className="pr-pace-divider">———</div>
            <div className="pr-pace-segment">
              <span className="pr-pace-text serif-cn">再下一个</span>
              <span className="pr-pace-mark kicker">step 3</span>
            </div>
          </div>
        </div>
      </div>
    );
  }

  /* Step 9 — Principle 5: hide chrome */
  if (step === 9) {
    return (
      <div className="pr-scene scene-pad">
        <div className="pr-principle-hdr">
          <span className="hero-num pr-principle-num">05</span>
          <span className="kicker">隐藏 chrome</span>
        </div>
        <hr className="rule" style={{ marginTop: "var(--space-5)" }} />

        <div className="pr-demo-area">
          <div className="pr-chrome-demo">
            <div className="pr-chrome-stage">
              <div className="pr-chrome-content serif-cn">录屏画面</div>
              <div className="pr-chrome-bar">
                <div className="pr-chrome-progress" />
              </div>
            </div>
            <div className="pr-chrome-label kicker">进度条默认透明，悬浮才出现</div>
          </div>
        </div>
      </div>
    );
  }

  /* Step 10 — Chrome hidden state emphasis */
  if (step === 10) {
    return (
      <div className="pr-scene pr-center-scene">
        <div className="pr-center-layout">
          <div className="kicker" style={{ marginBottom: "var(--space-4)" }}>
            录屏效果
          </div>
          <div className="pr-clean-h">
            <span className="serif-it pr-accent">没有任何</span>
            <br />
            <span className="serif-cn">浏览器痕迹</span>
          </div>
          <div className="pr-clean-sub serif-cn">看起来就是一段成品视频</div>
        </div>
      </div>
    );
  }

  /* Step 11 — Chapter summary */
  return (
    <div className="pr-scene pr-center-scene">
      <div className="pr-center-layout">
        <div className="kicker" style={{ marginBottom: "var(--space-5)" }}>
          原则小结
        </div>
        <h2 className="pr-summary-h">
          <span className="serif-cn">找不到内在动作</span>
          <br />
          <span className="serif-it pr-accent">才用入场动画</span>
          <span className="serif-cn">兜底</span>
        </h2>
        <div className="pr-summary-sub serif-cn">
          这决定了你是视频还是翻 PPT
        </div>
      </div>
    </div>
  );
}
