import { iconProps } from '@/types/iconProps';

const IconAdd = ({
  width = 24,
  height = 24,
  fillColor = '#292D32',
}: iconProps) => {
  return (
    <svg
      width={width}
      height={height}
      viewBox='0 0 24 24'
      fill='none'
      xmlns='http://www.w3.org/2000/svg'
    >
      <path
        d='M6 12H18'
        stroke={fillColor}
        strokeWidth='1.5'
        strokeLinecap='round'
        strokeLinejoin='round'
      />
      <path
        d='M12 18V6'
        stroke={fillColor}
        strokeWidth='1.5'
        strokeLinecap='round'
        strokeLinejoin='round'
      />
    </svg>
  );
};

export default IconAdd;
