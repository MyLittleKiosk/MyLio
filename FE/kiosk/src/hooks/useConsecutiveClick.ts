import { useRef } from 'react';

interface UseConsecutiveClickProps {
  requiredClicks?: number;
  timeWindow?: number;
  onSuccess: () => void;
  isAdmin?: boolean;
}

const useConsecutiveClick = ({
  requiredClicks = 5,
  timeWindow = 2000,
  onSuccess,
}: UseConsecutiveClickProps) => {
  const clickCountRef = useRef<number>(0);
  const lastClickTimeRef = useRef<number>(0);

  const handleClick = () => {
    const now = Date.now();
    if (now - lastClickTimeRef.current > timeWindow) {
      clickCountRef.current = 0;
    }
    clickCountRef.current++;
    lastClickTimeRef.current = now;

    if (clickCountRef.current >= requiredClicks) {
      onSuccess();
      clickCountRef.current = 0;
    }
  };

  return handleClick;
};

export default useConsecutiveClick;
