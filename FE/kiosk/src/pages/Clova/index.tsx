import {
  getClovaRecognitionResult,
  sendAudioToClova,
} from '@/service/apis/clova';
import React, { useState } from 'react';
import { useRecord } from '../../hooks/useAudioRecord';

const ClovaPage: React.FC = () => {
  const { isRecording, startRecording, audio, stopRecording } = useRecord();
  const [recognitionResult, setRecognitionResult] = useState<string>('');
  const [isProcessing, setIsProcessing] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);

  // 녹음된 오디오를 Clova로 전송하는 함수
  const handleSendToClova = async () => {
    if (!audio) {
      setError('녹음된 오디오가 없습니다.');
      return;
    }

    try {
      setIsProcessing(true);
      setError(null);

      // Blob URL에서 실제 Blob 데이터 가져오기
      const response = await fetch(audio);
      const audioBlob = await response.blob();

      // Clova API로 오디오 전송
      const result = await sendAudioToClova(audioBlob);

      // 결과 처리
      if (result.requestId) {
        // 비동기 처리인 경우 결과 조회
        const recognitionResult = await getClovaRecognitionResult(
          result.requestId
        );
        setRecognitionResult(recognitionResult.text || '인식 결과가 없습니다.');
      } else {
        // 동기 처리인 경우 바로 결과 표시
        setRecognitionResult(result.message || '인식 결과가 없습니다.');
      }
    } catch (err) {
      console.error('Clova 처리 중 오류 발생:', err);
      setError('오디오 처리 중 오류가 발생했습니다.');
    } finally {
      setIsProcessing(false);
    }
  };

  return (
    <div className='flex flex-col items-center justify-center min-h-screen p-4 bg-gray-100'>
      <div className='w-full max-w-md p-6 bg-white rounded-lg shadow-md'>
        <h1 className='text-2xl font-bold text-center mb-6'>
          Clova 음성 인식 테스트
        </h1>

        <div className='mb-6'>
          <div className='flex justify-center mb-4'>
            <button
              onClick={isRecording ? stopRecording : startRecording}
              className={`px-6 py-2 rounded-full font-medium ${
                isRecording
                  ? 'bg-red-500 hover:bg-red-600 text-white'
                  : 'bg-blue-500 hover:bg-blue-600 text-white'
              }`}
              disabled={isProcessing}
            >
              {isRecording ? '녹음 중지' : '녹음 시작'}
            </button>
          </div>

          {audio && (
            <div className='mb-4'>
              <p className='text-sm font-medium mb-2'>녹음된 오디오:</p>
              <audio controls src={audio} className='w-full' />
            </div>
          )}

          <button
            onClick={handleSendToClova}
            className={`w-full py-2 rounded-md font-medium ${
              isProcessing || !audio
                ? 'bg-gray-300 cursor-not-allowed'
                : 'bg-green-500 hover:bg-green-600 text-white'
            }`}
            disabled={isProcessing || !audio}
          >
            {isProcessing ? '처리 중...' : 'Clova로 전송'}
          </button>
        </div>

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
