import React from 'react';

interface SelectProps {
  label?: string;
  options: OptionType[];
  selected: string;
  placeholder: string;
  className?: string;
  error?: boolean;
  disabled?: boolean;
  onChange: (e: React.ChangeEvent<HTMLSelectElement>) => void;
}

interface OptionType {
  key: string;
  value: string;
}

const Select = ({
  options,
  label,
  selected,
  placeholder,
  className,
  error = false,
  disabled = false,
  onChange,
}: SelectProps) => {
  return (
    <div className={`${className}`}>
      {label && (
        <label className='text-md font-preSemiBold flex gap-2 items-center'>
          {label}
          <select
            className={`${error ? 'border-2 border-error' : 'border border-subContent'} rounded-md p-2 font-preRegular`}
            onChange={onChange}
            value={selected}
            disabled={disabled}
          >
            <option value='' className='font-preRegular'>
              {placeholder}
            </option>
            {options.map((option) => (
              <option key={option.key}>{option.value}</option>
            ))}
          </select>
        </label>
      )}
    </div>
  );
};

export default Select;
