import clsx from 'clsx';

interface OptionDetail {
  optionDetailValue: string;
  additionalPrice: number;
}

interface Option {
  optionName: string;
  optionDetails: OptionDetail[];
}

interface ItemProps {
  imageUrl: string;
  name: string;
  selectedOption: Option[];
  totalPrice: number;
  count: number;
  isLast?: boolean;
  onIncrease: () => void;
  onDecrease: () => void;
}

const Item = ({
  imageUrl,
  name,
  selectedOption,
  totalPrice,
  count,
  isLast,
  onIncrease,
  onDecrease,
}: ItemProps) => {
  return (
    <div
      className={clsx(
        'flex items-center gap-7 border-b-2 pb-4 border-gray-200',
        isLast && 'border-b-0'
      )}
    >
      <img
        src={imageUrl}
        alt={name}
        className='w-20 h-20 object-cover rounded-lg'
      />
      <div className='flex flex-col w-1/2 justify-between'>
        <h2 className='text-lg font-preBold'>{name}</h2>
        {selectedOption.map((option) => (
          <p key={option.optionName} className='text-xs text-gray-500'>
            {option.optionDetails
              .map(
                (detail) =>
                  `${detail.optionDetailValue}${
                    detail.additionalPrice > 0
                      ? ` (+${detail.additionalPrice}원)`
                      : ''
                  }`
              )
              .join(', ')}
          </p>
        ))}
        <p className='font-bold'>{totalPrice.toLocaleString()}원</p>
      </div>
      <div className='flex h-full items-end'>
        <div className='flex items-center bg-gray-100 rounded-xl px-3 py-1 gap-2 w-fit'>
          <button
            className='text-xl font-bold text-gray-400'
            onClick={onDecrease}
            disabled={count <= 1}
          >
            -
          </button>
          <span className='w-8 h-7 flex justify-center items-center  text-center font-bold text-gray-700 bg-white rounded-lg'>
            {count}
          </span>
          <button
            className='text-xl font-bold text-gray-400'
            onClick={onIncrease}
          >
            +
          </button>
        </div>
      </div>
    </div>
  );
};

export default Item;
