import { useEffect } from 'react';
import { useSearchParams } from 'react-router-dom';
import { useRequestPay, usePostSuccess } from '@/service/queries/order';
import useOrderStore from '@/stores/useOrderStore';

const KakaoPay = () => {
  const [searchParams] = useSearchParams();
  const { order } = useOrderStore();
  const { mutate: requestPay } = useRequestPay();
  const { mutate: postSuccess } = usePostSuccess();

  useEffect(() => {
    const pgToken = searchParams.get('pg_token');
    const orderId = searchParams.get('orderId');

    if (pgToken && orderId) {
      // 결제 성공 처리
      postSuccess({ orderId, pgToken });
    } else {
      // 결제 요청
      if (!order.sessionId) {
        throw new Error('세션 ID가 없습니다.');
      }
      const payRequest = {
        itemName: order.cart.map((item) => item.name).join(', '),
        totalAmount: order.cart.reduce((acc, item) => acc + item.quantity, 0),
        sessionId: order.sessionId,
      };
      requestPay(payRequest);
    }
  }, [searchParams]);

  return (
    <div className='flex flex-col items-center justify-center w-full h-full'>
      <h2 className='text-xl font-preBold mb-4'>카카오페이 결제 진행중...</h2>
      <p className='text-gray-600'>잠시만 기다려주세요.</p>
    </div>
  );
};

export default KakaoPay;
