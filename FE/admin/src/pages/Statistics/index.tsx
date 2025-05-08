import { useState } from 'react';

import Select from '@/components/common/Select';
import CategoryPieChart from '@/components/statistics/CategoryPieChart';
import OrderTypePieChart from '@/components/statistics/OrderTypePieChart';
import PaymentsPieChart from '@/components/statistics/PaymentsPieChart';
import SalesTrendChart from '@/components/statistics/SalesTrendChart';

const Statistics = () => {
  const [year, setYear] = useState<number>(new Date().getFullYear());
  const [month, setMonth] = useState<number>(new Date().getMonth() + 1);
  function getFullYear() {
    return Array.from(
      { length: 10 },
      (_, i) => new Date().getFullYear() - 1 - i
    );
  }

  function getFullMonth() {
    return Array.from({ length: 12 }, (_, i) => i + 1);
  }

  return (
    <>
      <div className='w-full h-full p-2 flex flex-col gap-2'>
        <div className='mb-4 flex items-center gap-4'>
          <h1 className='text-2xl font-bold'>통계 대시보드</h1>
        </div>
        <div className='w-full h-full max-h-[600px] min-h-[400px] flex gap-4'>
          <div className='w-full h-full flex flex-col border border-subContent rounded-md p-2 gap-2'>
            <h1 className='text-lg font-bold'>매출 추이</h1>
            <div className='w-full flex-1 flex flex-col gap-2'>
              <div className='flex gap-2'>
                <Select
                  options={getFullYear()}
                  selected={year}
                  placeholder={new Date().getFullYear().toString()}
                  onChange={(e) => setYear(Number(e.target.value))}
                  getOptionLabel={(option) => option.toString()}
                  getOptionValue={(option) => option.toString()}
                />
                <Select
                  options={getFullMonth()}
                  selected={month}
                  placeholder='전체'
                  onChange={(e) => setMonth(Number(e.target.value))}
                  getOptionLabel={(option) => option.toString()}
                  getOptionValue={(option) => option.toString()}
                />
              </div>
              <div className='flex-1 relative'>
                <SalesTrendChart year={year} month={month} />
              </div>
            </div>
          </div>
        </div>

        <div className='w-full h-full flex gap-4'>
          <div className='w-full max-h-[300px] min-h-[200px] flex flex-col border border-subContent rounded-md p-2 gap-2'>
            <h1 className='text-lg font-bold'>결제 수단 별 매출</h1>
            <div className='relative w-full flex-1 flex flex-col gap-2'>
              <PaymentsPieChart year={year} month={month} />
            </div>
          </div>
          <div className='w-full max-h-[300px] min-h-[200px] flex flex-col border border-subContent rounded-md p-2 gap-2'>
            <h1 className='text-lg font-bold'>주문 형태 별 매출</h1>
            <div className='relative w-full flex-1 flex flex-col gap-2'>
              <OrderTypePieChart year={year} month={month} />
            </div>
          </div>
          <div className='w-full max-h-[300px] min-h-[200px] flex flex-col border border-subContent rounded-md p-2 gap-2'>
            <h1 className='text-lg font-bold'>카테고리 별 매출</h1>
            <div className='relative w-full flex-1 flex flex-col gap-2'>
              <CategoryPieChart year={year} month={month} />
            </div>
          </div>
        </div>
      </div>
    </>
  );
};

export default Statistics;
