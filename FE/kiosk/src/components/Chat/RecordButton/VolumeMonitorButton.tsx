import mic from '@/assets/images/mic.png';
import { sendAudioToClova } from '@/service/apis/voice';
import audioStore from '@/stores/audioStore';
import clsx from 'clsx';
import { useState, useEffect, useRef } from 'react';

interface Props {
  onRecognitionResult: (text: string) => void;
}

const VolumeMonitorButton = ({ onRecognitionResult }: Props) => {
  const isRecording = audioStore((s) => s.isRecording);
  const startRecording = audioStore((s) => s.startRecording);
  const stopRecording = audioStore((s) => s.stopRecording);

  const [isProcessing, setIsProcessing] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);
  const [isMonitoring, setIsMonitoring] = useState<boolean>(false);
  const [currentVolume, setCurrentVolume] = useState<number>(0);

  const audioContextRef = useRef<AudioContext | null>(null);
  const analyserRef = useRef<AnalyserNode | null>(null);
  const mediaStreamRef = useRef<MediaStream | null>(null);
  const animationFrameRef = useRef<number | null>(null);
  const silenceStartTimeRef = useRef<number>(0);
  const lastRecordingStartRef = useRef<number>(0);
  const isRecordingRef = useRef<boolean>(false);

  // 볼륨 임계값 설정 (0-1 사이 값)
  const VOLUME_THRESHOLD = 0.25;
  // 무음 감지 후 녹음 종료까지 대기 시간 (ms)
  const SILENCE_DURATION = 800;
  // 녹음 시작 간 최소 대기 시간 (ms)
  const MIN_RECORDING_INTERVAL = 1000;

  // isRecording 상태가 변경될 때마다 ref 업데이트
  useEffect(() => {
    isRecordingRef.current = isRecording;
  }, [isRecording]);

  // 마이크 모니터링 시작
  const startMonitoring = async () => {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      mediaStreamRef.current = stream;

      const audioContext = new AudioContext();
      audioContextRef.current = audioContext;

      const analyser = audioContext.createAnalyser();
      analyser.fftSize = 256;
      analyserRef.current = analyser;

      const source = audioContext.createMediaStreamSource(stream);
      source.connect(analyser);

      setIsMonitoring(true);
      console.log('마이크 모니터링 시작됨');
      console.log('현재 임계값:', VOLUME_THRESHOLD);
      checkVolume();
    } catch (err) {
      console.error('마이크 접근 오류:', err);
      setError('마이크 접근에 실패했습니다.');
    }
  };

  // 마이크 모니터링 중지
  const stopMonitoring = () => {
    if (animationFrameRef.current) {
      cancelAnimationFrame(animationFrameRef.current);
    }
    if (mediaStreamRef.current) {
      mediaStreamRef.current.getTracks().forEach((track) => track.stop());
    }
    if (audioContextRef.current) {
      audioContextRef.current.close();
    }
    setIsMonitoring(false);
    console.log('마이크 모니터링 중지됨');
  };

  // 볼륨 체크 및 녹음 제어
  const checkVolume = async () => {
    if (!analyserRef.current) return;

    const dataArray = new Uint8Array(analyserRef.current.frequencyBinCount);
    analyserRef.current.getByteFrequencyData(dataArray);

    // 볼륨 계산 (평균값)
    const average = dataArray.reduce((a, b) => a + b) / dataArray.length;
    const volume = average / 255; // 0-1 사이 값으로 정규화
    setCurrentVolume(volume);

    const now = Date.now();

    if (!isRecordingRef.current) {
      // 마지막 녹음 시작으로부터 일정 시간이 지났는지 확인
      if (now - lastRecordingStartRef.current < MIN_RECORDING_INTERVAL) {
        animationFrameRef.current = requestAnimationFrame(checkVolume);
        return;
      }

      // 녹음 중이 아닐 때는 임계값 초과하면 즉시 녹음 시작
      if (volume > VOLUME_THRESHOLD) {
        console.log(
          '볼륨 임계값 초과, 녹음 시작 시도:',
          volume,
          '>',
          VOLUME_THRESHOLD
        );
        try {
          await startRecording();
          lastRecordingStartRef.current = now;
          console.log('녹음 시작 성공');
          silenceStartTimeRef.current = 0; // 무음 타이머 초기화
        } catch (err) {
          console.error('녹음 시작 실패:', err);
        }
      }
    } else {
      // 녹음 중일 때는 임계값 이하로 내려가면 무음 타이머 시작
      console.log('녹음 중일 때 볼륨:', volume);
      if (volume <= VOLUME_THRESHOLD) {
        // 무음이 시작된 시점 기록
        if (silenceStartTimeRef.current === 0) {
          console.log(
            '무음 감지, 타이머 시작:',
            volume,
            '<=',
            VOLUME_THRESHOLD
          );
          silenceStartTimeRef.current = now;
        }

        const silenceDuration = now - silenceStartTimeRef.current;
        console.log('무음 지속 시간:', silenceDuration, 'ms');

        // 무음이 일정 시간 이상 지속되면 녹음 종료
        if (silenceDuration >= SILENCE_DURATION) {
          console.log(
            '무음 지속 시간 초과, 녹음 종료 시도:',
            silenceDuration,
            'ms'
          );
          try {
            await handleRecordingStop();
            console.log('녹음 종료 성공');
            silenceStartTimeRef.current = 0;
          } catch (err) {
            console.error('녹음 종료 실패:', err);
          }
        }
      } else {
        // 볼륨이 다시 임계값을 넘으면 무음 타이머 리셋
        if (silenceStartTimeRef.current !== 0) {
          console.log(
            '볼륨 임계값 초과, 무음 타이머 리셋:',
            volume,
            '>',
            VOLUME_THRESHOLD
          );
          silenceStartTimeRef.current = 0;
        }
      }
    }

    animationFrameRef.current = requestAnimationFrame(checkVolume);
  };

  // 녹음 중지 및 처리
  const handleRecordingStop = async () => {
    if (isRecordingRef.current) {
      try {
        console.log('녹음 중지 시작');
        const audioBlob = await stopRecording();
        console.log('녹음 중지 완료, 오디오 Blob:', audioBlob);

        if (audioBlob) {
          handleSendToClova(audioBlob);
        }
      } catch (err) {
        console.error('녹음 중지 중 오류:', err);
        setError('녹음을 중지하는 중 오류가 발생했습니다.');
      }
    }
  };

  // 컴포넌트 마운트 시 마이크 모니터링 시작
  useEffect(() => {
    startMonitoring();
    return () => {
      stopMonitoring();
    };
  }, []);

  // 녹음된 오디오를 Clova로 전송하는 함수
  async function handleSendToClova(audioBlob: Blob) {
    if (!audioBlob) {
      setError('녹음된 오디오가 없습니다.');
      return;
    }

    try {
      setIsProcessing(true);
      setError(null);

      if (audioBlob.size < 1000) {
        setError('녹음된 오디오가 너무 짧습니다.');
        setIsProcessing(false);
        return;
      }

      const result = await sendAudioToClova(audioBlob);

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
  }

  return (
    <div className='flex flex-col items-center gap-2'>
      <button
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
      </button>
      <div className='text-sm'>
        <div>모니터링 상태: {isMonitoring ? '활성화' : '비활성화'}</div>
        <div>현재 볼륨: {(currentVolume * 100).toFixed(1)}%</div>
        <div>임계값: {(VOLUME_THRESHOLD * 100).toFixed(1)}%</div>
        <div>녹음 상태: {isRecording ? '녹음 중' : '대기 중'}</div>
        {isRecording && silenceStartTimeRef.current !== 0 && (
          <div>
            무음 지속:{' '}
            {((Date.now() - silenceStartTimeRef.current) / 1000).toFixed(1)}초
          </div>
        )}
      </div>
      {error && (
        <div className='p-2 bg-red-100 text-red-700 rounded-md text-sm'>
          {error}
        </div>
      )}
    </div>
  );
};

export default VolumeMonitorButton;
