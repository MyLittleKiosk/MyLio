import React from 'react';

interface InputProps {
  label?: string;
  inputId: string;
  placeholder: string;
  inputType: string;
  inputValue: string | number;
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
  const inputElement = (
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
  );

  return (
    <div className={`${className} flex items-center`}>
      {label ? (
        <label className='flex gap-4 items-center w-full'>
          <span className='min-w-[80px] max-w-[100px] text-md font-preSemiBold whitespace-nowrap'>
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
