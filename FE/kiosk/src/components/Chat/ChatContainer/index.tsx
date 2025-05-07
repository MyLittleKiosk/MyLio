import lio from '@/assets/images/ListenLio.png';
import clsx from 'clsx';
import { motion } from 'framer-motion';
import VoiceAnimation from '../VoiceAnimation';

interface Props {
  userChat: string;
  gptChat: string;
  isRecording: boolean;
  volume: number;
  isExpand: boolean; // 하단 컨텐츠가 있으면 true로 받아옴
}

// 이미지 크기 variants - 실제 애니메이션 속성만 사용
const imageVariants = {
  expanded: { width: 400, height: 400 },
  collapsed: { width: 100, height: 100 },
};

// gptChat 텍스트 variants
const textVariants = {
  expanded: { scale: 1.2 },
  collapsed: { scale: 1 },
};

// 스프링 애니메이션 설정
const springTransition = {
  type: 'spring',
  stiffness: 300,
  damping: 30,
};

const ChatContainer = ({
  userChat,
  gptChat,
  isRecording,
  volume,
  isExpand,
}: Props) => {
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
      className='w-full h-full px-10 flex flex-col items-center gap-5'
      transition={springTransition}
      layout
    >
      <motion.div
        className={clsx(
          'h-full flex items-center justify-center',
          isExpand ? 'flex-col gap-10' : 'flex-row gap-4'
        )}
        layout // 이것이 중요! flex 방향 변화를 애니메이션화
        transition={springTransition}
      >
        <motion.div
          className='w-fit p-2 flex justify-center items-center bg-white rounded-full'
          style={{ boxShadow: 'inset 0px 0px 10px rgba(0, 0, 0, 0.25)' }}
          transition={springTransition}
          layout
        >
          <motion.img
            src={lio}
            alt='img'
            className='object-cover'
            variants={imageVariants}
            animate={isExpand ? 'expanded' : 'collapsed'}
            transition={springTransition}
            layout
          />
        </motion.div>
        <motion.p
          className={clsx(
            'font-preBold whitespace-pre-line break-keep',
            isExpand ? 'text-xl text-center' : 'text-lg text-start'
          )}
          variants={textVariants}
          animate={isExpand ? 'expanded' : 'collapsed'}
          transition={springTransition}
          layout
        >
          {gptChat}
        </motion.p>
      </motion.div>
      <motion.div layout transition={springTransition}>
        <VoiceAnimation isRecording={isRecording} volume={volume} />
      </motion.div>
      <motion.div
        className={clsx(
          'font-preSemiBold text-center text-gray-400 break-keep',
          handleUserChatFontSize()
        )}
        layout
        transition={springTransition}
      >
        &quot;{userChat}&quot;
      </motion.div>
    </motion.div>
  );
};

export default ChatContainer;
