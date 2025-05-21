import { create } from 'zustand';

// 상수 정의
const AUDIO_SETTINGS = {
  SAMPLE_RATE: 24000,
  CHANNELS: 1,
  BITS_PER_SAMPLE: 16,
  PREBUFFER_SEC: 1,
  MIN_RECORDING_SIZE: 1000,
  MEDIA_RECORDER_OPTIONS: {
    mimeType: 'audio/webm;codecs=opus',
    audioBitsPerSecond: 128000,
  },
} as const;

// 타입 정의
interface AudioState {
  isRecording: boolean;
  mediaRecorder: MediaRecorder | null;
  audioChunks: Blob[];
  volume: number;
  _refs: {
    audioCtx?: AudioContext;
    analyser?: AnalyserNode;
    dataArray?: Uint8Array;
    rafId?: number;
    stream?: MediaStream;
    lastVolumeUpdate?: number;
  };
  startRecording: () => Promise<void>;
  stopRecording: (preBuffer: Float32Array[]) => Promise<Blob>;
}

// 유틸리티 함수
const createAudioContext = () =>
  new AudioContext({ sampleRate: AUDIO_SETTINGS.SAMPLE_RATE });

const encodeWAV = (samples: Int16Array): Blob => {
  const buffer = new ArrayBuffer(44 + samples.length * 2);
  const view = new DataView(buffer);

  // WAV 헤더 작성
  const writeString = (offset: number, string: string) => {
    for (let i = 0; i < string.length; i++) {
      view.setUint8(offset + i, string.charCodeAt(i));
    }
  };

  writeString(0, 'RIFF');
  view.setUint32(4, 36 + samples.length * 2, true);
  writeString(8, 'WAVE');
  writeString(12, 'fmt ');
  view.setUint32(16, 16, true);
  view.setUint16(20, 1, true);
  view.setUint16(22, AUDIO_SETTINGS.CHANNELS, true);
  view.setUint32(24, AUDIO_SETTINGS.SAMPLE_RATE, true);
  view.setUint32(28, AUDIO_SETTINGS.SAMPLE_RATE * 2, true);
  view.setUint16(32, 2, true);
  view.setUint16(34, AUDIO_SETTINGS.BITS_PER_SAMPLE, true);
  writeString(36, 'data');
  view.setUint32(40, samples.length * 2, true);

  // PCM 데이터 작성
  const writeOffset = 44;
  samples.forEach((sample, i) => {
    view.setInt16(writeOffset + i * 2, sample, true);
  });

  return new Blob([buffer], { type: 'audio/wav' });
};

