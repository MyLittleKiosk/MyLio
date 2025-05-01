import { useRef, useState } from 'react';

/**
 * useAudioRecord 커스텀 훅은 브라우저에서 오디오 녹음을 시작하고, 녹음이 완료되면 오디오 Blob URL을 반환합니다.
 * @function useAudioRecord
 * @returns {Object} 녹음 상태와 관련된 함수 및 데이터를 포함하는 객체.
 * @property {boolean} isRecording - 현재 녹음 중인지 여부를 나타냅니다. 녹음 중이면 true, 그렇지 않으면 false입니다.
 * @property {() => Promise<void>} startRecording - 녹음을 시작하는 비동기 함수입니다.
 *   사용자가 마이크 접근 권한을 허용해야 하며, 이 함수 호출 시 MediaRecorder가 초기화되고 녹음이 시작됩니다.
 * @property {() => void} stopRecording - 녹음을 중지하는 함수입니다.
 *   녹음이 중지되면, 현재까지 수집된 오디오 청크를 기반으로 Blob이 생성되고, 해당 Blob의 URL이 상태에 저장됩니다.
 * @property {number} volume - 현재 녹음 중인 오디오의 볼륨 수준을 나타냅니다. 0에서 1 사이의 값으로, 0은 음소거 상태를 나타내고 1은 최대 볼륨을 나타냅니다.
 */
export function useAudioRecord(): {
  isRecording: boolean;
  startRecording: () => Promise<void>;
  stopRecording: () => Promise<Blob>;
  volume: number;
} {
  const [isRecording, setIsRecording] = useState<boolean>(false);
  const [volume, setVolume] = useState(0);

  const mediaRecorderRef = useRef<MediaRecorder>(null);
  const audioChunksRef = useRef<Blob[]>([]); // 녹음 중 오디오 청크 저장
  const recordingPromiseRef = useRef<(value: Blob) => void>(() => {}); // 녹음 완료 후 프로미스 해결
  const streamRef = useRef<MediaStream>(null); // 미디어 스트림 저장
  const audioContextRef = useRef<AudioContext | null>(null); // 오디오 컨텍스트 저장
  const analyserRef = useRef<AnalyserNode | null>(null); // 실시간 오디오 볼륨 분석기 -> 실시간 파형(주파수) 측정
  const dataArrayRef = useRef<Uint8Array | null>(null); // 오디오 신호 측정용 바이트 배열
  const animationFrameRef = useRef<number | null>(null); // 애니메이션 프레임 저장

  async function startRecording() {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({
        audio: {
          echoCancellation: true,
          noiseSuppression: true,
          autoGainControl: false,
        },
      });
      streamRef.current = stream;

      mediaRecorderRef.current = new MediaRecorder(stream);

      audioChunksRef.current = [];
      mediaRecorderRef.current.ondataavailable = (event: BlobEvent) => {
        if (event.data.size > 0) {
          audioChunksRef.current.push(event.data);
        }
      };
      mediaRecorderRef.current.start();
      setIsRecording(true);

      // 실시간 볼륨 측정 설정
      audioContextRef.current = new AudioContext();
      analyserRef.current = audioContextRef.current.createAnalyser();
      const bufferLength = analyserRef.current.frequencyBinCount;
      dataArrayRef.current = new Uint8Array(bufferLength);

      const source = audioContextRef.current.createMediaStreamSource(stream);
      source.connect(analyserRef.current);

      getVolume();
    } catch (e: unknown) {
      setIsRecording(false);
      if (e instanceof Error) {
        throw new Error(e.message);
      } else {
        throw new Error('알 수 없는 에러 발생');
      }
    }
  }

  async function stopRecording(): Promise<Blob> {
    return new Promise<Blob>((resolve) => {
      recordingPromiseRef.current = resolve;

      if (streamRef.current) {
        streamRef.current.getTracks().forEach((track) => {
          track.stop();
        });
        streamRef.current = null;
      }

      if (mediaRecorderRef.current) {
        mediaRecorderRef.current.onstop = () => {
          const audioBlob = new Blob(audioChunksRef.current, {
            type: 'audio/wav',
          });
          resolve(audioBlob);
        };
        mediaRecorderRef.current.stop();
        mediaRecorderRef.current = null;
      }

      if (animationFrameRef.current) {
        cancelAnimationFrame(animationFrameRef.current);
        animationFrameRef.current = null;
      }

      setIsRecording(false);
      setVolume(0);
    });
  }

  // 실시간 볼륨 측정
  function getVolume() {
    if (!analyserRef.current || !dataArrayRef.current) return;

    analyserRef.current.getByteTimeDomainData(dataArrayRef.current); // 마이크에서 들어오는 파형 데이터를 Uint8Array 형식으로 읽어옴
    console.log(dataArrayRef.current);
    // 진폭 차이 계산, 128 -> 음이 없는 상태
    let sum = 0;
    for (let i = 0; i < dataArrayRef.current.length; i++) {
      const v = dataArrayRef.current[i] - 128;
      sum += v * v;
    }

    // 평균값의 제곱근 -> RMS: 진폭 에너지
    const rms = Math.sqrt(sum / dataArrayRef.current.length);
    setVolume(rms);
    animationFrameRef.current = requestAnimationFrame(getVolume);
  }

  return { isRecording, startRecording, stopRecording, volume };
}
