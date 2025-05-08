import PieChart from '@/components/common/PieChart';
import { useGetStatisticsByPayment } from '@/service/queries/statistics';
import { PaymentSalesRatioType } from '@/types/statistics';

interface Props {
  year: number;
  month?: number;
}

const PaymentsPieChart = ({ year, month }: Props) => {
  const { data, isLoading } = useGetStatisticsByPayment(year, month);

  if (isLoading) {
    return <div>Loading...</div>;
  }

  return (
    <div className='absolute inset-0 flex items-center justify-center'>
      <PieChart<PaymentSalesRatioType> data={data!} labelKey='paymentName' />
    </div>
  );
};

export default PaymentsPieChart;
