import { PAY_METHODS } from '@/datas/PAYS';
import { formatNumber } from '@/utils/formatNumber';
import useOrderStore from '@/stores/useOrderStore';
const SelectPay = () => {
  const { order } = useOrderStore();
  const totalPrice = order.contents.reduce(
    (acc, curr) => acc + curr.totalPrice,
    0
  );
  return (
    <section className='flex flex-col w-full h-full pt-5'>
      <h1 className='text-2xl font-preBold inline-block ps-10 mb-4'>
        결제 수단
      </h1>
      <div className='flex flex-wrap w-full px-10 gap-2 justify-center mt-3'>
        {PAY_METHODS.map((pay) => (
          <div
            key={pay.id}
            className='flex flex-col items-center w-44 h-36 rounded-md justify-center bg-[#F4F4F5]'
          >
            <img src={pay.image} alt={pay.name} className='w-10 h-10' />
            <span className='text-lg font-preBold'>{pay.name}</span>
          </div>
        ))}
      </div>
      <div className='mt-10 w-full flex justify-center'>
        <div className='border border-gray-200 rounded-md px-8 py-6 flex items-center gap-4 bg-white shadow'>
          <span className='font-preBold text-lg'>총 결제 금액</span>
          <span className='text-blue-500 font-preBold text-lg'>
            {formatNumber(totalPrice)}원
          </span>
        </div>
      </div>
    </section>
  );
};

export default SelectPay;
