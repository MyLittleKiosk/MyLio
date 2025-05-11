import { formatPieChartData } from '@/utils/formatPieChartData';
import { Pie } from 'react-chartjs-2';
import { config } from './chart.config';

interface Props<T> {
  data: T[];
  labelKey: keyof T;
}

const PieChart = <T extends Record<string, string | number>>({
  data,
  labelKey,
}: Props<T>) => {
  const chartData = formatPieChartData(data, labelKey);

  return (
    <div className='max-h-[300px] min-h-[100px] flex items-center justify-center'>
      <Pie options={config()} data={chartData} />
    </div>
  );
};

export default PieChart;
