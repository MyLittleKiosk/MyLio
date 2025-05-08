import {
  DUMMY_SALES_BY_MONTH_2024_05,
  DUMMY_SALES_BY_YEAR_2024,
} from '@/service/mock/dummies/statistics';
import { useGetSalesTrend } from '@/service/queries/statistics';
import formatSalesData from '@/utils/formatSalesData';
import { Line } from 'react-chartjs-2';
import { config } from './chart.config';

interface SalesTrendChartProps {
  year: number;
  month?: number;
}

const SalesTrendChart = ({ year, month }: SalesTrendChartProps) => {
  const { data, isLoading } = useGetSalesTrend(year, month);
  const chartType = month ? 'month' : 'year';

  if (isLoading) {
    return <div>Loading...</div>;
  }

  const isStorybook =
    typeof process !== 'undefined' && process.env?.VITE_IS_STORYBOOK === 'true';

  console.log(isStorybook);
  if (isStorybook) {
    const chartData = formatSalesData(
      month === 0 ? DUMMY_SALES_BY_YEAR_2024 : DUMMY_SALES_BY_MONTH_2024_05,
      chartType,
      year,
      month
    );
    return (
      <div className='absolute inset-0'>
        <Line data={chartData} options={config(chartType)} />
      </div>
    );
  }

  const chartData = formatSalesData(data!, chartType, year, month);

  return (
    <div className='absolute inset-0'>
      <Line data={chartData} options={config(chartType)} />
    </div>
  );
};

export default SalesTrendChart;