// 스토어 생성
const audioStore = create<AudioState>((set, get) => ({
  isRecording: false,
  mediaRecorder: null,
  audioChunks: [],
  volume: 0,
  _refs: {},

  startRecording: async () => {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      const mediaRecorder = new MediaRecorder(
        stream,
        AUDIO_SETTINGS.MEDIA_RECORDER_OPTIONS
      );
      const audioChunks: Blob[] = [];

      mediaRecorder.ondataavailable = (e) => {
        if (e.data.size > 0) {
          audioChunks.push(e.data);
        }
      };

      // 오디오 컨텍스트 및 분석기 설정
      const audioContext = createAudioContext();
      const analyser = audioContext.createAnalyser();
      analyser.fftSize = 1024; // FFT 크기 감소
      analyser.smoothingTimeConstant = 0.8; // 부드러운 전환을 위한 스무딩 추가
      const source = audioContext.createMediaStreamSource(stream);
      source.connect(analyser);

      const dataArray = new Uint8Array(analyser.frequencyBinCount);

      // 볼륨 계산 및 업데이트
      const updateVolume = () => {
        const state = get();
        if (
          !state._refs.analyser ||
          !state._refs.dataArray ||
          !state.isRecording
        )
          return;

        const now = performance.now();
        if (
          state._refs.lastVolumeUpdate &&
          now - state._refs.lastVolumeUpdate < 16
        ) {
          // 약 60fps
          state._refs.rafId = requestAnimationFrame(updateVolume);
          return;
        }

        state._refs.analyser.getByteTimeDomainData(state._refs.dataArray);
        const rms = Math.sqrt(
          state._refs.dataArray.reduce((s, v) => s + (v - 128) ** 2, 0) /
            state._refs.dataArray.length
        );

        // 볼륨 변화가 일정 임계값 이상일 때만 상태 업데이트
        if (Math.abs(state.volume - rms) > 0.1) {
          set({ volume: rms });
        }

        state._refs.lastVolumeUpdate = now;
        state._refs.rafId = requestAnimationFrame(updateVolume);
      };

      set({
        _refs: {
          audioCtx: audioContext,
          analyser,
          dataArray,
          stream,
          lastVolumeUpdate: 0,
        },
      });

      mediaRecorder.start(100);
      set({ isRecording: true, mediaRecorder, audioChunks });
      updateVolume();
      console.log('녹음 시작됨');
    } catch (error) {
      console.error('녹음 시작 실패:', error);
      throw error;
    }
  },

  stopRecording: async (preBuffer: Float32Array[]) => {
    const { mediaRecorder, audioChunks, _refs } = get();
    if (!mediaRecorder) throw new Error('녹음이 시작되지 않았습니다.');

    try {
      // MediaRecorder 중지
      mediaRecorder.stop();

      // 볼륨 업데이트 중지
      if (_refs.rafId) {
        cancelAnimationFrame(_refs.rafId);
      }

      // 스트림 정리
      if (_refs.stream) {
        _refs.stream.getTracks().forEach((track) => track.stop());
      }

      // 오디오 컨텍스트 정리
      if (_refs.audioCtx && _refs.audioCtx.state !== 'closed') {
        await _refs.audioCtx.close();
      }

      // 녹음된 데이터 처리
      const recordedBlob = new Blob(audioChunks, { type: 'audio/webm' });
      console.log('녹음된 webm Blob 크기:', recordedBlob.size);

      // AudioContext 생성
      const audioContext = createAudioContext();
      const audioBuffer = await audioContext.decodeAudioData(
        await recordedBlob.arrayBuffer()
      );
      const recordedData = new Int16Array(audioBuffer.length);
      const channelData = audioBuffer.getChannelData(0);

      // Float32Array를 Int16Array로 변환
      for (let i = 0; i < audioBuffer.length; i++) {
        recordedData[i] = Math.max(-1, Math.min(1, channelData[i])) * 0x7fff;
      }

      // 프리버퍼 처리
      const preBufferData = new Int16Array(
        preBuffer.reduce((acc, curr) => acc + curr.length, 0)
      );
      let offset = 0;
      preBuffer.forEach((buffer) => {
        for (let i = 0; i < buffer.length; i++) {
          preBufferData[offset + i] =
            Math.max(-1, Math.min(1, buffer[i])) * 0x7fff;
        }
        offset += buffer.length;
      });

      // 데이터 병합
      const mergedData = new Int16Array(
        preBufferData.length + recordedData.length
      );
      mergedData.set(preBufferData);
      mergedData.set(recordedData, preBufferData.length);

      // WAV로 인코딩
      const wavBlob = encodeWAV(mergedData);
      console.log('최종 wav Blob 크기:', wavBlob.size);

      // 상태 초기화
      set({
        isRecording: false,
        mediaRecorder: null,
        audioChunks: [],
        volume: 0,
        _refs: {},
      });
      return wavBlob;
    } catch (error) {
      console.error('녹음 중지 중 오류:', error);
      set({
        isRecording: false,
        mediaRecorder: null,
        audioChunks: [],
        volume: 0,
        _refs: {},
      });
      throw error;
    }
  },
}));

export default audioStore;
