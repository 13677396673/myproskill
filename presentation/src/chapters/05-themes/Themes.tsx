import type { ChapterStepProps } from "../../registry/types";
import "./Themes.css";

export default function Themes({ step }: ChapterStepProps) {
  if (step === 0) {
    return (
      <div className="th-scene scene-pad">
        <div className="masthead"><span className="brand">Themes</span><span className="issue">主题系统</span></div>
        <hr className="rule" style={{ marginTop: "var(--space-5)" }} />
        <div className="th-cover-body">
          <div className="kicker">二十三套独立设计 DNA</div>
          <h1 className="th-cover-h"><span className="serif-cn">不是换</span><span className="serif-it th-accent">颜色</span><br /><span className="serif-cn">是完整的设计</span><span className="serif-it th-accent">签名</span></h1>
        </div>
      </div>
    );
  }
  if (step === 1) {
    return (
      <div className="th-scene th-center-scene">
        <div className="th-center-layout">
          <div className="kicker" style={{ marginBottom: "var(--space-4)" }}>设计签名</div>
          <div className="th-sig-grid">
            <div className="th-sig-item"><span className="th-sig-icon" style={{ borderTop: "3px solid var(--accent)" }} /><span className="th-sig-label serif-cn">线条性格</span></div>
            <div className="th-sig-item"><span className="th-sig-icon" style={{ borderRadius: "50%", border: "2px solid var(--accent)" }} /><span className="th-sig-label serif-cn">圆角哲学</span></div>
            <div className="th-sig-item"><span className="th-sig-icon" style={{ background: "var(--accent)", borderRadius: "2px" }} /><span className="th-sig-label serif-cn">装饰签名</span></div>
            <div className="th-sig-item"><span className="th-sig-icon" style={{ borderBottom: "3px dotted var(--accent)" }} /><span className="th-sig-label serif-cn">动效基线</span></div>
          </div>
        </div>
      </div>
    );
  }
  if (step === 2) {
    return (
      <div className="th-scene scene-pad">
        <div className="th-theme-hdr"><span className="hero-num th-theme-num">01</span><span className="kicker">Midnight Press</span></div>
        <hr className="rule" style={{ marginTop: "var(--space-5)" }} />
        <div className="th-demo">
          <div className="th-preview th-preview-dark">
            <span className="serif-it th-preview-label">咖啡底 · 火热橙</span>
            <span className="kicker th-preview-sub">衬线字体 · 慢速电影感</span>
          </div>
        </div>
      </div>
    );
  }
  if (step === 3) {
    return (
      <div className="th-scene scene-pad">
        <div className="th-theme-hdr"><span className="hero-num th-theme-num">02</span><span className="kicker">Newsroom</span></div>
        <hr className="rule" style={{ marginTop: "var(--space-5)" }} />
        <div className="th-demo">
          <div className="th-preview th-preview-light">
            <span className="serif-cn th-preview-label">报纸奶油 · 墨黑衬线</span>
            <span className="kicker th-preview-sub">旗红标题 · 零圆角</span>
          </div>
        </div>
      </div>
    );
  }
  if (step === 4) {
    return (
      <div className="th-scene scene-pad">
        <div className="th-theme-hdr"><span className="hero-num th-theme-num">03</span><span className="kicker">Terminal Green</span></div>
        <hr className="rule" style={{ marginTop: "var(--space-5)" }} />
        <div className="th-demo">
          <div className="th-preview th-preview-terminal">
            <span className="th-preview-terminal-text serif-cn">纯黑 · 等宽字体</span>
            <span className="kicker th-preview-sub">CRT 扫描线 · 线性动效</span>
          </div>
        </div>
      </div>
    );
  }
  if (step === 5) {
    return (
      <div className="th-scene th-center-scene">
        <div className="th-center-layout">
          <div className="kicker" style={{ marginBottom: "var(--space-4)" }}>更多主题</div>
          <div className="th-more-list">
            <span className="th-more-tag">粉笔花园</span>
            <span className="th-more-tag">包豪斯</span>
            <span className="th-more-tag">双拼画布</span>
            <span className="th-more-tag">蓝图</span>
            <span className="th-more-tag">黑白印刷</span>
            <span className="th-more-tag">复古编辑</span>
          </div>
        </div>
      </div>
    );
  }
  if (step === 6) {
    return (
      <div className="th-scene th-center-scene">
        <div className="th-center-layout">
          <div className="kicker" style={{ marginBottom: "var(--space-4)" }}>CSS Token</div>
          <h2 className="th-token-h"><span className="hero-num th-token-num">25~35</span><span className="serif-cn"> 个 token</span></h2>
          <div className="th-token-sub serif-cn">颜色 · 字体 · 圆角 · 阴影 · 装饰</div>
        </div>
      </div>
    );
  }
  return (
    <div className="th-scene th-center-scene">
      <div className="th-center-layout">
        <div className="kicker" style={{ marginBottom: "var(--space-4)" }}>切换主题</div>
        <div className="th-switch-demo">
          <span className="th-switch-cmd">cp themes/&lt;id&gt;/tokens.css src/styles/</span>
        </div>
        <div className="th-switch-sub serif-cn">一条命令 · 章节代码不动</div>
      </div>
    </div>
  );
}
