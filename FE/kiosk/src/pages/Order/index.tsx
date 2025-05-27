import { useOrderRequest } from '@/service/queries/order';
import useOrderStore from '@/stores/useOrderStore';
import { formatNumber } from '@/utils/formatNumber';
import clsx from 'clsx';

const Order = () => {
  const { order, setOrder } = useOrderStore();
  const { mutate } = useOrderRequest();
  const menu = order.contents[0];

  const handleOptionSelect = (optionId: number, optionDetailId: number) => {
    const updatedOptions = menu.options.map((opt) =>
      opt.optionId === optionId ? { ...opt, selectedId: optionDetailId } : opt
    );

    const updatedContents = order.contents.map((content) =>
      content.menuId === menu.menuId
        ? { ...content, options: updatedOptions }
        : content
    );

    setOrder({
      ...order,
      contents: updatedContents,
    });
  };

  const isAllRequiredOptionsSelected = () => {
    return menu.options.every(
      (opt) => !opt.required || (opt.required && opt.selectedId !== null)
    );
  };

  const handleOrderRequest = () => {
    if (!isAllRequiredOptionsSelected()) return;

    const selectedOptions = menu.options
      .filter((opt) => opt.selectedId !== null)
      .map((opt) => {
        const selectedDetail = opt.optionDetails.find(
          (detail) => detail.optionDetailId === opt.selectedId
        );
        return `${opt.optionName}는 ${selectedDetail?.optionDetailValue}로`;
      })
      .join(' ');

    mutate({
      text: `${selectedOptions} 해주세요.`,
      ...order,
    });
  };

  return (
    order.contents[0] && (
      <section className='flex flex-col w-full h-full pt-5'>
        <div className='flex justify-between items-center'>
          <h1 className='text-2xl font-preBold inline-block ps-10 mb-4'>
            메뉴 주문
          </h1>
          <button
            onClick={handleOrderRequest}
            disabled={!isAllRequiredOptionsSelected()}
            className={clsx(
              'text-sm font-preBold text-white rounded-full px-4 py-2 me-10',
              isAllRequiredOptionsSelected()
                ? 'bg-primary'
                : 'bg-gray-300 cursor-not-allowed'
            )}
          >
            주문 담기
          </button>
        </div>
        <div className='flex flex-col items-center w-4/5 mx-auto justify-between overflow-y-auto'>
          <div className='flex items-center justify-center mb-1 w-full gap-4'>
            <img
              src={menu.imageUrl}
              alt={menu.name}
              className='w-24 h-24 object-cover rounded-xl mx-auto'
            />
            <div className='w-full h-full p-4 flex flex-col gap-4 justify-between'>
              <div>
                <p className='text-2xl font-preBold'>{menu.name}</p>
                <p className='text-xs text-gray-500 break-keep'>
                  {menu.description}
                </p>
              </div>
              <p className='text-xl font-preBold'>
                {formatNumber(menu.totalPrice)}원
              </p>
            </div>
          </div>
          <div className='flex flex-col h-full w-full overflow-y-auto mb-36 gap-2'>
            {menu.options.map((opt) => (
              <div key={opt.optionId} className='flex gap-2 items-center'>
                <div className='flex flex-col'>
                  <div className='flex gap-2 items-center'>
                    <p className='text-lg font-preBold'>{opt.optionName}</p>
                    {opt.required && (
                      <span className='text-sm text-red-500'>필수</span>
                    )}
                  </div>
                  <div className='flex flex-wrap gap-2'>
                    {opt.optionDetails.map((detail) => (
                      <button
                        key={detail.optionDetailId}
                        onClick={() =>
                          handleOptionSelect(
                            opt.optionId,
                            detail.optionDetailId
                          )
                        }
                        className={clsx(
                          'text-sm text-gray-500 px-2 py-1 rounded-md break-keep cursor-pointer',
                          opt.selectedId === detail.optionDetailId
                            ? 'bg-primary text-white'
                            : 'bg-gray-200 text-gray-500'
                        )}
                      >
                        {detail.optionDetailValue}
                        {detail.additionalPrice > 0 && (
                          <span
                            className={clsx(
                              'text-sm',
                              opt.selectedId === detail.optionDetailId
                                ? 'text-white'
                                : 'text-gray-500'
                            )}
                          >
                            {` (+${formatNumber(detail.additionalPrice)}원)`}
                          </span>
                        )}
                      </button>
                    ))}
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>
      </section>
    )
  );
};

export default Order;
