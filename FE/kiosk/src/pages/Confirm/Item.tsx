import { useDebounce } from '@/hooks/useDebounce';
import { useOrderRequest } from '@/service/queries/order';
import useOrderStore from '@/stores/useOrderStore';
import clsx from 'clsx';
import { useState } from 'react';

interface OptionDetail {
  optionDetailValue: string;
  additionalPrice: number;
}

interface Option {
  optionName: string;
  optionDetails: OptionDetail[];
}

interface ItemProps {
  menuId: number;
  imageUrl: string;
  name: string;
  selectedOption: Option[];
  totalPrice: number;
  count: number;
  isLast?: boolean;
}

const Item = ({
  menuId,
  imageUrl,
  name,
  selectedOption,
  totalPrice,
  count,
  isLast,
}: ItemProps) => {
  const { mutate } = useOrderRequest();
  const { order, setOrder } = useOrderStore();
  const [counter, setCounter] = useState(0);

  const debouncedMutate = useDebounce(
    (params: Parameters<typeof mutate>[0]) => {
      mutate(params, {
        onSuccess: () => {
          setCounter(0);
        },
      });
    },
    800
  );

  const increaseCount = (menuId: number) => {
    const cartItem = order.cart.find((item) => item.menuId === menuId);
    const quantity = cartItem ? cartItem.quantity + 1 : 1;

    setOrder({
      ...order,
      cart: order.cart.map((item) =>
        item.menuId === menuId ? { ...item, quantity } : item
      ),
      contents: order.contents.map((item) =>
        item.menuId === menuId ? { ...item, quantity } : item
      ),
    });

    setCounter(counter + 1);

    debouncedMutate({
      text: `cartId가 ${cartItem?.cartId}이고, cartName이 ${cartItem?.name}인 메뉴의 수량을 ${counter + 1}만큼 추가해 주세요.`,
      ...order,
    });
  };

  const decreaseCount = (menuId: number) => {
    const cartItem = order.cart.find((item) => item.menuId === menuId);
    const quantity = cartItem ? cartItem.quantity - 1 : 0;

    setOrder({
      ...order,
      cart: order.cart.map((item) =>
        item.menuId === menuId ? { ...item, quantity } : item
      ),
      contents: order.contents.map((item) =>
        item.menuId === menuId ? { ...item, quantity } : item
      ),
    });

    setCounter(counter - 1);

    debouncedMutate({
      text: `cartId가 ${cartItem?.cartId}이고, cartName이 ${cartItem?.name}인 메뉴의 수량을 ${counter - 1}만큼 감소해 주세요.`,
      ...order,
    });
  };

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
            onClick={() => decreaseCount(menuId)}
            disabled={count <= 1}
          >
            -
          </button>
          <span className='w-8 h-7 flex justify-center items-center  text-center font-bold text-gray-700 bg-white rounded-lg'>
            {count}
          </span>
          <button
            className='text-xl font-bold text-gray-400'
            onClick={() => increaseCount(menuId)}
          >
            +
          </button>
        </div>
      </div>
    </div>
  );
};

export default Item;
