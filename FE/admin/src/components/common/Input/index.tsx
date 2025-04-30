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
    <div className={`${className}`}>
      {label && (
        <label className='text-md font-preSemiBold flex gap-2 items-center'>
          {label}

          <input
            id={inputId}
            placeholder={placeholder}
            type={inputType}
            value={inputValue}
            onChange={onChange}
            className={` ${error ? 'border-2 border-error' : 'border border-subContent'} rounded-md p-2 font-preRegular`}
            disabled={disabled}
          />
        </label>
      )}
    </div>
  );
};

export default Input;
