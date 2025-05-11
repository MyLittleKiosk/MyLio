import { iconProps } from '@/types/iconProps';

const IconImage = ({
  width = 8,
  height = 8,
  fillColor = 'gray-400',
}: iconProps) => {
  return (
    <svg
      className={`w-${width} h-${height} text-${fillColor}`}
      fill='none'
      stroke='currentColor'
      viewBox='0 0 24 24'
    >
      <path
        strokeLinecap='round'
        strokeLinejoin='round'
        strokeWidth='2'
        d='M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z'
      />
    </svg>
  );
};

export default IconImage;
