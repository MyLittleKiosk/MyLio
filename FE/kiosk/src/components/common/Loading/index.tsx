import RunningLio from '@/assets/images/RunningLio.gif';
import LOADING_TEXT from '@/datas/loading';
const Loading = () => {
  return (
    <div className='p-10 flex flex-col items-center justify-center gap-5 bg-white rounded-lg'>
      <img
        className='h-20 object-cover'
        src={RunningLio}
        alt='loading'
        loading='lazy'
      />
      <p className='font-preBold text-xl text-content text-center whitespace-pre-line'>
        {LOADING_TEXT[Math.floor(Math.random() * LOADING_TEXT.length)]}
      </p>
    </div>
  );
};

export default Loading;
