import VoiceAnimation from '@/components/Chat/VoiceAnimation';
import { sendAudioToClova } from '@/service/apis/clova';
import { ClovaResponse } from '@/types/clova';
import { AxiosError } from 'axios';
import { useState } from 'react';
import { useAudioRecord } from '../../hooks/useAudioRecord';

const ClovaPage = () => {
  const { isRecording, startRecording, stopRecording, volume } =
    useAudioRecord();
  const [recognitionResult, setRecognitionResult] = useState<string>('');
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

      // Blob URL에서 실제 Blob 데이터 가져오

      console.log('오디오 Blob 정보:', {
        size: audioBlob.size,
        type: audioBlob.type,
      });

      // 오디오 데이터가 너무 작으면 오류 표시 (거의 껏다 킨 경우)
      if (audioBlob.size < 1000) {
        setError('녹음된 오디오가 너무 짧습니다. 더 긴 녹음을 시도해주세요.');
        setIsProcessing(false);
        return;
      }

      console.log('FastAPI 서버로 오디오 전송 시도...');

      // FastAPI 백엔드로 오디오 전송
      const result: ClovaResponse = await sendAudioToClova(audioBlob);

      console.log('FastAPI 응답 수신:', result);

      // 백엔드가 반환한 데이터에서 직접 텍스트 추출
      if (result.status === 'success' && result.text) {
        setRecognitionResult(result.text);
      } else {
        // 백엔드 응답 메시지 또는 기본 메시지 표시
        setRecognitionResult('인식 결과가 없거나 오류가 발생했습니다.');
      }
    } catch (err) {
      // 상황별 에러 문구 표현
      console.error('Clova 처리 중 오류 발생:', err);

      if (err instanceof AxiosError) {
        console.error('Axios 에러 상세 정보:', {
          status: err.response?.status,
          data: err.response?.data,
          message: err.message,
          config: {
            url: err.config?.url,
            method: err.config?.method,
            baseURL: err.config?.baseURL,
          },
        });

        if (err.response?.status === 422) {
          setError(
            '서버가 오디오 형식을 처리할 수 없습니다. 지원되는 형식은 WAV 또는 MP3입니다.'
          );
        } else if (err.response?.status === 400) {
          setError(
            '지원되지 않는 파일 형식입니다. WAV 또는 MP3 형식으로 녹음해주세요.'
          );
        } else if (err.code === 'ECONNABORTED') {
          setError(
            '서버 요청 시간이 초과되었습니다. 네트워크 연결을 확인해주세요.'
          );
        } else if (err.code === 'ERR_NETWORK') {
          setError(
            '서버에 연결할 수 없습니다. FastAPI 서버가 실행 중인지 확인해주세요. (http://localhost:8000)'
          );
        } else {
          setError(`서버 통신 오류: ${err.message}`);
        }
      } else {
        setError(
          `오디오 처리 중 오류가 발생했습니다: ${err instanceof Error ? err.message : String(err)}`
        );
      }
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
        // 녹음 중지하고 URL 받기
        const audioUrl = await stopRecording();

        console.log('녹음 완료, 오디오 URL:', audioUrl);

        // 약간의 지연 후 서버로 전송 (오디오 처리 완료 보장)
        setTimeout(() => {
          if (audioUrl) {
            handleSendToClova(audioUrl);
          }
        }, 300);
      } catch (err) {
        console.error('녹음 중지 중 오류:', err);
        setError('녹음을 중지하는 중 오류가 발생했습니다.');
      }
    }
  }

  // 오디오 재생을 위한 소스 선택 (현재 녹음된 오디오 우선)

  return (
    <div className='flex flex-col items-center justify-center min-h-screen p-4 bg-gray-100'>
      <div className='w-full max-w-md p-6 bg-white rounded-lg shadow-md'>
        <h1 className='text-2xl font-bold text-center mb-6'>
          Clova 음성 인식 테스트
        </h1>

        <div className='mb-6'>
          <div className='flex justify-center mb-4'>
            <button
              onMouseDown={handlePressStart}
              onMouseUp={handlePressEnd}
              onTouchStart={handlePressStart}
              onTouchEnd={handlePressEnd}
              className={`px-6 py-2 rounded-full font-medium ${
                isRecording
                  ? 'bg-red-500 text-white scale-110 transition-all'
                  : 'bg-blue-500 hover:bg-blue-600 text-white transition-all'
              }`}
              disabled={isProcessing}
            >
              {isRecording ? (
                <div>
                  <span>말하는 중...</span>
                </div>
              ) : (
                '눌러서 말하기'
              )}
            </button>
          </div>
          <div className='flex justify-center'>
            <VoiceAnimation isRecording={isRecording} volume={volume} />
          </div>

          <div className='mb-4'>
            <p className='text-sm font-medium mb-2'>녹음된 오디오:</p>
            {isProcessing ? (
              <p className='text-xs text-blue-500 mt-1'>
                음성을 처리하는 중...
              </p>
            ) : (
              <button
                className='text-xs text-blue-500 mt-1 underline'
                disabled={isProcessing}
              >
                다시 분석하기
              </button>
            )}
          </div>
        </div>

        {isProcessing && (
          <div className='p-3 mb-4 text-sm text-blue-700 bg-blue-100 rounded-md'>
            음성을 처리하는 중...
          </div>
        )}

        {error && (
          <div className='p-3 mb-4 text-sm text-red-700 bg-red-100 rounded-md'>
            {error}
          </div>
        )}

        {recognitionResult && (
          <div className='p-4 bg-gray-50 rounded-md'>
            <h2 className='text-lg font-medium mb-2'>인식 결과:</h2>
            <p className='text-gray-700'>{recognitionResult}</p>
          </div>
        )}
      </div>
    </div>
  );
};

export default ClovaPage;
