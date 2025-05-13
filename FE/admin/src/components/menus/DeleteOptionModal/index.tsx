import Button from '@/components/common/Button';
import CompleteModal from '@/components/common/CompleteModal';
import { useDeleteOptionGroup } from '@/service/queries/option';
import useModalStore from '@/stores/useModalStore';
import { OptionGroup } from '@/types/options';

interface Props {
  row: OptionGroup;
}

const DeleteOptionModal = ({ row }: Props) => {
  const { openModal } = useModalStore();
  const { mutate: deleteOptionGroup } = useDeleteOptionGroup();

  function handleDeleteOptionGroup(optionId: number) {
    deleteOptionGroup(optionId, {
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
        &quot;{row.optionNameKr}&quot; 옵션 그룹을 삭제하시겠습니까?
      </p>
      <div>
        <Button
          buttonType='button'
          text='삭제'
          onClick={() => handleDeleteOptionGroup(row.optionId)}
          className='w-full mt-4 flex justify-center'
        />
      </div>
    </div>
  );
};

export default DeleteOptionModal;
