import React from 'react';

interface SelectProps<T> {
  label?: string;
  options: T[];
  selected: T | null;
  placeholder: string;
  className?: string;
  error?: boolean;
  disabled?: boolean;
  onChange: (e: React.ChangeEvent<HTMLSelectElement>) => void;
  getOptionLabel: (option: T) => string;
  getOptionValue: (option: T) => string;
}

const Select = <T,>({
  options,
  label,
  selected,
  placeholder,
  className,
  error = false,
  disabled = false,
  onChange,
  getOptionLabel,
  getOptionValue,
}: SelectProps<T>) => {
  return (
    <div className={`${className} flex items-center`}>
      {label ? (
        <label className='flex gap-2 items-center w-full'>
          <span className='text-md font-preSemiBold whitespace-nowrap'>
            {label}
          </span>
          <select
            className={`w-full ${error ? 'border-2 border-error' : 'border border-subContent'} rounded-md p-2 font-preRegular`}
            onChange={onChange}
            value={selected ? getOptionValue(selected) : ''}
            disabled={disabled}
          >
            <option value='' className='font-preRegular'>
              {placeholder}
            </option>
            {options.map((option, index) => (
              <option key={index} value={getOptionValue(option)}>
                {getOptionLabel(option)}
              </option>
            ))}
          </select>
        </label>
      ) : (
        <select
          className={`w-full ${error ? 'border-2 border-error' : 'border border-subContent'} rounded-md p-2 font-preRegular`}
          onChange={onChange}
          value={selected ? getOptionValue(selected) : ''}
          disabled={disabled}
        >
          <option value='' className='font-preRegular'>
            {placeholder}
          </option>
          {options.map((option, index) => (
            <option key={index} value={getOptionValue(option)}>
              {getOptionLabel(option)}
            </option>
          ))}
        </select>
      )}
    </div>
  );
};

export default Select;
