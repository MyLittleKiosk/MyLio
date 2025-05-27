import { useEffect } from 'react';
import { useLocation } from 'react-router-dom';

const PayLoading = () => {
  const location = useLocation();
  const searchParams = new URLSearchParams(location.search);

  useEffect(() => {
    // 결제 성공 시 부모 창에 메시지와 파라미터 전달 후 팝업 닫기
    if (window.opener) {
      const pgToken = searchParams.get('pg_token');
      const orderId = searchParams.get('orderId');
      window.opener.postMessage(
        { type: 'KAKAO_PAY_SUCCESS', pgToken, orderId },
        '*'
      );
      window.close();
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
