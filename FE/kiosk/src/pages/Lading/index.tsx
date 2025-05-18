import { Link } from 'react-router-dom';
import landingImage1 from '@/assets/images/landing_image_1.png';
import landingImage2 from '@/assets/images/landing_image_2.png';
import landingImage3 from '@/assets/images/landing_image_3.png';
import landingImage4 from '@/assets/images/landing_image_4.png';
import atStore from '@/assets/images/at_store.png';
import toGo from '@/assets/images/to_go.png';
import korean from '@/assets/images/korean.png';
import english from '@/assets/images/english.png';
import japan from '@/assets/images/japan.png';
import china from '@/assets/images/china.png';
import { motion } from 'framer-motion';
import { useTranslation } from 'react-i18next';

const images = [landingImage1, landingImage2, landingImage3, landingImage4];

const IMAGE_WIDTH = 340;
const GAP = 8;
const SLIDE_WIDTH = (IMAGE_WIDTH + GAP) * images.length;

const Landing = () => {
  const { t, i18n } = useTranslation();
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
          <span className='font-preBold'>{t('hello')}</span>
          <span className='font-preBold'>{t('intro')}</span>
          <span className='font-preBold'>{t('start_order')}</span>
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
                <span className='font-preBold text-xl'>{t('eat_here')}</span>
              </div>
            </button>
          </Link>
          <Link to='/kiosk' className='w-1/2'>
            <button className='bg-gray-200 py-2 rounded-xl w-40'>
              <div className='flex flex-col gap-2 justify-center items-center'>
                <img src={toGo} alt='toGo' className='w-[162px] h-[162px]' />
                <span className='font-preBold text-xl'>{t('to_go')}</span>
              </div>
            </button>
          </Link>
        </div>
        <div className='flex gap-4 justify-center mt-10'>
          <button onClick={() => i18n.changeLanguage('ko')}>
            <img src={korean} alt='korean' className='w-10 h-10' />
          </button>
          <button onClick={() => i18n.changeLanguage('en')}>
            <img src={english} alt='english' className='w-10 h-10' />
          </button>
          <button onClick={() => i18n.changeLanguage('ja')}>
            <img src={japan} alt='japan' className='w-10 h-10' />
          </button>
          <button onClick={() => i18n.changeLanguage('zh')}>
            <img src={china} alt='china' className='w-10 h-10' />
          </button>
        </div>
      </div>
    </section>
  );
};

export default Landing;
