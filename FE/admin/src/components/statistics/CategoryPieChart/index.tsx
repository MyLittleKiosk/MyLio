import PieChart from '@/components/common/PieChart';
import { useGetStatisticsByCategory } from '@/service/queries/statistics';
import { CategorySalesRatioType } from '@/types/statistics';

interface Props {
  year: number;
  month?: number;
}

const CategoryPieChart = ({ year, month }: Props) => {
  const { data, isLoading } = useGetStatisticsByCategory(year, month);

  if (isLoading) {
    return <div>Loading...</div>;
  }

  return (
    <div className='absolute inset-0 flex items-center justify-center'>
      <PieChart<CategorySalesRatioType> data={data!} labelKey='categoryName' />
    </div>
  );
};

export default CategoryPieChart;
