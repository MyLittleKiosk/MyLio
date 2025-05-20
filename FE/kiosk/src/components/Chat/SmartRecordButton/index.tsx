import { createContext, useState, useRef, useEffect, ReactNode } from 'react';
import { sendAudioToClova } from '@/service/apis/voice';
import audioStore from '@/stores/audioStore';

// 상수 정의
const AUDIO_SETTINGS = {
  PREBUFFER_SEC: 1,
  BUFFER_SIZE: 2048,
  MIN_RECORDING_SIZE: 1000,
  PROCESSING_DELAY: 300,
  VOLUME_THRESHOLD: 0.1,
  SILENCE_DURATION: 800,
  MIN_RECORDING_INTERVAL: 1000,
} as const;

interface SmartRecordButtonContextType {
  isRecording: boolean;
  isProcessing: boolean;
  error: string | null;
  currentVolume: number;
  startRecording: () => Promise<void>;
  stopRecording: () => Promise<void>;
}

const SmartRecordButtonContext =
  createContext<SmartRecordButtonContextType | null>(null);

interface SmartRecordButtonProps {
  children: ReactNode;
  onRecognitionResult: (text: string) => void;
}

const SmartRecordButton = ({
  children,
  onRecognitionResult,
}: SmartRecordButtonProps) => {
  const [isProcessing, setIsProcessing] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [currentVolume, setCurrentVolume] = useState(0);

  const audioContextRef = useRef<AudioContext | null>(null);
  const analyserRef = useRef<AnalyserNode | null>(null);
  const mediaStreamRef = useRef<MediaStream | null>(null);
  const scriptNodeRef = useRef<ScriptProcessorNode | null>(null);
  const animationFrameRef = useRef<number | null>(null);
  const silenceStartTimeRef = useRef(0);
  const lastRecordingStartRef = useRef(0);
  const isRecordingRef = useRef(false);
  const preBufferRef = useRef<Float32Array[]>([]);

  const isRecording = audioStore((s) => s.isRecording);
  const startRecordingStore = audioStore((s) => s.startRecording);
  const stopRecordingStore = audioStore((s) => s.stopRecording);

  useEffect(() => {
    isRecordingRef.current = isRecording;
  }, [isRecording]);

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

      setupScriptProcessor(audioContext, source);
      checkVolume();
    } catch (err) {
      console.error('마이크 접근 오류:', err);
      setError('마이크 접근에 실패했습니다.');
    }
  };

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
    if (scriptNodeRef.current) {
      scriptNodeRef.current.disconnect();
    }
    preBufferRef.current = [];
  };

  const checkVolume = async () => {
    if (!analyserRef.current) return;

    const dataArray = new Uint8Array(analyserRef.current.frequencyBinCount);
    analyserRef.current.getByteFrequencyData(dataArray);

    const average = dataArray.reduce((a, b) => a + b) / dataArray.length;
    const volume = average / 255;
    setCurrentVolume(volume);

    const now = Date.now();

    if (!isRecordingRef.current) {
      if (
        now - lastRecordingStartRef.current <
        AUDIO_SETTINGS.MIN_RECORDING_INTERVAL
      ) {
        animationFrameRef.current = requestAnimationFrame(checkVolume);
        return;
      }

      if (volume > AUDIO_SETTINGS.VOLUME_THRESHOLD) {
        try {
          await startRecording();
          lastRecordingStartRef.current = now;
          silenceStartTimeRef.current = 0;
        } catch (err) {
          console.error('녹음 시작 실패:', err);
        }
      }
    } else {
      if (volume <= AUDIO_SETTINGS.VOLUME_THRESHOLD) {
        if (silenceStartTimeRef.current === 0) {
          silenceStartTimeRef.current = now;
        }

        const silenceDuration = now - silenceStartTimeRef.current;

        if (silenceDuration >= AUDIO_SETTINGS.SILENCE_DURATION) {
          try {
            await handleRecordingStop();
            silenceStartTimeRef.current = 0;
          } catch (err) {
            console.error('녹음 종료 실패:', err);
          }
        }
      } else {
        if (silenceStartTimeRef.current !== 0) {
          silenceStartTimeRef.current = 0;
        }
      }
    }

    animationFrameRef.current = requestAnimationFrame(checkVolume);
  };

  const setupScriptProcessor = (
    audioContext: AudioContext,
    source: MediaStreamAudioSourceNode
  ) => {
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
      }
    };
  };

  const startRecording = async () => {
    setError(null);
    await startRecordingStore();
  };

  const handleRecordingStop = async () => {
    if (isRecordingRef.current) {
      try {
        const preBufferSnapshot = preBufferRef.current.map(
          (buffer) => new Float32Array(buffer)
        );

        const totalSamples = preBufferSnapshot.reduce(
          (sum, arr) => sum + arr.length,
          0
        );

        if (totalSamples < (audioContextRef.current?.sampleRate || 0) * 0.5) {
          console.warn('프리버퍼가 너무 작습니다:', totalSamples, 'samples');
        }

        const audioBlob = await stopRecordingStore(preBufferSnapshot);

        if (audioBlob) {
          handleSendToClova(audioBlob);
        }
      } catch (err) {
        console.error('녹음 중지 중 오류:', err);
        setError('녹음을 중지하는 중 오류가 발생했습니다.');
      }
    }
  };

  const handleSendToClova = async (audioBlob: Blob) => {
    if (!audioBlob) {
      setError('녹음된 오디오가 없습니다.');
      return;
    }

    try {
      setIsProcessing(true);
      setError(null);

      if (audioBlob.size < AUDIO_SETTINGS.MIN_RECORDING_SIZE) {
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
  };

  useEffect(() => {
    startMonitoring();
    return () => stopMonitoring();
  }, []);

  const value = {
    isRecording,
    isProcessing,
    error,
    currentVolume,
    startRecording,
    stopRecording: handleRecordingStop,
  };

  return (
    <SmartRecordButtonContext.Provider value={value}>
      {children}
    </SmartRecordButtonContext.Provider>
  );
};

export default SmartRecordButton;
