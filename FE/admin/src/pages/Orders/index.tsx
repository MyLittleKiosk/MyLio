import { Suspense } from 'react';
import { ErrorBoundary } from 'react-error-boundary';
import Loading from '@/components/common/Loading';
import OrderContent from '@/components/orders/OrderContent';
import Error from '@/components/common/Error';

const Orders = () => {
  return (
    <ErrorBoundary fallbackRender={() => <Error />}>
      <Suspense fallback={<Loading />}>
        <OrderContent />
      </Suspense>
    </ErrorBoundary>
    <>
      <section className='w-full h-full p-4 flex flex-col gap-2 '>
        <h1 className='text-2xl font-preBold h-[5%]'>주문 관리</h1>
        <div className='flex gap-2 max-h-[10%] w-full justify-between'>
          <div className='flex gap-2 w-full'>
            <Input
              id='startSearchOrder'
              placeholder=''
              type='date'
              value={startSearchValue}
              maxDate={endSearchValue}
              onChange={handleSearchChange}
            />
            <Input
              id='endSearchOrder'
              placeholder=''
              type='date'
              value={endSearchValue}
              minDate={startSearchValue}
              onChange={handleEndSearchChange}
            />
            <Button
              id='searchBtnId'
              type='button'
              text='검색'
              onClick={handleSearch}
            />
            <Button
              id='resetBtnId'
              type='button'
              text='전체'
              onClick={handleReset}
              className='bg-content hover:bg-content2'
            />
          </div>
        </div>
        <Table
          title='주문 목록'
          description={`총 ${ordersData?.length || 0}개의 주문이 있습니다.`}
          columns={ORDER_COLUMNS}
          data={ordersData as OrderType[]}
          onView={(row) => {
            openModal(<ViewDetailOrderModal initialData={row} />);
          }}
        />
        <PageNavigation
          pageInfo={pageInfo as Pagination}
          onChangePage={(page: number) => handlePageChange(page)}
        />
        <Modal />
      </section>
    </>
  );
};

export default Orders;
