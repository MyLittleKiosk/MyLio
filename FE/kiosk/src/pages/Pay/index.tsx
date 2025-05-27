import useOrderStore from '@/stores/useOrderStore';
import KakaoPay from './KakaoPay';
import CardPay from './CardPay';

const Pay = () => {
  const { order } = useOrderStore();
  return (
    <div className='flex flex-col w-full h-full px-10 pt-10'>
      <h1 className='text-2xl font-preBold'>결제</h1>
      {order.payment === 'PAY' ? <KakaoPay /> : <CardPay />}
    </div>
  );
};

export default Pay;
