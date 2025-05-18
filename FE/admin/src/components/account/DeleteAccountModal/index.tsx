import Button from '@/components/common/Button';
import CompleteModal from '@/components/common/CompleteModal';
import { useDeleteAccount } from '@/service/queries/account';
import useModalStore from '@/stores/useModalStore';
import { AccountType } from '@/types/account';

interface Props {
  row: AccountType;
}

const DeleteAccountModal = ({ row }: Props) => {
  const { openModal, closeModal } = useModalStore();
  const { mutate: deleteAccount } = useDeleteAccount();

  function handleDeleteAccount(accountId: number) {
    deleteAccount(
      { accountId: accountId },
      {
        onSuccess: () => {
          openModal(
            <CompleteModal
              title='계정 삭제'
              description='계정 삭제가 완료되었습니다.'
              buttonText='확인'
            />
          );
        },
      }
    );
  }

  return (
    <div className='flex flex-col items-center justify-center py-6 gap-6'>
      <h2 className='font-preBold text-xl'>삭제 확인</h2>
      <p className='font-preMedium text-lg text-longContent'>
        &quot;{row.userName}&quot; 계정을 삭제하시겠습니까?
      </p>

      <div className='flex gap-4 items-center mt-4'>
        <Button
          type='button'
          text='취소'
          id='cancelDeleteAccountBtn'
          onClick={closeModal}
          className='w-full'
          cancel
        />
        <Button
          type='button'
          text='삭제'
          id='deleteAccountBtn'
          onClick={() => handleDeleteAccount(row.accountId)}
          className='w-full'
        />
      </div>
    </div>
  );
};

export default DeleteAccountModal;
