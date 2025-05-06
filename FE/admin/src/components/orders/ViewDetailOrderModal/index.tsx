import { DETAIL_ORDERS } from '@/datas/orderList';
import OrderItem from '@/types/orders';

interface ViewDetailOrderModalProps {
  initialData: OrderItem;
  onClose: () => void;
}

const ViewDetailOrderModal = ({
  initialData,
  onClose,
}: ViewDetailOrderModalProps) => {
  return (
    <section className='w-full h-full px-6 py-6 flex flex-col gap-6'>
      <div className='flex flex-col gap-1'>
        <h1 className='text-xl font-preBold'>주문 상세 정보</h1>
        <p className='text-sm text-content font-preRegular'>
          주문번호 : {initialData.order_id}
        </p>
      </div>
      <div>
        <table className='w-full'>
          <tr className='text-md text-longContent font-preRegular'>
            <td className='w-[50%]'>
              <span className='font-preBold'>날짜/시간: </span>
              <span>{initialData.order_date}</span>
            </td>
            <td className='w-[50%]'>
              <span className='font-preBold'>점포: </span>
              <span>{initialData.order_store}</span>
            </td>
          </tr>
          <tr className='text-md text-longContent font-preRegular'>
            <td className='w-[50%]'>
              <span className='font-preBold'>결제정보: </span>
              <span>{initialData.order_payment}</span>
            </td>
            <td className='w-[50%]'>
              <span className='font-preBold'>주문유형: </span>
              <span>{initialData.order_type}</span>
            </td>
          </tr>
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
                <td className='px-4 py-3'>{order.product_name}</td>
                <td>{order.product_quantity}</td>
                <td>{order.product_price}</td>
                <td>
                  {order.product_option ? (
                    <span>{order.product_option}</span>
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
          ₩{initialData.order_price}
        </span>
      </div>

      <div className='flex justify-end'>
        <button
          onClick={onClose}
          className='px-4 py-2 bg-white text-black font-preMedium rounded-md border border-subContent hover:bg-subContent'
        >
          닫기
        </button>
      </div>
    </section>
  );
};

export default ViewDetailOrderModal;
