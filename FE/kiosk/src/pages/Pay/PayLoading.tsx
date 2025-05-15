import { useEffect } from 'react';
import { useLocation, useNavigate } from 'react-router-dom';
import useOrderStore from '@/stores/useOrderStore';
import { usePostSuccess } from '@/service/queries/order';

const PayLoading = () => {
  const { order } = useOrderStore();
  const { mutate: postSuccess } = usePostSuccess();
  const location = useLocation();
  const searchParams = new URLSearchParams(location.search);
  const navigate = useNavigate();

  useEffect(() => {
    const pgToken = searchParams.get('pg_token');
    const orderId = searchParams.get('orderId');

    if (pgToken && orderId) {
      postSuccess(
        { orderId, pgToken },
        {
          onSuccess: () => {
            navigate('/kiosk/pay-success');
          },
          onError: () => {
            navigate('/kiosk/pay-fail');
          },
        }
      );
    } else {
      if (!order.sessionId) {
        alert('세션 ID가 없습니다.');
        navigate('/kiosk/select-pay');
      }
    }
  }, [location.search, navigate, postSuccess, order.sessionId]);

  return (
    <div className='flex flex-col items-center justify-center w-full h-full'>
      <h2 className='text-xl font-preBold mb-4'>카카오페이 결제 진행중...</h2>
      <p className='text-gray-600'>잠시만 기다려주세요.</p>
    </div>
  );
};

export default PayLoading;
