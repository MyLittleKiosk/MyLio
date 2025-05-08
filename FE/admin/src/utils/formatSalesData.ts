import { SalesTrendType } from '@/types/statistics';
import { ChartData } from 'chart.js';

const getDaysInMonth = (year: number, month: number): number => {
  return new Date(year, month, 0).getDate();
};

/**
 * 매출 데이터에 누락된 데이터를 채워주는 함수
 * @param data 매출 데이터
 * @param chartType 차트 타입
 * @param year 연도
 * @param month 월
 *
 * @returns 포맷팅된 매출 데이터
 */
const fillMissingData = (
  data: SalesTrendType[],
  chartType: 'month' | 'year',
  year?: number,
  month?: number
): SalesTrendType[] => {
  // 일별 데이터 (특정 연도, 월이 선택된 경우)
  if (chartType === 'month' && year && month) {
    const daysInMonth = getDaysInMonth(year, month);
    const days = Array.from({ length: daysInMonth }, (_, i) => i + 1);
    return days.map((day) => {
      const existingData = data.find((item) => item.type === day);
      return existingData || { type: day, sales: 0 };
    });
  }

  // 월별 데이터 (특정 연도가 선택된 경우)
  if (chartType === 'year' && year) {
    const months = Array.from({ length: 12 }, (_, i) => i + 1);
    return months.map((month) => {
      const existingData = data.find((item) => item.type === month);
      return existingData || { type: month, sales: 0 };
    });
  }

  return data;
};

/**
 * 매출 데이터를 그래프에 사용할 데이터 셋 옵션들로 포맷팅하는 함수
 * @param data 매출 데이터
 * @param chartType 차트 타입
 * @param year 연도
 * @param month 월
 *
 * @returns 그래프에 사용할 데이터 셋 옵션들
 */
const formatSalesData = (
  data: SalesTrendType[],
  chartType: 'month' | 'year',
  year?: number,
  month?: number
): ChartData<'line'> => {
  const processedData = fillMissingData(data, chartType, year, month);

  return {
    labels: processedData.map((item) => item.type),
    datasets: [
      {
        label: chartType === 'month' ? '일별 매출액' : '월별 매출액',
        data: processedData.map((item) => item.sales),
        backgroundColor: 'rgba(53, 162, 235, 0.2)',
        borderColor: 'rgb(53, 162, 235)',
        borderWidth: 2,
        fill: true,
        tension: 0.4,
        pointStyle: 'circle',
        pointRadius: 5,
        pointHoverRadius: 8,
        pointHoverBorderWidth: 2,
      },
    ],
  };
};

export default formatSalesData;
