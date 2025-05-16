import Character_Search from '@/assets/images/Character_Search.jpg';

const Loading = () => {
  return (
    <div className='w-full h-full flex flex-col items-center justify-center gap-10 border border-subContent rounded-lg'>
      <img src={Character_Search} alt='로딩 중' className='w-1/5' />
      <div className='flex flex-col items-center justify-center gap-2'>
        <p className='text-2xl font-preBold'>로딩 중입니다.</p>
        <p className='text-lg font-preSemiBold text-longContent'>
          잠시만 기다려 주세요!
        </p>
      </div>
    </div>
  );
};

export default Loading;
