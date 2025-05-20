import { useEffect } from 'react';
import { useNavigate, useLocation } from 'react-router-dom';

const KakaoPayBridge = () => {
  const navigate = useNavigate();
  const location = useLocation();

  useEffect(() => {
    if (window.opener) {
      window.opener.postMessage('KAKAO_PAY_SUCCESS', '*');
      window.close();
    } else {
      navigate('/kiosk/pay/loading' + location.search);
    }
  }, [navigate, location]);

  return <div>결제 완료 처리 중입니다...</div>;
};

export default KakaoPayBridge;
