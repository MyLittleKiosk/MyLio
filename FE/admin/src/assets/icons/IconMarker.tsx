import { iconProps } from '@/types/iconProps';

const IconMarker = ({ width, height }: iconProps) => {
  return (
    <svg
      width={width}
      height={height}
      viewBox='0 0 14 14'
      fill='none'
      xmlns='http://www.w3.org/2000/svg'
    >
      <path
        d='M11.6654 5.83341C11.6654 9.33341 6.9987 12.8334 6.9987 12.8334C6.9987 12.8334 2.33203 9.33341 2.33203 5.83341C2.33203 4.59574 2.8237 3.40875 3.69887 2.53358C4.57404 1.65841 5.76102 1.16675 6.9987 1.16675C8.23637 1.16675 9.42336 1.65841 10.2985 2.53358C11.1737 3.40875 11.6654 4.59574 11.6654 5.83341Z'
        stroke='#71717A'
        strokeWidth='1.16667'
        strokeLinecap='round'
        strokeLinejoin='round'
      />
      <path
        d='M7 7.58325C7.9665 7.58325 8.75 6.79975 8.75 5.83325C8.75 4.86675 7.9665 4.08325 7 4.08325C6.0335 4.08325 5.25 4.86675 5.25 5.83325C5.25 6.79975 6.0335 7.58325 7 7.58325Z'
        stroke='#71717A'
        strokeWidth='1.16667'
        strokeLinecap='round'
        strokeLinejoin='round'
      />
    </svg>
  );
};

export default IconMarker;
