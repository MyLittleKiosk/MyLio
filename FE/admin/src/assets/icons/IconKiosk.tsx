import { iconProps } from '../../types/iconProps';

const IconKiosk = ({ width, height }: iconProps) => {
  return (
    <svg
      width={width}
      height={height}
      viewBox='0 0 21 21'
      fill='none'
      xmlns='http://www.w3.org/2000/svg'
    >
      <path
        d='M15.6667 2.14307H5.66667C4.74619 2.14307 4 2.88926 4 3.80973V17.1431C4 18.0635 4.74619 18.8097 5.66667 18.8097H15.6667C16.5871 18.8097 17.3333 18.0635 17.3333 17.1431V3.80973C17.3333 2.88926 16.5871 2.14307 15.6667 2.14307Z'
        stroke='#0A0A0A'
        strokeWidth='1.66667'
        strokeLinecap='round'
        strokeLinejoin='round'
      />
      <path
        d='M10.667 15.4766H10.6753'
        stroke='#0A0A0A'
        strokeWidth='1.66667'
        strokeLinecap='round'
        strokeLinejoin='round'
      />
    </svg>
  );
};

export default IconKiosk;
