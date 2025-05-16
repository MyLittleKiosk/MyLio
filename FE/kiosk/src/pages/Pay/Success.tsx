import { useEffect } from 'react';
import { useNavigate } from 'react-router-dom';

const Success = () => {
  const navigate = useNavigate();

  useEffect(() => {
    const timer = setTimeout(() => {
      navigate('/landing');
    }, 3000);

    return () => clearTimeout(timer);
  }, [navigate]);

  return (
    <div className='flex flex-col items-center justify-center w-full h-full'>
      <h2 className='text-2xl font-preBold mb-4'>결제가 완료되었습니다!</h2>
      <p className='text-gray-600'>잠시 후 메인 화면으로 이동합니다.</p>
    </div>
  );
};

export default Success;
