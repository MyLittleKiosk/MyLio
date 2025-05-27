import { useRef } from 'react';

interface UseAdminConsecutiveClickProps {
  onSuccess: () => void;
}

const useAdminConsecutiveClick = ({
  onSuccess,
}: UseAdminConsecutiveClickProps) => {
  const clickCountRef = useRef<number>(0);
  const lastClickTimeRef = useRef<number>(0);

  const handleClick = () => {
    const now = Date.now();
    if (now - lastClickTimeRef.current > 2000) {
      clickCountRef.current = 0;
    }
    clickCountRef.current++;
    lastClickTimeRef.current = now;

    if (clickCountRef.current >= 5) {
      onSuccess();
      clickCountRef.current = 0;
    }
  };

  return handleClick;
};

export default useAdminConsecutiveClick;
