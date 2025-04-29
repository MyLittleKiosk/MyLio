import { iconProps } from '@/types/iconProps';

const IconTrashCan = ({ width = 20, height = 20 }: iconProps) => {
  return (
    <svg
      width={width}
      height={height}
      viewBox='0 0 16 16'
      fill='none'
      xmlns='http://www.w3.org/2000/svg'
    >
      <path
        d='M2 4H14'
        stroke='#2E1314'
        strokeWidth='1.33333'
        strokeLinecap='round'
        strokeLinejoin='round'
      />
      <path
        d='M12.6654 4V13.3333C12.6654 14 11.9987 14.6667 11.332 14.6667H4.66536C3.9987 14.6667 3.33203 14 3.33203 13.3333V4'
        stroke='#2E1314'
        strokeWidth='1.33333'
        strokeLinecap='round'
        strokeLinejoin='round'
      />
      <path
        d='M5.33203 3.99992V2.66659C5.33203 1.99992 5.9987 1.33325 6.66536 1.33325H9.33203C9.9987 1.33325 10.6654 1.99992 10.6654 2.66659V3.99992'
        stroke='#2E1314'
        strokeWidth='1.33333'
        strokeLinecap='round'
        strokeLinejoin='round'
      />
    </svg>
  );
};

export default IconTrashCan;
