import lio from '@/assets/images/ListenLio.png';
import clsx from 'clsx';
import VoiceAnimation from '../VoiceAnimation';

interface Props {
  userChat: string;
  gptChat: string;
  isRecording: boolean;
  volume: number;
  isExpand: boolean; // 하단 컨텐츠가 있으면 true로 받아옴
}

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
    <div className='w-full h-full px-10 flex flex-col items-center gap-5'>
      <div
        className={clsx(
          'h-full flex items-center justify-center transition-all ease-in-out duration-800',
          isExpand ? 'flex-col  gap-10' : 'flex-row gap-4'
        )}
      >
        <div
          className='w-fit p-2 flex justify-center items-center bg-white rounded-full'
          style={{ boxShadow: 'inset 0px 0px 10px rgba(0, 0, 0, 0.25)' }}
        >
          <img
            src={lio}
            alt='img'
            className={clsx(
              'object-cover transition-all ease-in-out duration-500',
              isExpand ? 'size-[400px]' : 'size-[100px]'
            )}
            loading='lazy'
          />
        </div>
        <p
          className={clsx(
            'font-bold whitespace-pre-line break-keep',
            isExpand ? 'text-xl text-center' : 'text-lg text-start'
          )}
        >
          {gptChat}
        </p>
      </div>
      <div>
        <VoiceAnimation isRecording={isRecording} volume={volume} />
      </div>
      <div
        className={clsx(
          'font-semibold text-center text-gray-400 break-keep',
          handleUserChatFontSize()
        )}
      >
        &quot;{userChat}&quot;
      </div>
    </div>
  );
};

export default ChatContainer;
