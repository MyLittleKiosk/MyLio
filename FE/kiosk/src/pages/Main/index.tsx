import { useLocation } from 'react-router-dom';
import ChatContainer from '@/components/Chat/ChatContainer';
import { useAudioRecord } from '@/hooks/useAudioRecord';

interface Props {
  userChat: string;
  gptChat: string;
}
/**
 * Clova 테스트 페이지
 */
const Main = ({ userChat, gptChat }: Props) => {
  const location = useLocation();
  const { isRecording, volume } = useAudioRecord();

  return (
    <div className='flex flex-col items-center justify-center p-4 '>
      <ChatContainer
        userChat={userChat}
        gptChat={gptChat}
        isRecording={isRecording}
        volume={volume}
        isExpand={location.pathname === '/kiosk'}
      />
    </div>
  );
};

export default Main;
