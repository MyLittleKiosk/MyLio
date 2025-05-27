import ChatContainer from '@/components/Chat/ChatContainer';
import Loading from '@/components/common/Loading';
import { useLocation } from 'react-router-dom';
import { useEffect } from 'react';
import { useTTS } from '@/service/queries/voice';
import useKioskStore from '@/stores/useKioskStore';

interface Props {
  userChat: string;
  gptChat: string;
  isPending: boolean;
}
/**
 * Clova 테스트 페이지
 */
const Main = ({ userChat, gptChat, isPending }: Props) => {
  const location = useLocation();
  const { mutate: tts } = useTTS();
  const { isMute } = useKioskStore();
  useEffect(() => {
    if (!isPending && !isMute) {
      tts(gptChat);
    }
  }, [isPending]);
  return (
    <div className='flex flex-col items-center justify-center p-4 '>
      {isPending ? (
        <Loading />
      ) : (
        <ChatContainer
          userChat={userChat}
          gptChat={gptChat}
          isExpand={location.pathname === '/kiosk'}
        />
      )}
    </div>
  );
};

export default Main;
