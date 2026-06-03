import type { ChapterStepProps } from "../../registry/types";
import "./Ending.css";

export default function Ending({ step }: ChapterStepProps) {
  if (step === 0) {
    return (
      <div className="en-scene scene-pad">
        <div className="masthead"><span className="brand">Closing</span><span className="issue">尾声</span></div>
        <hr className="rule" style={{ marginTop: "var(--space-5)" }} />
        <div className="en-cover-body">
          <div className="kicker">四点心得</div>
          <h1 className="en-cover-h">
            <span className="serif-it en-accent">Agent Skill</span>
            <br />
            <span className="serif-cn">设计心法</span>
          </h1>
        </div>
      </div>
    );
  }
  if (step === 1) {
    return (
      <div className="en-scene en-center-scene">
        <div className="en-center-layout">
          <div className="en-num-wrap">
            <span className="hero-num en-num">01</span>
          </div>
          <h2 className="en-point-h">
            <span className="serif-cn">Checkpoint 设计</span>
            <br />
            <span className="serif-it en-accent">比提示词重要</span>
          </h2>
          <div className="en-point-sub serif-cn">什么时候停、怎么对齐、谁决策</div>
        </div>
      </div>
    );
  }
  if (step === 2) {
    return (
      <div className="en-scene en-center-scene">
        <div className="en-center-layout">
          <div className="en-num-wrap">
            <span className="hero-num en-num">02</span>
          </div>
          <h2 className="en-point-h">
            <span className="serif-cn">先定</span>
            <span className="serif-it en-accent">原则</span>
            <br />
            <span className="serif-cn">再写代码</span>
          </h2>
          <div className="en-point-sub serif-cn">从原则往回推理，不是从模板出发</div>
        </div>
      </div>
    );
  }
  if (step === 3) {
    return (
      <div className="en-scene en-center-scene">
        <div className="en-center-layout">
          <div className="en-num-wrap">
            <span className="hero-num en-num">03</span>
          </div>
          <h2 className="en-point-h">
            <span className="serif-cn">去 AI 味</span>
            <span className="serif-it en-accent">不是降质</span>
          </h2>
          <div className="en-point-sub serif-cn">朗诵换聊天，信息量一个不少</div>
        </div>
      </div>
    );
  }
  if (step === 4) {
    return (
      <div className="en-scene en-center-scene">
        <div className="en-center-layout">
          <div className="en-num-wrap">
            <span className="hero-num en-num">04</span>
          </div>
          <h2 className="en-point-h">
            <span className="serif-cn">主题系统</span>
            <br />
            <span className="serif-it en-accent">换的是签名</span>
          </h2>
          <div className="en-point-sub serif-cn">不是颜色</div>
        </div>
      </div>
    );
  }
  return (
    <div className="en-scene en-center-scene">
      <div className="en-center-layout">
        <div className="kicker" style={{ marginBottom: "var(--space-4)" }}>开源</div>
        <h2 className="en-final-h">
          <span className="serif-cn">去 GitHub 搜</span>
          <br />
          <span className="serif-it en-accent">web-video-presentation</span>
        </h2>
        <div className="en-final-sub serif-cn">欢迎来交流 · 下期见</div>
      </div>
    </div>
  );
}
