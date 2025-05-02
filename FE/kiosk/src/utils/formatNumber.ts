/**
 * 숫자를 1000단위로 콤마를 찍어주는 함수
 * @param num 변환할 숫자
 * @returns 콤마가 찍힌 문자열
 */
export const formatNumber = (num: number): string => {
  return num.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ',');
};
