import PieChart from '@/components/common/PieChart';
import { useGetStatisticsByOrder } from '@/service/queries/statistics';
import { OrderSalesRatioType } from '@/types/statistics';

interface Props {
  year: number;
  month?: number;
}

const OrderTypePieChart = ({ year, month }: Props) => {
  const { data, isLoading } = useGetStatisticsByOrder(year, month);

  if (isLoading) {
    return <div>Loading...</div>;
  }

  return (
    <div className='absolute inset-0 flex items-center justify-center'>
      <PieChart<OrderSalesRatioType> data={data!} labelKey='orderTypeName' />
    </div>
  );
};

export default OrderTypePieChart;
