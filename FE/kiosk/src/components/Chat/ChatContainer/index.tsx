import lio from '@/assets/images/ListenLio.png';
import clsx from 'clsx';
import { motion } from 'framer-motion';
import VoiceAnimation from '../VoiceAnimation';
import { useLocation } from 'react-router-dom';
import { IMAGE_ROUTE } from '@/datas/IMAGE_ROUTE';
import { useMemo } from 'react';
interface Props {
  userChat: string;
  gptChat: string;
  isExpand: boolean;
}

// 이미지 크기 variants (width만 조절)
const imageVariants = {
  expanded: {
    width: 600,
    transition: { type: 'spring', stiffness: 100, damping: 20, mass: 1 },
  },
  collapsed: {
    width: 200,
    transition: { type: 'spring', stiffness: 100, damping: 20, mass: 1 },
  },
};

// gptChat 텍스트 variants
const textVariants = {
  expanded: {
    scale: 1.2,
    transition: { type: 'spring', stiffness: 100, damping: 20, mass: 1 },
  },
  collapsed: {
    scale: 1,
    transition: { type: 'spring', stiffness: 100, damping: 20, mass: 1 },
  },
};

// 레이아웃 애니메이션 설정
const layoutTransition = {
  type: 'spring',
  stiffness: 100,
  damping: 20,
  mass: 1,
  duration: 0.3,
};

const ChatContainer = ({ userChat, gptChat, isExpand }: Props) => {
  const { pathname } = useLocation();
  const image = useMemo(() => {
    if (pathname === '/kiosk') return lio;
    const imagePath = pathname.split('/').pop();
    console.log('imagePath:', imagePath);
    return IMAGE_ROUTE[imagePath as keyof typeof IMAGE_ROUTE];
  }, [pathname]);
  console.log('image:', image);
  function handleUserChatFontSize() {
    if (!userChat) return isExpand ? 'text-xl' : 'text-lg';

    const base = isExpand ? 'text-xl' : 'text-lg';
    const userChatLength = userChat.length;

    if (userChatLength > 100) return 'text-xs';
    if (userChatLength > 50) return `text-sm`;
    if (userChatLength > 20) return `text-base`;

    return base;
  }

  return (
    <motion.div
      className='w-full h-full px-4 sm:px-6 md:px-10 flex flex-col items-center justify-start gap-5'
      transition={layoutTransition}
      layout
    >
      <motion.div
        className={clsx(
          'w-full max-w-7xl h-full flex items-center justify-start',
          isExpand ? 'flex-col gap-10' : 'flex-row gap-4'
        )}
        layout
        transition={layoutTransition}
      >
        <motion.div
          className='p-2 pe-1 flex justify-center items-center rounded-full shrink-0'
          style={{
            aspectRatio: '1/1',
            overflow: 'hidden',
          }}
          variants={imageVariants}
          animate={isExpand ? 'expanded' : 'collapsed'}
          layout
        >
          <img
            src={image}
            alt='img'
            className='object-contain w-full h-full mb-2'
            draggable={false}
          />
        </motion.div>
        <motion.div
          className={clsx(
            'w-[min(600px,80vw)] font-preBold whitespace-pre-line break-keep',
            isExpand ? 'text-xl text-center' : 'text-lg text-start'
          )}
          variants={textVariants}
          animate={isExpand ? 'expanded' : 'collapsed'}
          layout
        >
          <div className='w-full h-full overflow-y-auto font-preBold'>
            {gptChat}
          </div>
        </motion.div>
      </motion.div>
      <motion.div
        layout
        transition={layoutTransition}
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
      >
        <VoiceAnimation />
      </motion.div>
      <motion.div
        className={clsx(
          'font-preSemiBold text-center text-gray-400 break-keep',
          handleUserChatFontSize()
        )}
        layout
        transition={layoutTransition}
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
      >
        {userChat !== '' && (
          <span className='font-preBold'>&quot;{userChat}&quot;</span>
        )}
      </motion.div>
    </motion.div>
  );
};

export default ChatContainer;
