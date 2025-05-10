interface Props {
  width: number;
  height: number;
}

const IconPerson = ({ width = 20, height = 20 }: Props) => {
  return (
    <svg
      width={width}
      height={height}
      viewBox='0 0 15 17'
      fill='none'
      xmlns='http://www.w3.org/2000/svg'
    >
      <path
        d='M13.3337 16V14.3333C13.3337 13.4493 12.9825 12.6014 12.3573 11.9763C11.7322 11.3512 10.8844 11 10.0003 11H5.00033C4.11627 11 3.26842 11.3512 2.6433 11.9763C2.01818 12.6014 1.66699 13.4493 1.66699 14.3333V16'
        stroke='black'
        strokeWidth='1.66667'
        strokeLinecap='round'
        strokeLinejoin='round'
      />
      <path
        d='M7.50033 7.66667C9.34127 7.66667 10.8337 6.17428 10.8337 4.33333C10.8337 2.49238 9.34127 1 7.50033 1C5.65938 1 4.16699 2.49238 4.16699 4.33333C4.16699 6.17428 5.65938 7.66667 7.50033 7.66667Z'
        stroke='black'
        strokeWidth='1.66667'
        strokeLinecap='round'
        strokeLinejoin='round'
      />
    </svg>
  );
};

export default IconPerson;
