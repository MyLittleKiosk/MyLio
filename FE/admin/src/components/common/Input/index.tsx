import clsx from 'clsx';
import React from 'react';
interface InputProps {
  label?: string;
  inputId: string;
  placeholder: string;
  inputType: string;
  inputValue: string | number;
  className?: string;
  inputClassName?: string;
  error?: boolean;
  errorMessage?: string;
  disabled?: boolean;
  minDate?: string;
  maxDate?: string;
  onChange: (e: React.ChangeEvent<HTMLInputElement>) => void;
  onKeyDown?: (e: React.KeyboardEvent<HTMLInputElement>) => void;
}

const Input = ({
  label,
  inputId,
  placeholder,
  inputType,
  inputValue,
  onChange,
  className,
  inputClassName,
  error = false,
  errorMessage,
  disabled = false,
  onKeyDown,
  minDate,
  maxDate,
}: InputProps) => {
  const inputElement = (
    <div className='w-full'>
      <input
        id={inputId}
        placeholder={placeholder}
        type={inputType}
        value={inputValue}
        onChange={onChange}
        className={clsx(
          'rounded-md p-2 font-preRegular h-[40px] box-border',
          inputClassName || 'w-full',
          error
            ? 'border-2 border-error focus:ring-1 focus:ring-error focus:ring-inset focus:outline-none'
            : 'border border-subContent'
        )}
        disabled={disabled}
        onKeyDown={onKeyDown}
        min={minDate}
        max={maxDate}
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
        <label className='flex gap-4 items-start w-full'>
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
