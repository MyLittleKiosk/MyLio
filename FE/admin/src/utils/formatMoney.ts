/**
 * 숫자를 원화 형식으로 변환합니다.
 * @param money 숫자
 * @returns 원화 형식의 문자열
 */
export function formatMoney(money: number) {
  return money.toLocaleString('ko-KR', {
    style: 'currency',
    currency: 'KRW',
    minimumFractionDigits: 0,
  });
}
