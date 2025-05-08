import ChatContainer from '@/components/Chat/ChatContainer';
import { useLocation } from 'react-router-dom';

interface Props {
  userChat: string;
  gptChat: string;
  isRecording: boolean;
  volume: number;
}
/**
 * Clova 테스트 페이지
 */
const Main = ({ isRecording, volume }: Props) => {
  const location = useLocation();

  return (
    <div className='flex flex-col items-center justify-center p-4 '>
      <ChatContainer
        userChat={'아아 한 잔 줘'}
        gptChat={`무엇을 도와드릴까요?\n다양한 커피 메뉴를 소개해드릴게요.\n커피 메뉴를 선택해주세요.\n오늘의 메뉴로 청포도 아이스 티를 추천해드려요!`}
        isRecording={isRecording}
        volume={volume}
        isExpand={location.pathname === '/kiosk'}
      />
    </div>
  );
};

export default Main;
