import ChatContainer from '@/components/Chat/ChatContainer';
import { useAudioRecord } from '@/hooks/useAudioRecord';
import { gcpTts } from '@/service/apis/voice';
import { useState } from 'react';
import { useLocation } from 'react-router-dom';

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
  const [audio, setAudio] = useState<string>('');

  return (
    <div className='flex flex-col items-center justify-center p-4 '>
      <ChatContainer
        userChat={userChat}
        gptChat={gptChat}
        isRecording={isRecording}
        volume={volume}
        isExpand={location.pathname === '/kiosk'}
      />
      <button
        onClick={async () => {
          const audio = await gcpTts(
            '아메리카노 (온도: Hot, 사이즈: S)를 장바구니에 담았어요.'
          );
          setAudio(URL.createObjectURL(audio.data));
          console.log('테스트');
        }}
      >
        테스트
      </button>
      {audio && <audio src={audio} autoPlay />}
    </div>
  );
};

export default Main;
