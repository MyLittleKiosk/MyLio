import { PAY_METHODS } from '@/datas/PAYS';
import { formatNumber } from '@/utils/formatNumber';

const SelectPay = () => {
  const totalPrice = 13000;

  return (
    <section className='flex flex-col w-full h-full px-10 pt-10'>
      <h1 className='text-2xl font-bold'>결제 수단</h1>
      <div className='grid grid-cols-2 gap-3 mt-10 w-full overflow-y-auto p-1'>
        {PAY_METHODS.map((pay) => (
          <div
            key={pay.id}
            className='flex items-center gap-2 border border-gray-300 rounded-md p-10 justify-center shadow-md'
          >
            <span className='text-lg font-bold'>{pay.name}</span>
          </div>
        ))}
      </div>
      <div className='mt-10 w-full flex justify-center'>
        <div className='border border-gray-200 rounded-md px-8 py-6 flex items-center gap-4 bg-white shadow'>
          <span className='font-bold text-lg'>총 결제 금액</span>
          <span className='text-blue-500 font-bold text-lg'>
            {formatNumber(totalPrice)}원
          </span>
        </div>
      </div>
    </section>
  );
};

export default SelectPay;
