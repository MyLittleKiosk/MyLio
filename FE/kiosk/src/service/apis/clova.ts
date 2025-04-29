import axios from 'axios';

// API 응답 타입 정의
export interface ClovaResponse {
  requestId: string;
  status: string;
  message: string;
}

export interface RecognitionResult {
  requestId: string;
  status: string;
  text: string;
  confidence: number;
  timestamp: string;
}

// API 클라이언트 설정
const clovaClient = axios.create({
  baseURL: 'http://127.0.0.1:8000',
});

/**
 * Clova API 서비스
 * 음성 인식 및 처리와 관련된 API 호출을 담당합니다.
 */

/**
 * 오디오 데이터를 Clova API로 전송하여 처리합니다.
 * @param audioBlob - 전송할 오디오 Blob 데이터
 * @returns API 응답 데이터
 */
export const sendAudioToClova = async (
  audioBlob: Blob
): Promise<ClovaResponse> => {
  try {
    // FormData를 사용하여 Blob 데이터 전송
    const formData = new FormData();
    formData.append('audio', audioBlob, 'recording.wav');

    // Clova API 엔드포인트로 요청 전송
    const response = await clovaClient.post(
      '/api/clova/process-audio',
      formData,
      {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      }
    );
    return response.data;
  } catch (error) {
    console.error('Clova API 요청 중 오류 발생:', error);
    throw error;
  }
};

/**
 * Clova API의 음성 인식 결과를 가져옵니다.
 * @param requestId - 처리 요청 ID
 * @returns 음성 인식 결과
 */
export const getClovaRecognitionResult = async (
  requestId: string
): Promise<RecognitionResult> => {
  try {
    const response = await clovaClient.get(`/api/clova/result/${requestId}`);
    return response.data;
  } catch (error) {
    console.error('Clova 결과 조회 중 오류 발생:', error);
    throw error;
  }
};
