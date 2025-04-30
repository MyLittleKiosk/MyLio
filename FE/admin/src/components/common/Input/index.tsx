import React from 'react';

interface InputProps {
  label?: string;
  id: string;
  placeholder: string;
  type: string;
  value: string;
  className?: string;
  error?: boolean;
  disabled?: boolean;
  onChange: (e: React.ChangeEvent<HTMLInputElement>) => void;
}

const Input = ({
  label,
  id,
  placeholder,
  type,
  value,
  onChange,
  className,
  error = false,
  disabled = false,
}: InputProps) => {
  return (
    <div className='flex gap-2 items-center'>
      {label && <label className='text-md font-preSemiBold'>{label}</label>}
      <input
        id={id}
        placeholder={placeholder}
        type={type}
        value={value}
        onChange={onChange}
        className={`${className} ${error ? 'border-2 border-error' : 'border border-subContent'} rounded-md p-2 font-preRegular`}
        disabled={disabled}
      />
    </div>
  );
};

export default Input;
