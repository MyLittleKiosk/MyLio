import { formatNumber } from '@/utils/formatNumber';

interface OptionProps {
  optionName: string;
  price: number;
}

const Option = ({ optionName, price }: OptionProps) => {
  return (
    <div className='px-3 py-2  rounded-md bg-primary text-white font-preBold text-sm '>
      {optionName} (+{formatNumber(price)}원)
    </div>
  );
};

export default Option;
