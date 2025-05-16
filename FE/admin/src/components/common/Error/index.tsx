import { useNavigate } from 'react-router-dom';
import Button from '@/components/common/Button';
import Character_ROOo from '@/assets/images/Character_ROOo.png';

const Error = () => {
  const navigate = useNavigate();

  return (
    <div className='w-full h-full flex flex-col items-center justify-center gap-10 border border-subContent rounded-lg'>
      <img src={Character_ROOo} alt='에러 발생' className='w-1/5' />
      <div className='flex flex-col items-center justify-center gap-2'>
        <p className='text-2xl font-preBold'>오류가 발생했습니다.</p>
        <p className='text-lg font-preSemiBold text-longContent'>
          잠시 후 다시 시도해 주세요.
        </p>
      </div>

      <Button onClick={() => navigate('/')} text='홈으로' />
    </div>
  );
};

export default Error;
