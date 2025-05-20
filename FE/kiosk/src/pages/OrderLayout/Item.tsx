interface ItemFooterProps {
  cartId: string;
  imageUrl: string;
  name: string;
  quantity: number;
  onIncrease: () => void;
  onDecrease: () => void;
  onRemove: () => void;
}

const Item = ({
  imageUrl,
  name,
  quantity,
  onIncrease,
  onDecrease,
  onRemove,
}: ItemFooterProps) => {
  return (
    <div className='w-16 h-20 flex flex-col bg-white rounded-xl justify-between items-center relative'>
      <button
        className='absolute -top-2 -right-2 bg-red-500 text-white rounded-full w-6 h-6 flex items-center justify-center text-sm font-bold z-10'
        onClick={onRemove}
      >
        X
      </button>
      <img
        src={imageUrl}
        alt={name}
        className='w-16 h-16 object-cover rounded-t-xl'
      />
      <div className='flex items-center justify-center bg-gray-200 rounded-b-xl w-full '>
        <button
          className='text-gray-500 px-2'
          onClick={onDecrease}
          disabled={quantity <= 1}
        >
          -
        </button>
        <span className='mx-1 w-4 text-center text-xs'>{quantity}</span>
        <button className='text-gray-500 px-2' onClick={onIncrease}>
          +
        </button>
      </div>
    </div>
  );
};

export default Item;
