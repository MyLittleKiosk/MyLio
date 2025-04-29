import { iconProps } from '../../types/iconProps';

const IconStatistic = ({ width, height }: iconProps) => {
  return (
    <svg
      width={width}
      height={height}
      viewBox='0 0 20 20'
      fill='none'
      xmlns='http://www.w3.org/2000/svg'
    >
      <path
        d='M2.5 2.5V17.5H17.5'
        stroke='black'
        strokeWidth='1.66667'
        strokeLinecap='round'
        strokeLinejoin='round'
      />
      <path
        d='M15 14.1667V7.5'
        stroke='black'
        strokeWidth='1.66667'
        strokeLinecap='round'
        strokeLinejoin='round'
      />
      <path
        d='M10.832 14.1667V4.16675'
        stroke='black'
        strokeWidth='1.66667'
        strokeLinecap='round'
        strokeLinejoin='round'
      />
      <path
        d='M6.66797 14.1667V11.6667'
        stroke='black'
        strokeWidth='1.66667'
        strokeLinecap='round'
        strokeLinejoin='round'
      />
    </svg>
  );
};

export default IconStatistic;
