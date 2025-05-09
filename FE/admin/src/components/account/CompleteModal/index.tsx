import Button from '@/components/common/Button';
import ModalHeader from '@/components/common/Modal/ModalHeader';
import useModalStore from '@/stores/useModalStore';

const CompleteModal = () => {
  const { closeModal } = useModalStore();

  return (
    <div className='fixed inset-0 flex items-center justify-center z-50 bg-black/30'>
      <div className='bg-white rounded-2xl shadow-2xl p-8 min-w-[320px] max-w-[90vw] text-center'>
        <ModalHeader
          title='계정 추가'
          description='계정 추가가 완료되었습니다.'
        />
        <div className='flex flex-col gap-2 mt-4'>
          <Button
            buttonType='button'
            text='확인'
            onClick={closeModal}
            className='w-full mt-4 flex justify-center'
          />
        </div>
      </div>
    </div>
  );
};

export default CompleteModal;
