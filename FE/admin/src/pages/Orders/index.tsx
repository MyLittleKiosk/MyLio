import OrderContent from '@/components/orders/OrderContent';
import ErrorHandler from '@/components/common/ErrorHandler';

const Orders = () => {
  return (
    <ErrorHandler>
      <OrderContent />
    </ErrorHandler>
  );
};

export default Orders;
