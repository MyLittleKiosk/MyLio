import { useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { motion } from 'framer-motion';
import useKioskStore from '@/stores/useKioskStore';
const Success = () => {
  const navigate = useNavigate();
  const { orderId } = useKioskStore();

  useEffect(() => {
    const timer = setTimeout(() => {
      navigate('/landing');
    }, 3000);
    return () => clearTimeout(timer);
  }, [navigate]);

  return (
    <div className='flex flex-col items-center justify-center w-full h-full fixed top-0 left-0 bg-white gap-10'>
      <div className='flex flex-col items-center justify-center w-40 h-40 border-8 border-primary rounded-full px-4 py-4 mb-5'>
        <motion.svg
          width='200'
          height='200'
          viewBox='0 0 100 100'
          initial='hidden'
          animate='visible'
        >
          <motion.path
            d='M20 50 L40 70 L80 30'
            fill='transparent'
            stroke='#5D85FE'
            strokeWidth='8'
            strokeLinecap='round'
            strokeLinejoin='round'
            variants={{
              hidden: {
                pathLength: 0,
                opacity: 0,
              },
              visible: {
                pathLength: 1,
                opacity: 1,
                scale: 1,
                rotate: 0,
                transition: {
                  duration: 0.5,
                  ease: 'easeInOut',
                },
              },
            }}
          />
        </motion.svg>
      </div>
      <div className='flex flex-col items-center justify-center gap-2'>
        <span className='font-preBold text-4xl bg-gradient-to-r from-[#578771] to-[#0471FF] text-transparent bg-clip-text'>
          결제 완료!
        </span>
        <p className='font-preBold text-2xl'>{orderId}번으로 알려드릴게요</p>
      </div>
      <div className='flex flex-col items-center justify-center gap-2'>
        <p className='font-preBold text-sm text-gray-500'>
          3초 후 메인 화면으로 돌아가요
        </p>
      </div>
    </div>
  );
};

export default Success;
