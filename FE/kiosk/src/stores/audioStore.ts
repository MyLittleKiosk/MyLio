import { create } from 'zustand';

interface AudioStore {
  isRecording: boolean; // 녹음 중 여부
  volume: number; // 실시간 RMS 볼륨

  startRecording: () => Promise<void>;
  stopRecording: () => Promise<Blob>;

  _refs: {
    audioCtx?: AudioContext; // 오디오 컨텍스트
    analyser?: AnalyserNode; // 분석 노드
    dataArray?: Uint8Array; // 데이터 배열
    mediaRec?: MediaRecorder; // 미디어 레코더
    stream?: MediaStream; // 미디어 스트림
    rafId?: number; // 애니메이션 프레임 아이디
    chunks: Blob[]; // 블롭 배열
  };
}

const audioStore = create<AudioStore>((set) => ({
  /* 상태 */
  isRecording: false,
  volume: 0,

  _refs: { chunks: [] },

  /* 액션 */
  async startRecording() {
    const state = audioStore.getState();
    if (state.isRecording) return;
    const r = state._refs;

    r.stream = await navigator.mediaDevices.getUserMedia({
      audio: {
        echoCancellation: true,
        noiseSuppression: true,
        autoGainControl: false,
      },
    });
    r.mediaRec = new MediaRecorder(r.stream);
    r.chunks = [];
    r.mediaRec.ondataavailable = (e) => e.data.size && r.chunks.push(e.data);
    r.mediaRec.start();

    r.audioCtx = new AudioContext();
    r.analyser = r.audioCtx.createAnalyser();
    r.dataArray = new Uint8Array(r.analyser.frequencyBinCount);
    r.audioCtx.createMediaStreamSource(r.stream).connect(r.analyser);

    const tick = () => {
      r.analyser!.getByteTimeDomainData(r.dataArray!);
      const rms = Math.sqrt(
        r.dataArray!.reduce((s, v) => s + (v - 128) ** 2, 0) /
          r.dataArray!.length
      );
      set({ volume: rms }); // 볼륨만 반응형 업데이트
      r.rafId = requestAnimationFrame(tick);
    };
    tick();

    set({ isRecording: true }); // 녹음 시작 알림
  },

  async stopRecording() {
    const state = audioStore.getState();
    if (!state.isRecording) throw new Error('녹음 중이 아닙니다.');
    const r = state._refs;

    r.stream?.getTracks().forEach((t) => t.stop());
    r.stream = undefined;

    const blobPromise = new Promise<Blob>((res) => {
      r.mediaRec!.onstop = () => res(new Blob(r.chunks, { type: 'audio/wav' }));
    });
    r.mediaRec!.stop();
    r.mediaRec = undefined;

    cancelAnimationFrame(r.rafId!);
    r.rafId = undefined;
    await r.audioCtx?.close();
    r.audioCtx = undefined;

    set({ isRecording: false, volume: 0 });
    return blobPromise;
  },
}));

export default audioStore;
