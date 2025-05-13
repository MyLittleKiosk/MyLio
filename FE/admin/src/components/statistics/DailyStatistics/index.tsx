import { useGetStatisticsByDaily } from '@/service/queries/statistics';
import { formatMoney } from '@/utils/formatMoney';

const DailyStatistics = () => {
  const { data, isLoading } = useGetStatisticsByDaily();
  if (isLoading) {
    return (
      <div className='text-3xl font-preBold text-primary'>오늘의 실적은?!</div>
    );
  }
  return (
    <section className='flex gap-4 font-preRegular'>
      <article className='w-[300px] px-5 flex flex-col justify-center gap-2 border border-subContent rounded-md p-2'>
        <h1 className='text-sm'>오늘의 총 매출</h1>
        <p className='text-2xl font-preBold'>
          {formatMoney(data?.totalSales || 0)}
        </p>
      </article>
      <article className='w-[300px] px-5 flex flex-col justify-center gap-2 border border-subContent rounded-md p-2'>
        <h1 className='text-sm'>오늘의 주문 건수</h1>
        <p className='text-2xl font-preBold'>{data?.totalOrders} 건</p>
      </article>
    </section>
  );
};

export default DailyStatistics;
