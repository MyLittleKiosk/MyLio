import Modal from '@/components/common/Modal';
import useModalStore from '@/stores/useModalStore';

const Statistics = () => {
  const { openModal } = useModalStore();
  return (
    <div className='w-full'>
      <button onClick={() => openModal(<div className='w-12 h-10'>Modal</div>)}>
        Open Modal
      </button>
      <Modal />
    </div>
  );
};

export default Statistics;
