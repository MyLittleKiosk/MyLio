import Button from '@/components/common/Button';
import useModalStore from '@/stores/useModalStore';

interface Props {
  title: string;
  description: string;
  buttonText: string;
}

const CompleteModal = ({ title, description, buttonText }: Props) => {
  const { closeModal } = useModalStore();

  return (
    <div className='flex flex-col items-center justify-center py-6'>
      <header className='flex flex-col items-center justify-between gap-2'>
        <h2 className='font-preBold text-xl'>{title}</h2>
        <p className='font-preRegular text-md text-content'>{description}</p>
      </header>

      <div className='mt-2'>
        <Button
          buttonType='button'
          text={buttonText}
          onClick={closeModal}
          className='w-full mt-4 flex justify-center'
        />
      </div>
    </div>
  );
};

export default CompleteModal;
