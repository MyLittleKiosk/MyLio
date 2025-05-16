import { ClovaResponse } from '@/types/clova';
import axios from 'axios';

// Clova API 클라이언트 설정
const baseUrl = import.meta.env.VITE_PUBLIC_VOICE_API_URL;
console.log('baseUrl:', baseUrl);
// const baseUrl = 'https://localhost:8000';
const voiceClient = axios.create({
  baseURL: baseUrl,
});

/**
 * Clova API 서비스
 * 음성 인식 및 처리와 관련된 API 호출을 담당합니다.
 */

/**
 * 오디오 데이터를 FastAPI 백엔드로 전송하여 처리합니다.
 * @param audioBlob - 전송할 오디오 Blob 데이터
 * @returns 백엔드 API 응답 데이터
 */
export async function sendAudioToClova(
  audioBlob: Blob
): Promise<ClovaResponse> {
  try {
    // FormData를 사용하여 Blob 데이터 전송
    const formData = new FormData();
    formData.append('file', audioBlob, 'recording.wav');

    // Clova API 엔드포인트로 요청 전송
    const response = await voiceClient.post('/clova/stt', formData, {
      timeout: 30000,
    });

    return response.data;
  } catch (error) {
    console.error('FastAPI 백엔드 요청 중 오류 발생:', error);
    throw error;
  }
}

export async function gcpTts(text: string): Promise<Blob> {
  try {
    const formData = new FormData();
    formData.append('text', text);

    const response = await voiceClient.post('/google/tts', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
      responseType: 'blob', // mp3 받을 거면 blob으로
    });
    console.log('response:', response);

    return response.data;
  } catch (error) {
    console.error('FastAPI 백엔드 요청 중 오류 발생:', error);
    throw error;
  }
}
