import React, { ButtonHTMLAttributes, useRef, useState } from 'react';

type ButtonSize = 'small' | 'medium' | 'large';

interface ButtonProps extends ButtonHTMLAttributes<HTMLButtonElement> {
  content: string;
  size?: ButtonSize;
  className?: string;
  isLoading?: boolean;
  disabled?: boolean;
  onClick?: (e: React.MouseEvent<HTMLButtonElement>) => void;
}

const Button = ({
  content,
  size = 'medium',
  className = '',
  isLoading = false,
  disabled,
  type = 'button',
  onClick,
  ...props
}: ButtonProps) => {
  const [ripples, setRipples] = useState<
    Array<{ x: number; y: number; id: number }>
  >([]);
  const buttonRef = useRef<HTMLButtonElement>(null);
  const rippleCount = useRef(0);

  const handleClick = (e: React.MouseEvent<HTMLButtonElement>) => {
    if (buttonRef.current) {
      const rect = buttonRef.current.getBoundingClientRect();
      const x = e.clientX - rect.left;
      const y = e.clientY - rect.top;

      const newRipple = {
        x,
        y,
        id: rippleCount.current++,
      };

      setRipples((prevRipples) => [...prevRipples, newRipple]);

      // 1초 후에 리플 효과 제거
      setTimeout(() => {
        setRipples((prevRipples) =>
          prevRipples.filter((ripple) => ripple.id !== newRipple.id)
        );
      }, 1000);
    }

    onClick?.(e);
  };

  const baseStyles = 'rounded-md font-preBold relative overflow-hidden';

  const variantStyles = {
    primary: 'bg-primary text-white hover:bg-primary/90',
  };

  const sizeStyles = {
    small: 'px-2 py-1 text-sm',
    medium: 'px-3 py-2',
    large: 'px-4 py-3 text-lg',
  };

  return (
    <button
      ref={buttonRef}
      type={type}
      className={`${baseStyles} ${variantStyles.primary} ${sizeStyles[size]} ${className} ${
        disabled || isLoading ? 'opacity-50 cursor-not-allowed' : ''
      }`}
      disabled={disabled || isLoading}
      onClick={handleClick}
      {...props}
    >
      {isLoading ? '잠시 기다려주세요' : content}
      {ripples.map((ripple) => (
        <span
          key={ripple.id}
          className='absolute bg-white/30 rounded-full animate-ripple'
          style={{
            left: ripple.x,
            top: ripple.y,
            transform: 'translate(-50%, -50%)',
          }}
        />
      ))}
    </button>
  );
};

export default Button;
