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
  );
};

export default Orders;
