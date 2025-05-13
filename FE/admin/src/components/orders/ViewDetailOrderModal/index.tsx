import { DETAIL_ORDERS } from '@/datas/orderList';
import useModalStore from '@/stores/useModalStore';
import { OrderType } from '@/types/orders';
import { formatDate } from '@/utils/formatDate';
import { formatMoney } from '@/utils/formatMoney';

interface ViewDetailOrderModalProps {
  initialData: OrderType;
}

const ViewDetailOrderModal = ({ initialData }: ViewDetailOrderModalProps) => {
  const { closeModal } = useModalStore();

  return (
    <section className='w-full h-full px-6 py-6 flex flex-col gap-6'>
      <div className='flex flex-col gap-1'>
        <h1 className='text-xl font-preBold'>주문 상세 정보</h1>
        <p className='text-sm text-content font-preRegular'>
          주문번호 : {initialData.orderId}
        </p>
      </div>
      <div>
        <table className='w-full'>
          <tbody>
            <tr className='text-md text-longContent font-preRegular'>
              <td className='w-[50%]'>
                <span className='font-preBold'>날짜/시간:</span>
                <br />
                <span>{formatDate(initialData.orderedAt)}</span>
              </td>
            </tr>
            <tr className='text-md text-longContent font-preRegular'>
              <td className='w-[50%]'>
                <span className='font-preBold'>결제정보: </span>
                <span>{initialData.paidBy}</span>
              </td>
              <td className='w-[50%]'>
                <span className='font-preBold'>주문유형: </span>
                <span>{initialData.orderType}</span>
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
              <th>수량</th>
              <th>가격</th>
              <th>옵션</th>
            </tr>
          </thead>
          <tbody className='divide-y divide-subContent'>
            {DETAIL_ORDERS.content.map((order, index) => (
              <tr key={index} className='text-sm font-preRegular'>
                <td className='px-4 py-3'>{order.productName}</td>
                <td>{order.productQuantity}</td>
                <td>{formatMoney(order.productPrice)}</td>
                <td>
                  {order.productOption ? (
                    <span>{order.productOption}</span>
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
          {formatMoney(initialData.totalPrice)}
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
