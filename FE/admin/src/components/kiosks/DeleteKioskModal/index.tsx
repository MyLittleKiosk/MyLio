import Button from '@/components/common/Button';
import CompleteModal from '@/components/common/CompleteModal';
import { useDeleteKiosk } from '@/service/queries/kiosk';
import useModalStore from '@/stores/useModalStore';
import { KioskType } from '@/types/kiosk';

interface Props {
  row: KioskType;
}

const DeleteKioskModal = ({ row }: Props) => {
  const { openModal, closeModal } = useModalStore();
  const { mutate: deleteKiosk } = useDeleteKiosk();

  function handleDeleteKiosk(kioskId: number) {
    deleteKiosk(kioskId, {
      onSuccess: () => {
        openModal(
          <CompleteModal
            title='삭제 성공'
            description='삭제에 성공했습니다.'
            buttonText='확인'
          />,
          'sm'
        );
      },
    });
  }

  return (
    <div className='flex flex-col items-center justify-center py-6 gap-6'>
      <h2 className='font-preBold text-xl'>삭제 확인</h2>
      <p className='font-preMedium text-lg text-longContent'>
        &quot;{row.name}&quot; 키오스크를 삭제하시겠습니까?
      </p>

      <div className='flex gap-4 items-center mt-4'>
        <Button
          type='button'
          text='취소'
          id='cancelDeleteKioskBtn'
          onClick={closeModal}
          className='w-full'
          cancel
        />
        <Button
          type='button'
          text='삭제'
          id='deleteKioskBtn'
          onClick={() => handleDeleteKiosk(row.kioskId)}
          className='w-full'
        />
      </div>
    </div>
  );
};

export default DeleteKioskModal;
