# 音频同步方案：用真实时长驱动自动翻页

## 问题

当前 auto 模式靠 Audio 的 `ended` 事件驱动翻页。当浏览器 Audio 播放性能下降（变慢/卡顿），翻页也跟着延迟，体验越来越差。

## 思路

**音频继续播放给人听，但自动翻页的时钟改用音频的真实时长（`audio.duration`）驱动，不依赖 `ended` 事件。**

这样即使播放器实际播慢了，页面仍然在正确的时间点翻页 —— 视觉节奏不受音频卡顿影响。

## 方案

### 改动范围：仅 `useAudioPlayer.ts`

当前流程：
```
加载音频 → play() → ended 事件 → 翻页
```

新流程：
```
加载音频 → loadedmetadata（获得 duration）→ play() → duration ± 200ms → 翻页
                   ↓
             同时 ended 事件作为兜底
```

### 具体实现

```typescript
if (src) {
  audio.src = src;

  const onMeta = () => {
    const durMs = (audio.duration || 3) * 1000;  // 秒 → 毫秒
    advanceAfter(durMs + trailMs);
  };

  // 主时钟：loadedmetadata 获取真实时长后启动计时器
  audio.addEventListener("loadedmetadata", onMeta, { once: true });
  // 兜底：ended 事件（万一 timer 未触发）
  const onEnded = () => advanceAfter(trailMs);

  audio.play();
}
```

### 为什么 `loadedmetadata` 可靠

- 设 `audio.src` 后浏览器从文件头读取时长信息
- 对本地 mp3 文件，loadedmetadata 在几毫秒内触发
- 即使播放卡顿，计时器不受影响
- `{ once: true }` 确保每次换源只绑定一次

### 边界情况

| 场景 | 处理 |
|------|------|
| loadedmetadata 不触发 | ended 兜底 |
| 两者都触发 | `advanced` 标志位防重复翻页（已有）|
| duration 拿不到（=NaN）| 回退到字数估时 |
| 无音频文件（silent step）| 字数估时不变 |

### 不动的东西

- 不新增文件、不新增依赖
- 不改 App.tsx / Stage.tsx / chapters.ts
- 不改三种模式（manual / audio / auto）的逻辑
- 不改接口签名
