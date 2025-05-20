import { useGetOrderDetail } from '@/service/queries/orders';
import useModalStore from '@/stores/useModalStore';
import { OrderType } from '@/types/orders';
import { formatDate } from '@/utils/formatDate';
import { formatMoney } from '@/utils/formatMoney';

interface ViewDetailOrderModalProps {
  initialData: OrderType;
}

const ViewDetailOrderModal = ({ initialData }: ViewDetailOrderModalProps) => {
  const { closeModal } = useModalStore();
  const { data: orderDetail, isLoading } = useGetOrderDetail(
    initialData.orderId
  );

  if (isLoading) {
    return <div>Loading...</div>;
  }

  return (
    <section className='w-full h-full px-6 py-6 flex flex-col gap-6'>
      <div className='flex flex-col gap-1'>
        <h1 className='text-xl font-preBold'>주문 상세 정보</h1>
        <p className='text-sm text-content font-preRegular'>
          주문번호 : {orderDetail?.orderId}
        </p>
      </div>
      <div>
        <table className='w-full'>
          <tbody>
            <tr className='text-md text-longContent font-preRegular'>
              <td className='w-[50%]'>
                <span className='font-preBold'>날짜/시간:</span>
                <br />
                <span>{formatDate(orderDetail?.orderedAt || '')}</span>
              </td>
            </tr>
            <tr className='text-md text-longContent font-preRegular'>
              <td className='w-[50%]'>
                <span className='font-preBold'>결제정보: </span>
                <span>{orderDetail?.paidBy}</span>
              </td>
              <td className='w-[50%]'>
                <span className='font-preBold'>주문유형: </span>
                <span>{orderDetail?.orderType}</span>
              </td>
            </tr>
          </tbody>
        </table>
      </div>

      <div>
        <h3 className='text-md text-longContent font-preBold'>주문 상품</h3>
        <table className='w-full'>
          <thead className='border-b border-subContent'>
            <tr className='text-sm text-left text-content2 font-preLight'>
              <th className='px-4 py-3'>상품명</th>
              <th className='text-center'>수량</th>
              <th className='px-2'>가격</th>
              <th>옵션</th>
            </tr>
          </thead>
          <tbody className='divide-y divide-subContent'>
            {orderDetail?.orderItems.map((order, index) => (
              <tr key={index} className='text-sm font-preRegular'>
                <td className='px-4 py-3'>{order.itemName}</td>
                <td className='text-center'>{order.quantity}</td>
                <td className='px-2'>{formatMoney(order.price)}</td>
                <td>
                  {order.options.length > 0 ? (
                    <span>{order.options.join(', ')}</span>
                  ) : (
                    <span>-</span>
                  )}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      <div>
        <span className='text-md text-longContent font-preBold'>총 금액 :</span>
        <span className='text-md text-longContent font-preBold'>
          {formatMoney(orderDetail?.totalPrice || 0)}
        </span>
      </div>

      <div className='flex justify-end'>
        <button
          onClick={closeModal}
          className='px-4 py-2 bg-white text-black font-preMedium rounded-md border border-subContent hover:bg-subContent'
        >
          닫기
        </button>
      </div>
    </section>
  );
};

export default ViewDetailOrderModal;
