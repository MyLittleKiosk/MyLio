import { sendAudioToClova } from '@/service/apis/voice';
import audioStore from '@/stores/audioStore';
import { useEffect, useRef, forwardRef, useImperativeHandle } from 'react';

interface Props {
  onRecognitionResult: (text: string) => void;
  setRecordingMethod: (method: 'pitch' | 'hold') => void;
  onRecordStart: () => void;
  onRecordStop: () => void;
  onPreBufferUpdate: (buffer: Float32Array[]) => void;
}

export interface PitchDetectorRef {
  reset: () => void;
}

const PitchDetector = forwardRef<PitchDetectorRef, Props>(
  ({ onRecognitionResult, setRecordingMethod }, ref) => {
    const isRecording = audioStore((s) => s.isRecording);
    const startRecording = audioStore((s) => s.startRecording);
    const stopRecording = audioStore((s) => s.stopRecording);

    const startRecordingRef = useRef(startRecording);
    const setRecordingMethodRef = useRef(setRecordingMethod);

    const audioContextRef = useRef<AudioContext | null>(null);
    const analyserRef = useRef<AnalyserNode | null>(null);
    const mediaStreamRef = useRef<MediaStream | null>(null);
    const animationFrameRef = useRef<number | null>(null);
    const silenceStartTimeRef = useRef<number>(0);
    const lastRecordingStartRef = useRef<number>(0);
    const isRecordingRef = useRef<boolean>(false);
    const preBufferRef = useRef<Float32Array[]>([]);
    const scriptNodeRef = useRef<ScriptProcessorNode | null>(null);

    // 볼륨 임계값 설정 (0-1 사이 값)
    const VOLUME_THRESHOLD = 0.2;
    // 무음 감지 후 녹음 종료까지 대기 시간 (ms)
    const SILENCE_DURATION = 800;
    // 녹음 시작 간 최소 대기 시간 (ms)
    const MIN_RECORDING_INTERVAL = 1000;
    // 프리버퍼 크기 (초)
    const PREBUFFER_SEC = 1;

    useEffect(() => {
      startRecordingRef.current = startRecording;
      setRecordingMethodRef.current = setRecordingMethod;
    }, [startRecording, setRecordingMethod]);

    // isRecording 상태가 변경될 때마다 ref 업데이트
    useEffect(() => {
      isRecordingRef.current = isRecording;
    }, [isRecording]);

    // 초기화 메서드
    const reset = async () => {
      // 먼저 현재 실행 중인 모니터링을 중지
      stopMonitoring();

      // 모든 상태 초기화
      silenceStartTimeRef.current = 0;
      lastRecordingStartRef.current = 0;
      preBufferRef.current = [];

      // 약간의 지연 후 모니터링 재시작
      setTimeout(() => {
        startMonitoring();
      }, 100);
    };

    // ref를 통해 외부에서 접근할 수 있는 메서드 노출
    useImperativeHandle(ref, () => ({
      reset,
    }));

    // 마이크 모니터링 시작
    const startMonitoring = async () => {
      try {
        // 이미 실행 중인 모니터링이 있다면 중지
        stopMonitoring();

        const stream = await navigator.mediaDevices.getUserMedia({
          audio: true,
        });
        mediaStreamRef.current = stream;

        const audioContext = new AudioContext();
        audioContextRef.current = audioContext;

        const analyser = audioContext.createAnalyser();
        analyser.fftSize = 256;
        analyserRef.current = analyser;

        const source = audioContext.createMediaStreamSource(stream);
        source.connect(analyser);

        setupScriptProcessor(audioContext, source);

        console.log('마이크 모니터링 시작됨');
        console.log('현재 임계값:', VOLUME_THRESHOLD);
        checkVolume();
      } catch (err) {
        console.error('마이크 접근 오류:', err);
      }
    };

    // 마이크 모니터링 중지
    const stopMonitoring = () => {
      if (animationFrameRef.current) {
        cancelAnimationFrame(animationFrameRef.current);
        animationFrameRef.current = null;
      }

      if (scriptNodeRef.current) {
        scriptNodeRef.current.disconnect();
        scriptNodeRef.current = null;
      }

      if (mediaStreamRef.current) {
        mediaStreamRef.current.getTracks().forEach((track) => track.stop());
        mediaStreamRef.current = null;
      }

      if (audioContextRef.current) {
        audioContextRef.current.close();
        audioContextRef.current = null;
      }

      analyserRef.current = null;
      preBufferRef.current = [];
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
            await startRecordingRef.current();
            setRecordingMethodRef.current('pitch');
            lastRecordingStartRef.current = now;
            console.log('녹음 시작 성공');
            silenceStartTimeRef.current = 0; // 무음 타이머 초기화
          } catch (err) {
            console.error('녹음 시작 실패:', err);
          }
        }
      } else {
        // 녹음 중일 때는 임계값 이하로 내려가면 무음 타이머 시작
        // console.log('녹음 중일 때 볼륨:', volume);
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
          // console.log('무음 지속 시간:', silenceDuration, 'ms');

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
          const preBufferSnapshot = preBufferRef.current.map((buffer) => {
            return new Float32Array(buffer);
          });

          const totalSamples = preBufferSnapshot.reduce(
            (sum, arr) => sum + arr.length,
            0
          );

          if (totalSamples < (audioContextRef.current?.sampleRate || 0) * 0.5) {
            console.warn('프리버퍼가 너무 작습니다:', totalSamples, 'samples');
          }

          const audioBlob = await stopRecording(preBufferSnapshot);
          console.log('녹음 중지 완료, 오디오 Blob:', audioBlob);

          if (audioBlob) {
            handleSendToClova(audioBlob);
            setRecordingMethodRef.current('pitch'); // 녹음 종료 후 recordingMethod를 'pitch'로 변경
          }
        } catch (err) {
          console.error('녹음 중지 중 오류:', err);
        }
      }
    };

    // ScriptProcessorNode 설정 (프리버퍼용)
    const setupScriptProcessor = (
      audioContext: AudioContext,
      source: MediaStreamAudioSourceNode
    ) => {
      const scriptNode = audioContext.createScriptProcessor(2048, 1, 1);
      scriptNodeRef.current = scriptNode;
      source.connect(scriptNode);
      scriptNode.connect(audioContext.destination);

      scriptNode.onaudioprocess = (e) => {
        if (!isRecordingRef.current) {
          const inputData = e.inputBuffer.getChannelData(0);
          // 새로운 Float32Array로 복사하여 저장
          preBufferRef.current.push(new Float32Array(inputData));

          // 프리버퍼 크기 제한 (1초)
          const maxBufferLength = audioContext.sampleRate * PREBUFFER_SEC;
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

          // // 프리버퍼 상태 로깅
          // if (currentLength > 0) {
          //   console.log('프리버퍼 상태:', {
          //     bufferCount: preBufferRef.current.length,
          //     totalSamples: currentLength,
          //     maxSamples: maxBufferLength,
          //     sampleRate: audioContext.sampleRate,
          //     bufferSizes: preBufferRef.current.map((arr) => arr.length),
          //   });
          // }
        }
      };
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
        return;
      }

      try {
        const result = await sendAudioToClova(audioBlob);

        if (result.status === 'success' && result.text) {
          onRecognitionResult(result.text);
        }
      } catch (err) {
        console.error('Clova 처리 중 오류 발생:', err);
      }
    }

    return null;
  }
);

PitchDetector.displayName = 'PitchDetector';

export default PitchDetector;
