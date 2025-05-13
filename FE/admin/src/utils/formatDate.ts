/**
 * 날짜 형식을 변환합니다.
 * @param str 날짜 문자열
 * @returns 변환된 날짜 문자열
 */
export function formatDate(date: string) {
  return new Date(date).toLocaleString('ko-KR', {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit',
    hour12: false,
    timeZone: 'Asia/Seoul',
  });
}
