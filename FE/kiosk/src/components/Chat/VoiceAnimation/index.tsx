import audioStore from '@/stores/audioStore';
import { useEffect, useRef, useMemo, useState } from 'react';

const BAR_COUNT = 20;
const MIN_HEIGHT = 0.2; // 최소 높이 비율
const UPDATE_INTERVAL = 1000 / 30; // 30fps

const VoiceAnimation = () => {
  const isRecording = audioStore((s) => s.isRecording);
  const volume = audioStore((s) => s.volume);
  const [heights, setHeights] = useState<number[]>(
    Array(BAR_COUNT).fill(MIN_HEIGHT)
  );

  const containerRef = useRef<HTMLDivElement>(null);
  const barRefs = useRef<Array<HTMLDivElement | null>>(
    Array(BAR_COUNT).fill(0)
  );
  const maxVolRef = useRef<number>(10);
  const lastUpdateRef = useRef<number>(0);

  // 바 요소들을 미리 생성
  const bars = useMemo(
    () =>
      Array.from({ length: BAR_COUNT }).map((_, idx) => (
        <div
          key={idx}
          ref={(el: HTMLDivElement | null) => {
            barRefs.current[idx] = el;
          }}
          className='w-0.5 flex-1 bg-jihyegra transition-all duration-100'
          style={{ height: `${heights[idx] * 100}%` }}
        />
      )),
    [heights]
  );

  useEffect(() => {
    let rafId: number;

    const update = (timestamp: number) => {
      if (timestamp - lastUpdateRef.current < UPDATE_INTERVAL) {
        rafId = requestAnimationFrame(update);
        return;
      }
      lastUpdateRef.current = timestamp;

      if (isRecording && volume > 0) {
        maxVolRef.current = Math.max(maxVolRef.current, volume);
        const normVol = maxVolRef.current > 0 ? volume / maxVolRef.current : 0;

        // 모든 바의 높이를 한 번에 계산
        const newHeights = heights.map(() => {
          const random = Math.random() * 0.5 + 0.7;
          const h = MIN_HEIGHT + normVol * (1 - MIN_HEIGHT) * random;
          return Math.min(1, Math.max(MIN_HEIGHT, h));
        });

        setHeights(newHeights);
      } else {
        setHeights(Array(BAR_COUNT).fill(MIN_HEIGHT));
      }

      rafId = requestAnimationFrame(update);
    };

    rafId = requestAnimationFrame(update);
    return () => cancelAnimationFrame(rafId);
  }, [isRecording, volume, heights]);

  return (
    <div
      ref={containerRef}
      className='flex items-end gap-1 h-16 overflow-hidden'
    >
      {bars}
    </div>
  );
};

export default VoiceAnimation;
