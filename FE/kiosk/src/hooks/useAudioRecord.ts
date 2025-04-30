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
 */
export function useAudioRecord(): {
  isRecording: boolean;
  startRecording: () => Promise<void>;
  stopRecording: () => Promise<Blob>;
} {
  const [isRecording, setIsRecording] = useState<boolean>(false);
  const mediaRecorderRef = useRef<MediaRecorder>(null);
  const audioChunksRef = useRef<Blob[]>([]);
  const recordingPromiseRef = useRef<(value: Blob) => void>(() => {});
  const streamRef = useRef<MediaStream>(null);

  const startRecording = async () => {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({
        audio: {
          echoCancellation: true,
          noiseSuppression: true,
          autoGainControl: false,
        },
      });
      streamRef.current = stream;

      try {
        mediaRecorderRef.current = new MediaRecorder(stream);
        console.log('Using default MediaRecorder.');
      } catch (e) {
        console.error('Error creating MediaRecorder:', e);
        throw new Error('MediaRecorder 생성에 실패했습니다.');
      }

      audioChunksRef.current = [];
      mediaRecorderRef.current.ondataavailable = (event: BlobEvent) => {
        if (event.data.size > 0) {
          audioChunksRef.current.push(event.data);
        }
      };
      mediaRecorderRef.current.start();
      setIsRecording(true);
    } catch (e: unknown) {
      if (e instanceof Error) {
        throw new Error(e.message);
      } else {
        throw new Error('알 수 없는 에러 발생');
      }
    }
  };
  const stopRecording = (): Promise<Blob> => {
    return new Promise<Blob>((resolve) => {
      recordingPromiseRef.current = resolve;

      if (streamRef.current) {
        streamRef.current.getTracks().forEach((track) => {
          track.stop();
        });
      }

      if (mediaRecorderRef.current) {
        mediaRecorderRef.current.onstop = () => {
          const audioBlob = new Blob(audioChunksRef.current, {
            type: 'audio/wav',
          });
          resolve(audioBlob);
        };
        mediaRecorderRef.current.stop();
      }
      setIsRecording(false);
    });
  };

  return { isRecording, startRecording, stopRecording };
}
