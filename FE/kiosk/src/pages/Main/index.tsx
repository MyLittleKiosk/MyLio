import ChatContainer from '@/components/Chat/ChatContainer';
import Loading from '@/components/common/Loading';
import { useLocation } from 'react-router-dom';

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
