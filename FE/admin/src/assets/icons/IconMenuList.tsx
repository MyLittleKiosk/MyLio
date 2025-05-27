import { iconProps } from '@/types/iconProps';

const IconMenuList = ({ width = 20, height = 20 }: iconProps) => {
  return (
    <svg
      width={width}
      height={height}
      viewBox='0 0 20 20'
      fill='none'
      xmlns='http://www.w3.org/2000/svg'
    >
      <path
        d='M3.33203 10H16.6654'
        stroke='black'
        strokeWidth='1.66667'
        strokeLinecap='round'
        strokeLinejoin='round'
      />
      <path
        d='M3.33203 5H16.6654'
        stroke='black'
        strokeWidth='1.66667'
        strokeLinecap='round'
        strokeLinejoin='round'
      />
      <path
        d='M3.33203 15H16.6654'
        stroke='black'
        strokeWidth='1.66667'
        strokeLinecap='round'
        strokeLinejoin='round'
      />
    </svg>
  );
};

export default IconMenuList;
