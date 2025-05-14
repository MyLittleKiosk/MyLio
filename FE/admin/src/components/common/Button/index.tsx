import clsx from 'clsx';
import React, { ButtonHTMLAttributes } from 'react';

type ButtonProps = ButtonHTMLAttributes<HTMLButtonElement> & {
  text?: string;
  cancel?: boolean;
  disabled?: boolean;
  error?: boolean;
  className?: string;
  icon?: React.ReactNode;
};

const Button = ({
  text,
  disabled = false,
  cancel = false,
  error = false,
  className,
  icon,
  ...props
}: ButtonProps) => {
  return (
    <button
      className={clsx(
        'flex items-center justify-center gap-2 bg-primary text-white rounded-md px-4 py-2 font-preRegular hover:opacity-70',
        className,
        error && 'bg-error text-white',
        disabled && 'bg-subContent text-white pointer-events-none',
        cancel && 'bg-subContent text-black'
      )}
      disabled={disabled}
      {...props}
    >
      {icon}
      {text}
    </button>
  );
};

export default Button;
