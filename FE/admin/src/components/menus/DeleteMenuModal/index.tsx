import Button from '@/components/common/Button';
import CompleteModal from '@/components/common/CompleteModal';
import { useDeleteMenu } from '@/service/queries/menu';
import useModalStore from '@/stores/useModalStore';
import { MenuType } from '@/types/menus';

interface Props {
  row: MenuType;
}

const DeleteMenuModal = ({ row }: Props) => {
  const { openModal, closeModal } = useModalStore();
  const { mutate: deleteMenu } = useDeleteMenu();

  function handleDeleteMenu(menuId: number) {
    deleteMenu(menuId, {
      onSuccess: () => {
        openModal(
          <CompleteModal
            title='삭제 성공'
            description='메뉴가 삭제되었습니다.'
            buttonText='확인'
          />
        );
      },
    });
  }

  return (
    <div className='flex flex-col items-center justify-center py-6 gap-6'>
      <h2 className='font-preBold text-xl'>삭제 확인</h2>
      <p className='font-preMedium text-lg text-longContent'>
        &quot;{row.nameKr}&quot; 메뉴를 삭제하시겠습니까?
      </p>
      <div className='flex gap-4 items-center mt-4'>
        <Button
          type='button'
          text='취소'
          id='cancelDeleteMenuBtn'
          onClick={closeModal}
          className='w-full'
          cancel
        />
        <Button
          type='button'
          text='삭제'
          onClick={() => handleDeleteMenu(row.menuId)}
          className='w-full'
        />
      </div>
    </div>
  );
};

export default DeleteMenuModal;
