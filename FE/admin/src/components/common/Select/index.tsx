import clsx from 'clsx';
import React, { SelectHTMLAttributes } from 'react';

type SelectProps<T> = SelectHTMLAttributes<HTMLSelectElement> & {
  label?: string;
  options: T[];
  selected: T | null;
  placeholder: string;
  className?: string;
  error?: boolean;
  getOptionLabel: (option: T) => string;
  getOptionValue: (option: T) => string;
};

const Select = <T,>({
  options,
  label,
  selected,
  placeholder,
  className,
  error = false,
  getOptionLabel,
  getOptionValue,
  ...props
}: SelectProps<T>) => {
  const selectElement = (
    <select
      className={clsx(
        'w-full rounded-md p-2 font-preRegular',
        error ? 'border-2 border-error' : 'border border-subContent',
        className
      )}
      value={selected ? getOptionValue(selected) : ''}
      {...props}
    >
      <option value={placeholder} className='font-preRegular'>
        {placeholder}
      </option>
      {options.map((option, index) => (
        <option key={index} value={getOptionValue(option)}>
          {getOptionLabel(option)}
        </option>
      ))}
    </select>
  );
  return (
    <div className={`${className} flex items-center`}>
      {label ? (
        <label className='flex gap-4 items-center w-full'>
          <span className='min-w-[80px] max-w-[100px] text-md font-preSemiBold whitespace-nowrap'>
            {label}
          </span>
          {selectElement}
        </label>
      ) : (
        selectElement
      )}
    </div>
  );
};

export default Select;
