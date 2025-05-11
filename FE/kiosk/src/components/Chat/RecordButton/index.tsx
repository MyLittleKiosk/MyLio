import mic from '@/assets/icons/mic.svg';
import { useAudioRecord } from '@/hooks/useAudioRecord';
import { sendAudioToClova } from '@/service/apis/clova';
import { useState } from 'react';

interface Props {
  onRecognitionResult: (text: string) => void;
}

const RecordButton = ({ onRecognitionResult }: Props) => {
  const { isRecording, startRecording, stopRecording } = useAudioRecord();
  const [isProcessing, setIsProcessing] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);

  // 녹음된 오디오를 Clova로 전송하는 함수
  async function handleSendToClova(audioBlob: Blob) {
    if (!audioBlob) {
      setError('녹음된 오디오가 없습니다.');
      return;
    }

    try {
      setIsProcessing(true);
      setError(null);

      console.log('오디오 Blob 정보:', {
        size: audioBlob.size,
        type: audioBlob.type,
      });

      // 오디오 데이터가 너무 작으면 오류 표시 (거의 껐다 킨 경우)
      if (audioBlob.size < 1000) {
        setError('녹음된 오디오가 너무 짧습니다. 더 긴 녹음을 시도해주세요.');
        setIsProcessing(false);
        return;
      }

      console.log('FastAPI 서버로 오디오 전송 시도...');

      // FastAPI 백엔드로 오디오 전송
      const result = await sendAudioToClova(audioBlob);

      console.log('FastAPI 응답 수신:', result);

      // 백엔드가 반환한 데이터에서 직접 텍스트 추출
      if (result.status === 'success' && result.text) {
        onRecognitionResult(result.text);
      } else {
        // 백엔드 응답 메시지 또는 기본 메시지 표시
        setError('인식 결과가 없거나 오류가 발생했습니다.');
      }
    } catch (err) {
      console.error('Clova 처리 중 오류 발생:', err);
      setError('음성 인식 중 오류가 발생했습니다.');
    } finally {
      setIsProcessing(false);
    }
  }

  // 버튼을 누르고 있는 동안 녹음하는 핸들러
  async function handlePressStart() {
    setError(null);
    // 새 녹음 시작 전에 이전 오디오 상태 초기화
    await startRecording();
  }

  // 버튼을 떼면 녹음 중지 및 Clova로 자동 전송
  async function handlePressEnd() {
    if (isRecording) {
      try {
        // 녹음 중지하고 Blob 받기
        const audioBlob = await stopRecording();

        console.log('녹음 완료, 오디오 Blob:', audioBlob);

        // 약간의 지연 후 서버로 전송 (오디오 처리 완료 보장)
        setTimeout(() => {
          if (audioBlob) {
            handleSendToClova(audioBlob);
          }
        }, 300);
      } catch (err) {
        console.error('녹음 중지 중 오류:', err);
        setError('녹음을 중지하는 중 오류가 발생했습니다.');
      }
    }
  }

  return (
    <button
      onMouseDown={handlePressStart}
      onMouseUp={handlePressEnd}
      onTouchStart={handlePressStart}
      onTouchEnd={handlePressEnd}
      className={`absolute bottom-10 right-10 bg-white rounded-full p-2 flex justify-center items-center transition-all ${
        isRecording ? 'scale-110 bg-red-100' : 'hover:bg-gray-100'
      }`}
      disabled={isProcessing}
    >
      <img src={mic} alt='microphone' className='w-10 h-10' />
      {error && (
        <div className='absolute bottom-full right-0 mb-2 p-2 bg-red-100 text-red-700 rounded-md text-sm whitespace-nowrap'>
          {error}
        </div>
      )}
    </button>
  );
};

export default RecordButton;
