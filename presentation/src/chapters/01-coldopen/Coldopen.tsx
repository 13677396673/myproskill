import type { ChapterStepProps } from "../../registry/types";
import "./Coldopen.css";

export default function Coldopen({ step }: ChapterStepProps) {
  /* Step 0 — Hook: magazine cover with three hint dots */
  if (step === 0) {
    return (
      <div className="cd-scene scene-pad">
        <div className="masthead">
          <span className="brand">web-video-presentation</span>
          <span className="issue">Issue · 00</span>
        </div>
        <hr className="rule" style={{ marginTop: "var(--space-5)" }} />

        <div className="cd-cover-body">
          <div className="kicker">你遇到过这些吗？</div>
          <h1 className="cd-cover-h">
            <span className="serif-it cd-accent">尴尬</span>
            <span className="serif-cn">的场景</span>
          </h1>
          <div className="cd-hints">
            <div className="cd-hint">
              <span className="cd-dot" />
              <span className="serif-cn cd-hint-label">传统幻灯片</span>
            </div>
            <div className="cd-hint">
              <span className="cd-dot" />
              <span className="serif-cn cd-hint-label">纯文字画面</span>
            </div>
            <div className="cd-hint">
              <span className="cd-dot" />
              <span className="serif-cn cd-hint-label">AI 视觉指纹</span>
            </div>
          </div>
        </div>
      </div>
    );
  }

  /* Step 1 — Slide pain point: mock corporate slide */
  if (step === 1) {
    return (
      <div className="cd-scene scene-pad">
        <div className="masthead">
          <span className="brand">Issue #01</span>
          <span className="issue">传统幻灯片</span>
        </div>
        <hr className="rule" style={{ marginTop: "var(--space-5)" }} />

        <div className="cd-demo-area">
          <div className="cd-slide-mock">
            <div className="cd-slide-bar" />
            <div className="cd-slide-title" />
            <div className="cd-slide-bullets">
              <div className="cd-slide-bullet" />
              <div className="cd-slide-bullet" />
              <div className="cd-slide-bullet cd-slide-bullet-short" />
            </div>
          </div>
          <div className="cd-stamp">像 PPT</div>
        </div>
      </div>
    );
  }

  /* Step 2 — Text pain point: wall of text */
  if (step === 2) {
    return (
      <div className="cd-scene scene-pad">
        <div className="masthead">
          <span className="brand">Issue #02</span>
          <span className="issue">纯文字</span>
        </div>
        <hr className="rule" style={{ marginTop: "var(--space-5)" }} />

        <div className="cd-demo-area">
          <div className="cd-text-wall">
            {[...Array(16)].map((_, i) => (
              <div
                key={i}
                className="cd-text-line"
                style={{ width: `${50 + (i * 3) % 35}%` }}
              />
            ))}
          </div>
          <div className="cd-stamp">没人想看</div>
        </div>
      </div>
    );
  }

  /* Step 3 — AI visual pain: critique specimen */
  if (step === 3) {
    return (
      <div className="cd-scene scene-pad">
        <div className="masthead">
          <span className="brand">Issue #03</span>
          <span className="issue">AI 视觉</span>
        </div>
        <hr className="rule" style={{ marginTop: "var(--space-5)" }} />

        <div className="cd-demo-area">
          <div className="cd-critique-mock">
            {/* diagonal gradient backdrop */}
            <div className="cd-critique-bg" />
            {/* rounded cards with colored left border */}
            <div className="cd-critique-card cd-critique-card-1">
              <div className="cd-critique-line" />
              <div className="cd-critique-line cd-line-short" />
            </div>
            <div className="cd-critique-card cd-critique-card-2">
              <div className="cd-critique-line" />
              <div className="cd-critique-line cd-line-short" />
            </div>
            {/* accent stamp */}
            <div className="cd-critique-badge" />
          </div>
          <div className="cd-stamp">AI 味</div>
        </div>
      </div>
    );
  }

  /* Step 4 — Pivot to core problem */
  if (step === 4) {
    return (
      <div className="cd-scene cd-center-scene">
        <div className="cd-center-layout">
          <div className="kicker" style={{ marginBottom: "var(--space-5)" }}>
            核心问题
          </div>
          <h2 className="cd-pivot-h">
            <span className="serif-cn">怎么把一篇文章</span>
            <br />
            <span className="serif-it cd-accent">变成像视频</span>
            <span className="serif-cn">的网页</span>
          </h2>
          <div className="cd-pivot-sub kicker">
            能看 · 能录 · 能发出去
          </div>
        </div>
      </div>
    );
  }

  /* Step 5 — Tool introduction */
  if (step === 5) {
    return (
      <div className="cd-scene scene-pad">
        <div className="masthead">
          <span className="brand">Solution</span>
        </div>
        <hr className="rule" style={{ marginTop: "var(--space-5)" }} />

        <div className="cd-tool-intro">
          <div className="kicker" style={{ marginBottom: "var(--space-4)" }}>
            Claude Code Skill
          </div>
          <h1 className="cd-tool-name">
            <span className="serif-it cd-accent">web-video-</span>
            <span className="serif-it">presentation</span>
          </h1>
          <div className="cd-tool-specs">
            <div className="cd-spec">
              <span className="hero-num cd-spec-num">16:9</span>
              <span className="cd-spec-label">固定画幅</span>
            </div>
            <div className="cd-spec">
              <span className="hero-num cd-spec-num">逐点击</span>
              <span className="cd-spec-label">每步独占整屏</span>
            </div>
          </div>
        </div>
      </div>
    );
  }

  /* Step 6 — Auto mode visualization */
  if (step === 6) {
    return (
      <div className="cd-scene cd-center-scene">
        <div className="cd-center-layout">
          <div className="kicker" style={{ marginBottom: "var(--space-5)" }}>
            Feature
          </div>
          <h2 className="cd-auto-h">
            <span className="serif-it cd-accent">auto</span>
            <span className="serif-cn"> 模式</span>
          </h2>
          <div className="cd-auto-visual">
            <div className="cd-auto-track">
              <div className="cd-auto-seg cd-auto-active" />
              <div className="cd-auto-seg cd-auto-prev" />
              <div className="cd-auto-seg" />
              <div className="cd-auto-seg" />
              <div className="cd-auto-seg" />
            </div>
            <div className="cd-auto-flow kicker">音频 → 200ms → 推进</div>
          </div>
          <p className="cd-auto-desc serif-cn">
            一镜到底，不需要后期对轨
          </p>
        </div>
      </div>
    );
  }

  /* Step 7 — Use cases */
  return (
    <div className="cd-scene scene-pad">
      <div className="masthead">
        <span className="brand">Use Cases</span>
      </div>
      <hr className="rule" style={{ marginTop: "var(--space-5)" }} />

      <div className="cd-uses">
        <div className="cd-use-item">
          <span className="hero-num cd-use-num">01</span>
          <span className="serif-cn cd-use-label">公众号转 B 站视频</span>
        </div>
        <div className="cd-use-item">
          <span className="hero-num cd-use-num">02</span>
          <span className="serif-cn cd-use-label">产品演示与教程</span>
        </div>
        <div className="cd-use-item">
          <span className="hero-num cd-use-num">03</span>
          <span className="serif-cn cd-use-label">电影感路演 demo</span>
        </div>
      </div>
    </div>
  );
}
