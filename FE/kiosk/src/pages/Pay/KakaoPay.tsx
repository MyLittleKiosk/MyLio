import { useEffect } from 'react';
import { useSearchParams, useNavigate } from 'react-router-dom';
import { useRequestPay } from '@/service/queries/order';
import useOrderStore from '@/stores/useOrderStore';
import { usePostSuccess } from '@/service/queries/order';

const KakaoPay = () => {
  const [searchParams] = useSearchParams();
  const { order } = useOrderStore();
  const { mutate: requestPay } = useRequestPay();
  const { mutate: postSuccess } = usePostSuccess();
  const navigate = useNavigate();

  useEffect(() => {
    if (!order.sessionId) throw new Error('세션 ID가 없습니다.');
    const payRequest = {
      itemName: order.cart.map((item) => item.name).join(', '),
      totalAmount: order.cart.reduce((acc, item) => acc + item.quantity, 0),
      sessionId: order.sessionId,
    };
    requestPay(payRequest, {
      onSuccess: (data) => {
        const width = 800;
        const height = 1000;
        const left = (window.screen.width - width) / 2;
        const top = (window.screen.height - height) / 2;
        window.open(
          data.data.next_redirect_pc_url,
          'kakaoPay',
          `width=${width},height=${height},left=${left},top=${top},scrollbars=yes,resizable=no,status=no,location=no,menubar=no,toolbar=no,titlebar=no`
        );
      },
    });
  }, [searchParams]);

  useEffect(() => {
    const handleMessage = (event: MessageEvent) => {
      if (
        event.data &&
        event.data.type === 'KAKAO_PAY_SUCCESS' &&
        event.data.pgToken &&
        event.data.orderId
      ) {
        postSuccess({
          orderId: event.data.orderId,
          pgToken: event.data.pgToken,
          payMethod: 'PAY',
        });
      }
    };
    window.addEventListener('message', handleMessage);
    return () => window.removeEventListener('message', handleMessage);
  }, [postSuccess, navigate]);

  return (
    <div className='flex flex-col items-center justify-center w-full h-full'>
      <h2 className='text-xl font-preBold mb-4'>
        카카오페이 결제 창이 열립니다...
      </h2>
      <p className='text-gray-600'>팝업 창에서 결제를 진행해주세요.</p>
    </div>
  );
};

export default KakaoPay;
