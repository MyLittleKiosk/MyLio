import Button from '@/components/common/Button';
import CompleteModal from '@/components/common/CompleteModal';
import { useDeleteCategory } from '@/service/queries/category';
import useModalStore from '@/stores/useModalStore';
import { CategoryType } from '@/types/categories';

interface Props {
  row: CategoryType;
}

const DeleteCategoryModal = ({ row }: Props) => {
  const { openModal } = useModalStore();
  const { mutate: deleteCategory } = useDeleteCategory();

  function handleDeleteCategory(categoryId: number) {
    deleteCategory(categoryId, {
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
        &quot;{row.nameKr}&quot; 카테고리를 삭제하시겠습니까?
      </p>

      <div>
        <Button
          type='button'
          text='삭제'
          onClick={() => handleDeleteCategory(row.categoryId)}
          className='w-full mt-4 flex justify-center'
        />
      </div>
    </div>
  );
};

export default DeleteCategoryModal;
