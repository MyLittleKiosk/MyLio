import { ChartData } from 'chart.js';

export const DEFAULT_COLORS = [
  '#60a5fa',
  '#34d399',
  '#f87171',
  '#fbbf24',
  '#a78bfa',
  '#f472b6',
  '#38bdf8',
  '#4ade80',
  '#facc15',
  '#fb7185',
  '#10b981',
  '#c084fc',
];

/**
 * 다양한 데이터 타입에 대해 Pie 차트용 Chart.js 데이터로 변환하는 유틸 함수
 *
 * @param rawData - [{ labelKey, valueKey }] 형태의 배열
 * @param labelKey - 라벨 필드 이름 (예: 'paymentName', 'orderTypeName')
 * @param valueKey - 값 필드 이름 (예: 'ratio')
 * @returns Chart.js Pie 차트에 맞는 데이터 구조
 */
export function formatPieChartData<T extends Record<string, string | number>>(
  rawData: T[],
  labelKey: keyof T
): ChartData<'pie'> {
  if (rawData === undefined || rawData.length === 0) {
    return {
      labels: ['데이터 없음'],
      datasets: [
        {
          label: '비중',
          data: [1], // 100% 하나로 처리
          backgroundColor: ['#e5e7eb'], // Tailwind gray-200
          borderWidth: 1,
        },
      ],
    };
  }
  return {
    labels: rawData.map((item) => item[labelKey] as string),
    datasets: [
      {
        label: '비중',
        data: rawData.map((item) => item['ratio'] as number),
        backgroundColor: DEFAULT_COLORS.slice(0, rawData.length),
        borderWidth: 1,
      },
    ],
  };
}
