import type { ChapterStepProps } from "../../registry/types";
import "./TechArch.css";

export default function TechArch({ step }: ChapterStepProps) {
  if (step === 0) {
    return (
      <div className="ta-scene scene-pad">
        <div className="masthead"><span className="brand">Architecture</span><span className="issue">技术架构</span></div>
        <hr className="rule" style={{ marginTop: "var(--space-5)" }} />
        <div className="ta-cover-body">
          <div className="kicker">三个关键设计</div>
          <h1 className="ta-cover-h"><span className="serif-cn">技术架构</span></h1>
          <div className="ta-teasers">
            <span className="ta-teaser">step 游标</span>
            <span className="ta-teaser">Auto 模式</span>
            <span className="ta-teaser">Provider-agnostic</span>
          </div>
        </div>
      </div>
    );
  }
  if (step === 1) {
    return (
      <div className="ta-scene scene-pad">
        <div className="ta-hdr"><span className="hero-num ta-hdr-num">01</span><span className="kicker">step 游标模型</span></div>
        <hr className="rule" style={{ marginTop: "var(--space-5)" }} />
        <div className="ta-demo">
          <div className="ta-cursor-flow">
            <div className="ta-cursor-item ta-cursor-active"><span className="ta-cursor-step">ch 1</span></div>
            <span className="ta-cursor-arrow serif-it">→</span>
            <div className="ta-cursor-item"><span className="ta-cursor-step">ch 2</span></div>
            <span className="ta-cursor-arrow serif-it">→</span>
            <div className="ta-cursor-item"><span className="ta-cursor-step">ch 3</span></div>
          </div>
          <div className="ta-caption serif-cn">useStepper + localStorage 持久化</div>
        </div>
      </div>
    );
  }
  if (step === 2) {
    return (
      <div className="ta-scene ta-center-scene">
        <div className="ta-center-layout">
          <div className="kicker" style={{ marginBottom: "var(--space-4)" }}>纯函数</div>
          <h2 className="ta-feat-h"><span className="serif-cn">没有 </span><span className="serif-it ta-accent">useEffect</span></h2>
          <div className="ta-feat-sub serif-cn">全部 CSS keyframes 声明式完成</div>
        </div>
      </div>
    );
  }
  if (step === 3) {
    return (
      <div className="ta-scene ta-center-scene">
        <div className="ta-center-layout">
          <div className="kicker" style={{ marginBottom: "var(--space-4)" }}>五处永不漂</div>
          <div className="ta-sync-list">
            <div className="ta-sync-item kicker">script.md</div>
            <div className="ta-sync-arrow">↓</div>
            <div className="ta-sync-item kicker">outline.md</div>
            <div className="ta-sync-arrow">↓</div>
            <div className="ta-sync-item kicker">章节代码</div>
            <div className="ta-sync-arrow">↓</div>
            <div className="ta-sync-item kicker">chapters.ts</div>
            <div className="ta-sync-arrow">↓</div>
            <div className="ta-sync-item kicker">音频文件</div>
          </div>
        </div>
      </div>
    );
  }
  if (step === 4) {
    return (
      <div className="ta-scene ta-center-scene">
        <div className="ta-center-layout">
          <div className="kicker" style={{ marginBottom: "var(--space-4)" }}>唯一真相源</div>
          <div className="ta-source-block">
            <span className="ta-source-file">narrations.ts</span>
          </div>
          <div className="ta-source-sub serif-cn">所有数据的源头</div>
        </div>
      </div>
    );
  }
  if (step === 5) {
    return (
      <div className="ta-scene scene-pad">
        <div className="ta-hdr"><span className="hero-num ta-hdr-num">02</span><span className="kicker">Auto 模式</span></div>
        <hr className="rule" style={{ marginTop: "var(--space-5)" }} />
        <div className="ta-demo">
          <div className="ta-auto-visual">
            <div className="ta-auto-segments">
              <div className="ta-auto-seg ta-auto-seg-active" />
              <div className="ta-auto-seg" />
              <div className="ta-auto-seg" />
              <div className="ta-auto-seg" />
            </div>
            <div className="ta-auto-info">
              <span className="kicker">音频 → 200ms → 推进</span>
            </div>
          </div>
        </div>
      </div>
    );
  }
  if (step === 6) {
    return (
      <div className="ta-scene ta-center-scene">
        <div className="ta-center-layout">
          <div className="kicker" style={{ marginBottom: "var(--space-4)" }}>参数驱动</div>
          <h2 className="ta-feat-h"><span className="serif-it ta-accent">?auto=1</span></h2>
          <div className="ta-feat-sub serif-cn">加个参数就能全自动播放</div>
        </div>
      </div>
    );
  }
  if (step === 7) {
    return (
      <div className="ta-scene ta-center-scene">
        <div className="ta-center-layout">
          <div className="kicker" style={{ marginBottom: "var(--space-4)" }}>硬约束</div>
          <h2 className="ta-feat-h"><span className="serif-cn">动画比口播长</span><br /><span className="serif-it ta-accent">会被切断</span></h2>
          <div className="ta-feat-sub serif-cn">倒逼动画服务于口播节奏</div>
        </div>
      </div>
    );
  }
  if (step === 8) {
    return (
      <div className="ta-scene scene-pad">
        <div className="ta-hdr"><span className="hero-num ta-hdr-num">03</span><span className="kicker">Provider-agnostic</span></div>
        <hr className="rule" style={{ marginTop: "var(--space-5)" }} />
        <div className="ta-demo">
          <div className="ta-providers">
            <div className="ta-provider">
              <span className="ta-provider-name kicker">minimax</span>
            </div>
            <div className="ta-provider">
              <span className="ta-provider-name kicker">openai</span>
            </div>
            <div className="ta-provider">
              <span className="ta-provider-name kicker">mimo</span>
            </div>
          </div>
          <div className="ta-caption serif-cn">每个后端一个脚本，三函数契约</div>
        </div>
      </div>
    );
  }
  return (
    <div className="ta-scene ta-center-scene">
      <div className="ta-center-layout">
        <div className="kicker" style={{ marginBottom: "var(--space-4)" }}>可扩展</div>
        <h2 className="ta-feat-h"><span className="serif-cn">照着 </span><span className="serif-it ta-accent">README</span><span className="serif-cn"> 改</span></h2>
        <div className="ta-feat-sub serif-cn">ElevenLabs · Azure · 任意 TTS</div>
      </div>
    </div>
  );
}
