import mic from '@/assets/images/mic.png';
import { sendAudioToClova } from '@/service/apis/voice';
import audioStore from '@/stores/audioStore';
import clsx from 'clsx';
import { useState, useRef, useEffect } from 'react';

// 상수 정의
const AUDIO_SETTINGS = {
  PREBUFFER_SEC: 1,
  BUFFER_SIZE: 2048,
  MIN_RECORDING_SIZE: 1000,
  PROCESSING_DELAY: 300,
} as const;

interface Props {
  onRecognitionResult: (text: string) => void;
}

const RecordButton = ({ onRecognitionResult }: Props) => {
  // 상태 관리
  const [isProcessing, setIsProcessing] = useState(false);
  const [error, setError] = useState<string | null>(null);

  // 오디오 관련 refs
  const audioContextRef = useRef<AudioContext | null>(null);
  const mediaStreamRef = useRef<MediaStream | null>(null);
  const scriptNodeRef = useRef<ScriptProcessorNode | null>(null);
  const preBufferRef = useRef<Float32Array[]>([]);
  const isRecordingRef = useRef(false);

  // Zustand 스토어
  const isRecording = audioStore((s) => s.isRecording);
  const startRecording = audioStore((s) => s.startRecording);
  const stopRecording = audioStore((s) => s.stopRecording);

  // isRecording 상태 동기화
  useEffect(() => {
    isRecordingRef.current = isRecording;
  }, [isRecording]);

  // 오디오 모니터링 시작
  const startMonitoring = async () => {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      mediaStreamRef.current = stream;

      const audioContext = new AudioContext();
      audioContextRef.current = audioContext;

      const source = audioContext.createMediaStreamSource(stream);
      const scriptNode = audioContext.createScriptProcessor(
        AUDIO_SETTINGS.BUFFER_SIZE,
        1,
        1
      );
      scriptNodeRef.current = scriptNode;

      source.connect(scriptNode);
      scriptNode.connect(audioContext.destination);

      scriptNode.onaudioprocess = (e) => {
        if (!isRecordingRef.current) {
          const inputData = e.inputBuffer.getChannelData(0);
          preBufferRef.current.push(new Float32Array(inputData));

          // 프리버퍼 크기 제한
          const maxBufferLength =
            audioContext.sampleRate * AUDIO_SETTINGS.PREBUFFER_SEC;
          let currentLength = preBufferRef.current.reduce(
            (sum, arr) => sum + arr.length,
            0
          );

          while (currentLength > maxBufferLength) {
            const removed = preBufferRef.current.shift();
            if (removed) {
              currentLength -= removed.length;
            }
          }

          // 프리버퍼 상태 로깅
          if (currentLength > 0 && Date.now() % 1000 < 50) {
            console.log('프리버퍼 상태:', {
              bufferCount: preBufferRef.current.length,
              totalSamples: currentLength,
              maxSamples: maxBufferLength,
              sampleRate: audioContext.sampleRate,
              bufferSizes: preBufferRef.current.map((arr) => arr.length),
            });
          }
        }
      };

      console.log('오디오 모니터링 시작됨');
    } catch (err) {
      console.error('마이크 접근 오류:', err);
      setError('마이크 접근에 실패했습니다.');
    }
  };

  // 오디오 모니터링 중지
  const stopMonitoring = () => {
    if (mediaStreamRef.current) {
      mediaStreamRef.current.getTracks().forEach((track) => track.stop());
    }
    if (audioContextRef.current) {
      audioContextRef.current.close();
    }
    if (scriptNodeRef.current) {
      scriptNodeRef.current.disconnect();
    }
    preBufferRef.current = [];
    console.log('오디오 모니터링 중지됨');
  };

  // 컴포넌트 마운트/언마운트 처리
  useEffect(() => {
    startMonitoring();
    return () => stopMonitoring();
  }, []);

  // Clova로 오디오 전송
  const handleSendToClova = async (audioBlob: Blob) => {
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

      if (audioBlob.size < AUDIO_SETTINGS.MIN_RECORDING_SIZE) {
        setError('녹음된 오디오가 너무 짧습니다. 더 긴 녹음을 시도해주세요.');
        setIsProcessing(false);
        return;
      }

      const result = await sendAudioToClova(audioBlob);
      console.log('FastAPI 응답 수신:', result);

      if (result.status === 'success' && result.text) {
        onRecognitionResult(result.text);
      } else {
        setError('인식 결과가 없거나 오류가 발생했습니다.');
      }
    } catch (err) {
      console.error('Clova 처리 중 오류 발생:', err);
      setError('음성 인식 중 오류가 발생했습니다.');
    } finally {
      setIsProcessing(false);
    }
  };

  // 녹음 시작
  const handlePressStart = async () => {
    setError(null);
    await startRecording();
  };

  // 녹음 중지
  const handlePressEnd = async () => {
    if (isRecording) {
      try {
        const preBufferSnapshot = preBufferRef.current.map(
          (buffer) => new Float32Array(buffer)
        );
        const totalSamples = preBufferSnapshot.reduce(
          (sum, arr) => sum + arr.length,
          0
        );

        console.log('프리버퍼 스냅샷:', {
          bufferCount: preBufferSnapshot.length,
          totalSamples,
          sampleRate: audioContextRef.current?.sampleRate,
          expectedSamples: audioContextRef.current?.sampleRate || 0,
          bufferSizes: preBufferSnapshot.map((arr) => arr.length),
        });

        if (totalSamples < (audioContextRef.current?.sampleRate || 0) * 0.5) {
          console.warn('프리버퍼가 너무 작습니다:', totalSamples, 'samples');
        }

        const audioBlob = await stopRecording(preBufferSnapshot);
        console.log('녹음 완료, 오디오 Blob:', audioBlob);

        setTimeout(() => {
          if (audioBlob) {
            handleSendToClova(audioBlob);
          }
        }, AUDIO_SETTINGS.PROCESSING_DELAY);
      } catch (err) {
        console.error('녹음 중지 중 오류:', err);
        setError('녹음을 중지하는 중 오류가 발생했습니다.');
      }
    }
  };

  return (
    <button
      onMouseDown={handlePressStart}
      onMouseUp={handlePressEnd}
      onTouchStart={handlePressStart}
      onTouchEnd={handlePressEnd}
      className={clsx(
        'p-2 w-16 h-16 shadow-lg rounded-full flex justify-center items-center transition-all',
        'animate-[pulse_1s_ease-in-out_infinite]',
        isRecording
          ? 'scale-90 shadow-inner shadow-green-500 bg-green-100'
          : 'bg-white hover:bg-gray-100'
      )}
      disabled={isProcessing}
    >
      <img src={mic} alt='microphone' className='w-full h-full' />
      {error && (
        <div className='absolute bottom-full right-0 mb-2 p-2 bg-red-100 text-red-700 rounded-md text-sm whitespace-nowrap'>
          {error}
        </div>
      )}
    </button>
  );
};

export default RecordButton;
