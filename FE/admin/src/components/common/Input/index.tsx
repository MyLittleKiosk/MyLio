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
}: InputProps) => {
  const inputElement = (
    <div>
      <input
        id={inputId}
        placeholder={placeholder}
        type={inputType}
        value={inputValue}
        onChange={onChange}
        className={`${
          error ? 'border-2 border-error' : 'border border-subContent'
        } rounded-md p-2 font-preRegular h-[40px] box-border ${inputClassName || 'w-full'}`}
        disabled={disabled}
        onKeyDown={onKeyDown}
      />
      {error && (
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
