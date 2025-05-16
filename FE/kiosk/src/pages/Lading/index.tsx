import { Link } from 'react-router-dom';

const Landing = () => {
  return (
    <section className='w-screen h-dvh mx-auto rounded-2xl shadow-lg flex flex-col items-center'>
      <img
        src='/src/assets/images/poster.png'
        alt='poster'
        className='w-full'
      />
      <div className='flex flex-col w-full gap-2 justify-center items-center '>
        <div className='flex w-full gap-2 justify-center items-center'>
          <Link
            to='/kiosk'
            className='flex justify-center items-center text-2xl bg-primary text-white font-bold py-2 rounded-xl w-1/2 h-[200px]'
          >
            먹고갈래요
          </Link>
          <Link
            to='/kiosk'
            className='flex justify-center items-center text-2xl bg-primary text-white font-bold py-2 rounded-xl w-1/2 h-[200px]'
          >
            가져갈래요
          </Link>
        </div>
        <div className='flex flex-col w-full justify-between mt-3'>
          <div className='flex gap-2 justify-between items-center px-4'>
            <button className='text-xl'>한국어</button>
            <button className='text-xl'>English</button>
            <button className='text-xl'>中文</button>
            <button className='text-xl'>日本語</button>
          </div>
        </div>
      </div>
      {/* 언어 선택 */}
    </section>
  );
};

export default Landing;
