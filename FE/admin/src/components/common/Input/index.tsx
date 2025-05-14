import clsx from 'clsx';
import React, { InputHTMLAttributes } from 'react';

type InputProps = InputHTMLAttributes<HTMLInputElement> & {
  label?: string;
  error?: boolean;
  errorMessage?: string;
  minDate?: string;
  maxDate?: string;
  className?: string;
  inputClassName?: string;
};

const Input = ({
  label,
  inputClassName,
  error = false,
  errorMessage,
  minDate,
  maxDate,
  className,
  ...props
}: InputProps) => {
  const inputElement = (
    <div className='w-full'>
      <input
        className={clsx(
          'rounded-md p-2 font-preRegular h-[40px] box-border',
          inputClassName || 'w-full',
          error
            ? 'border-2 border-error focus:ring-1 focus:ring-error focus:ring-inset focus:outline-none'
            : 'border border-subContent'
        )}
        min={minDate}
        max={maxDate}
        {...props}
      />
      {errorMessage && (
        <span className='text-error text-sm font-preMedium'>
          {errorMessage}
        </span>
      )}
    </div>
  );

  return (
    <div className={`flex items-center ${className || ''}`}>
      {label ? (
        <label className='flex gap-4 items-center w-full'>
          <span className='w-[10%] min-w-[80px] max-w-[100px] text-md font-preSemiBold whitespace-wrap break-keep'>
            {label}
          </span>
          {inputElement}
        </label>
      ) : (
        inputElement
      )}
    </div>
  );
};

export default Input;
