import RunningLio from '@/assets/images/RunningLio.gif';

const Loading = () => {
  return (
    <div className='p-10 flex items-center justify-center gap-5 bg-white'>
      <img
        className='h-20 object-cover'
        src={RunningLio}
        alt='loading'
        loading='lazy'
      />
      <p className='font-preBold text-base text-content'>대기중입니다...</p>
    </div>
  );
};

export default Loading;
