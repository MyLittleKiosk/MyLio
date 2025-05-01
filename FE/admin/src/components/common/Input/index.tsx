import React from 'react';

interface InputProps {
  label?: string;
  inputId: string;
  placeholder: string;
  inputType: string;
  inputValue: string;
  className?: string;
  error?: boolean;
  disabled?: boolean;
  onChange: (e: React.ChangeEvent<HTMLInputElement>) => void;
}

const Input = ({
  label,
  inputId,
  placeholder,
  inputType,
  inputValue,
  onChange,
  className,
  error = false,
  disabled = false,
}: InputProps) => {
  return (
    <div className={`${className} flex items-center`}>
      {label ? (
        <label className='flex gap-2 items-center w-full'>
          <span className='text-md font-preSemiBold whitespace-nowrap'>
            {label}
          </span>
          <input
            id={inputId}
            placeholder={placeholder}
            type={inputType}
            value={inputValue}
            onChange={onChange}
            className={`${
              error ? 'border-2 border-error' : 'border border-subContent'
            } rounded-md p-2 font-preRegular w-full`}
            disabled={disabled}
          />
        </label>
      ) : (
        <input
          id={inputId}
          placeholder={placeholder}
          type={inputType}
          value={inputValue}
          onChange={onChange}
          className={`${
            error ? 'border-2 border-error' : 'border border-subContent'
          } rounded-md p-2 font-preRegular w-full`}
          disabled={disabled}
        />
      )}
    </div>
  );
};

export default Input;
