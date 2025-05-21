import { usePostSuccess } from '@/service/queries/order';
import useOrderStore from '@/stores/useOrderStore';
import { useEffect } from 'react';
import { useNavigate, useSearchParams } from 'react-router-dom';

const CardPay = () => {
  const navigate = useNavigate();
  const { order } = useOrderStore();
  const { mutate: postSuccess } = usePostSuccess();
  const [searchParams] = useSearchParams();
  const payMethod = searchParams.get('pay_method');
  useEffect(() => {
    const timeout = setTimeout(() => {
      sessionStorage.setItem('cartItem', JSON.stringify(order.cart));
      if (order.payment !== 'PAY' && payMethod !== 'PAY') {
        postSuccess({
          orderId: order.sessionId || '',
          pgToken: null,
          payMethod: payMethod || '',
        });
      }
      navigate('/success');
    }, 3000);
    return () => {
      clearTimeout(timeout);
    };
  }, []);
  return (
    <section className='flex flex-col w-full h-full px-10 pt-10'>
      <div className='flex flex-col items-center justify-center w-full h-full'>
        <h2 className='text-xl font-preBold mb-4'>결제 진행중...</h2>
        <p className='text-gray-600'>잠시만 기다려주세요.</p>
      </div>
    </section>
  );
};

export default CardPay;
