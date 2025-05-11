import Button from '@/components/common/Button';
import ModalHeader from '@/components/common/Modal/ModalHeader';
import useModalStore from '@/stores/useModalStore';

interface Props {
  title: string;
  description: string;
  buttonText: string;
}

const CompleteModal = ({ title, description, buttonText }: Props) => {
  const { closeModal } = useModalStore();

  return (
    <div className='fixed inset-0 flex items-center justify-center z-50 bg-black/30'>
      <div className='bg-white rounded-2xl shadow-2xl p-8 min-w-[320px] max-w-[90vw] text-center'>
        <ModalHeader title={title} description={description} />
        <div className='flex flex-col gap-2 mt-4'>
          <Button
            buttonType='button'
            text={buttonText}
            onClick={closeModal}
            className='w-full mt-4 flex justify-center'
          />
        </div>
      </div>
    </div>
  );
};

export default CompleteModal;
