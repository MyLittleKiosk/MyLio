import { Link } from 'react-router-dom';
import landingImage1 from '@/assets/images/landing_image_1.png';
import landingImage2 from '@/assets/images/landing_image_2.png';
import landingImage3 from '@/assets/images/landing_image_3.png';
import landingImage4 from '@/assets/images/landing_image_4.png';
import atStore from '@/assets/images/at_store.png';
import toGo from '@/assets/images/to_go.png';
import { motion } from 'framer-motion';

const images = [landingImage1, landingImage2, landingImage3, landingImage4];

const IMAGE_WIDTH = 340;
const GAP = 8;
const SLIDE_WIDTH = (IMAGE_WIDTH + GAP) * images.length;

const Landing = () => {
  return (
    <section className='w-screen h-dvh mx-auto rounded-2xl shadow-lg flex flex-col'>
      <div className='flex flex-col gap-4 h-full flex flex-col items-center pt-40'>
        <div className='flex justify-center items-center overflow-hidden w-full'>
          <motion.div
            className='flex gap-1'
            animate={{
              x: [0, -SLIDE_WIDTH],
            }}
            transition={{
              duration: 10,
              repeat: Infinity,
              ease: 'linear',
            }}
            style={{ width: `${SLIDE_WIDTH * 2}px` }}
          >
            {[...images, ...images].map((img, idx) => (
              <img
                key={idx}
                src={img}
                alt={`landingImage${(idx % images.length) + 1}`}
                className='w-[340px] h-[340px] object-cover'
              />
            ))}
          </motion.div>
        </div>
        <p className='text-2xl flex flex-col gap-2 justify-center items-center mt-20'>
          <span className='font-preBold'>안녕하세요!</span>
          <span className='font-preBold'>음성인식 키오스크 리오와 함께</span>
          <span className='font-preBold'>주문을 시작하세요!</span>
        </p>
        <div className='flex gap-4 justify-center mt-10'>
          <Link to='/kiosk' className='w-1/2'>
            <button className='bg-gray-200 py-2 rounded-xl w-40'>
              <div className='flex flex-col gap-2 justify-center items-center'>
                <img
                  src={atStore}
                  alt='atStore'
                  className='w-[162px] h-[162px]'
                />
                <span className='font-preBold text-xl'>먹고가요</span>
              </div>
            </button>
          </Link>
          <Link to='/kiosk' className='w-1/2'>
            <button className='bg-gray-200 py-2 rounded-xl w-40'>
              <div className='flex flex-col gap-2 justify-center items-center'>
                <img src={toGo} alt='toGo' className='w-[162px] h-[162px]' />
                <span className='font-preBold text-xl'>포장해요</span>
              </div>
            </button>
          </Link>
        </div>
      </div>
    </section>
  );
};

export default Landing;
