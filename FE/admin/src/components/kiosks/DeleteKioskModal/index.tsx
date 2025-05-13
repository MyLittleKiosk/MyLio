import Button from '@/components/common/Button';
import CompleteModal from '@/components/common/CompleteModal';
import { useDeleteKiosk } from '@/service/queries/kiosk';
import useModalStore from '@/stores/useModalStore';
import { KioskType } from '@/types/kiosk';

interface Props {
  row: KioskType;
}

const DeleteKioskModal = ({ row }: Props) => {
  const { openModal } = useModalStore();
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

      <div>
        <Button
          buttonType='button'
          text='삭제'
          buttonId='deleteKioskBtn'
          onClick={() => handleDeleteKiosk(row.kioskId)}
          className='w-full mt-4 flex justify-center'
        />
      </div>
    </div>
  );
};

export default DeleteKioskModal;
