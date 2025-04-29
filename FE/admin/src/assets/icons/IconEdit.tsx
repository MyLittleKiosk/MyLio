import { iconProps } from '@/types/iconProps';

const IconEdit = ({ width, height }: iconProps) => {
  return (
    <svg
      width={width}
      height={height}
      viewBox='0 0 16 16'
      fill='none'
      xmlns='http://www.w3.org/2000/svg'
    >
      <path
        d='M8 2H3.33333C2.97971 2 2.64057 2.14048 2.39052 2.39052C2.14048 2.64057 2 2.97971 2 3.33333V12.6667C2 13.0203 2.14048 13.3594 2.39052 13.6095C2.64057 13.8595 2.97971 14 3.33333 14H12.6667C13.0203 14 13.3594 13.8595 13.6095 13.6095C13.8595 13.3594 14 13.0203 14 12.6667V8'
        stroke='#09090B'
        strokeWidth='1.33333'
        strokeLinecap='round'
        strokeLinejoin='round'
      />
      <path
        d='M12.2487 1.74991C12.5139 1.48469 12.8736 1.33569 13.2487 1.33569C13.6238 1.33569 13.9835 1.48469 14.2487 1.74991C14.5139 2.01512 14.6629 2.37483 14.6629 2.74991C14.6629 3.12498 14.5139 3.48469 14.2487 3.74991L7.9987 9.99991L5.33203 10.6666L5.9987 7.99991L12.2487 1.74991Z'
        stroke='#09090B'
        strokeWidth='1.33333'
        strokeLinecap='round'
        strokeLinejoin='round'
      />
    </svg>
  );
};

export default IconEdit;
