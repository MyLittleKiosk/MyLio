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
    // 팝업에서 결제 성공 시 부모 창에 메시지 전송 후 팝업 닫기
    if (window.opener) {
      window.opener.postMessage('KAKAO_PAY_SUCCESS', '*');
      window.close();
    }

    // 기존 결제 성공 처리 로직
    const pgToken = searchParams.get('pg_token');
    const orderId = searchParams.get('orderId');
    if (pgToken && orderId) {
      postSuccess({ orderId, pgToken });
    } else if (!order.sessionId) {
      alert('세션 ID가 없습니다.');
      navigate('/kiosk/select-pay');
    }
  }, []);

  return (
    <div className='flex flex-col items-center justify-center w-full h-full'>
      <h2 className='text-xl font-preBold mb-4'>카카오페이 결제 진행중...</h2>
      <p className='text-gray-600'>잠시만 기다려주세요.</p>
    </div>
  );
};

export default PayLoading;
