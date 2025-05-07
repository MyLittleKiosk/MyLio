import React from 'react';

interface ButtonProps {
  buttonType: 'button' | 'submit' | 'reset';
  text?: string;
  cancel?: boolean;
  disabled?: boolean;
  error?: boolean;
  className?: string;
  icon?: React.ReactNode;
  onClick?: () => void;
  onKeyDown?: (e: React.KeyboardEvent<HTMLButtonElement>) => void;
}

const Button = ({
  buttonType,
  text,
  disabled = false,
  cancel = false,
  error = false,
  className,
  icon,
  onClick,
  onKeyDown,
}: ButtonProps) => {
  return (
    <button
      type={buttonType}
      className={`${className} ${error && 'bg-error text-white'} ${disabled && 'bg-subContent text-white pointer-events-none'} ${cancel && 'bg-subContent text-black'} flex items-center gap-2 bg-primary text-white rounded-md px-4 py-2 font-preRegular hover:opacity-70`}
      disabled={disabled}
      onClick={onClick}
      onKeyDown={onKeyDown}
    >
      {icon}
      {text}
    </button>
  );
};

export default Button;
