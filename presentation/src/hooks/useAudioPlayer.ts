import { useEffect, useRef } from "react";

export type PlaybackMode = "manual" | "audio" | "auto";

interface Options {
  src: string | null;
  mode: PlaybackMode;
  trailMs?: number;
  estimateFallbackMs?: number;
  onAutoAdvance: () => void;
  autoStarted: boolean;
}

/**
 * Per-step audio playback.
 *
 * Reuses a single `<audio>` element across all steps to avoid browser
 * Audio-object accumulation that causes playback speed degradation.
 *
 * In `auto` mode:
 *   • Primary clock: `loadedmetadata` → `audio.duration` (browser-read
 *     from file header, immune to playback slowdown/stutter).
 *   • Fallback: `ended` event fires the same advanceAfter, so even if
 *     duration is unavailable the audio still drives the timeline.
 *   • No audio / error → `estimateFallbackMs`.
 */
export function useAudioPlayer({
  src,
  mode,
  trailMs = 200,
  estimateFallbackMs = 1500,
  onAutoAdvance,
  autoStarted,
}: Options) {
  const audioRef = useRef<HTMLAudioElement | null>(null);
  const onAdvanceRef = useRef(onAutoAdvance);
  onAdvanceRef.current = onAutoAdvance;

  useEffect(() => {
    if (mode === "manual") return;
    if (mode === "auto" && !autoStarted) return;

    let advanced = false;
    let timer: number | null = null;

    const advanceAfter = (ms: number) => {
      if (mode !== "auto" || advanced) return;
      timer = window.setTimeout(() => {
        if (advanced) return;
        advanced = true;
        onAdvanceRef.current();
      }, Math.max(0, ms));
    };

    // Create the persistent Audio element once
    if (!audioRef.current) {
      audioRef.current = new Audio();
      audioRef.current.preload = "auto";
    }
    const audio = audioRef.current;

    audio.playbackRate = 1.0;

    if (src) {
      audio.src = src;

      // Primary clock: use audio's real duration read from file header.
      // This is immune to playback slowdown because it's a property of
      // the file, not of real-time playback performance.
      const onMeta = () => {
        const durMs =
          audio.duration && isFinite(audio.duration)
            ? audio.duration * 1000
            : estimateFallbackMs;
        advanceAfter(durMs + trailMs);
      };

      // Fallback: ended event fires the same guard
      const onEnded = () => advanceAfter(trailMs);

      const onError = () => {
        if (mode === "auto") advanceAfter(estimateFallbackMs);
      };

      audio.addEventListener("loadedmetadata", onMeta, { once: true });
      audio.addEventListener("ended", onEnded);
      audio.addEventListener("error", onError);

      audio.play().catch((err) => {
        console.warn("audio play failed:", err);
        if (mode === "auto") advanceAfter(estimateFallbackMs);
      });

      return () => {
        advanced = true;
        if (timer != null) clearTimeout(timer);
        audio.pause();
        audio.removeEventListener("ended", onEnded);
        audio.removeEventListener("error", onError);
        // onMeta is auto-removed by { once: true }
      };
    }

    // No audio source — use estimate in auto mode
    if (mode === "auto") advanceAfter(estimateFallbackMs);

    return () => {
      advanced = true;
      if (timer != null) clearTimeout(timer);
    };
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [src, mode, autoStarted]);
}
