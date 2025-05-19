import { useEffect } from 'react';
import { useNavigate } from 'react-router-dom';

const CardPay = () => {
  const navigate = useNavigate();
  useEffect(() => {
    const timeout = setTimeout(() => {
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
