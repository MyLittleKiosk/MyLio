import { useEffect, useRef } from 'react';

interface Props {
  isRecording: boolean;
  volume: number;
}

const BAR_COUNT = 20;
const MIN_HEIGHT = 0.2; // 최소 높이 비율

function VoiceAnimation({ isRecording, volume }: Props) {
  const containerRef = useRef<HTMLDivElement>(null); // 애니메이션 박스의 DOM 요소 참조
  const barRefs = useRef<Array<HTMLDivElement | null>>(
    Array(BAR_COUNT).fill(0)
  ); // 각 바의 DOM 요소 참조
  const maxVolRef = useRef<number>(10); // 최대 볼륨 값 참조

  useEffect(() => {
    let rafId: number;

    const update = () => {
      if (isRecording) {
        maxVolRef.current = Math.max(maxVolRef.current, volume);
        const normVol = maxVolRef.current > 0 ? volume / maxVolRef.current : 0;

        barRefs.current.forEach((bar) => {
          if (!bar) return;
          const random = Math.random() * 0.5 + 0.7;
          const h = MIN_HEIGHT + normVol * (1 - MIN_HEIGHT) * random;
          bar.style.height = `${Math.min(1, Math.max(MIN_HEIGHT, h)) * 100}%`;
        });
      } else {
        barRefs.current.forEach((bar) => {
          if (!bar) return;
          bar.style.height = `${MIN_HEIGHT * 100}%`;
        });
      }
      rafId = requestAnimationFrame(update);
    };

    // requestAnimationFrame 함수: 브라우저의 리페인트 주기에 맞춰 애니메이션을 실행하는 함수
    rafId = requestAnimationFrame(update);
    return () => cancelAnimationFrame(rafId);
  }, [isRecording, volume]);

  return (
    <div
      ref={containerRef}
      className='flex items-end gap-1 h-16 overflow-hidden'
    >
      {Array.from({ length: BAR_COUNT }).map((_, idx) => (
        <div
          key={idx}
          ref={(el: HTMLDivElement | null) => {
            barRefs.current[idx] = el;
          }}
          className='w-0.5 flex-1 bg-jihyegra'
          style={{ height: `${MIN_HEIGHT * 100}%` }}
        />
      ))}
    </div>
  );
}

export default VoiceAnimation;
