import Button from '@/components/common/Button';
import CompleteModal from '@/components/common/CompleteModal';
import Input from '@/components/common/Input';
import { usePatchAccount } from '@/service/queries/account';
import useModalStore from '@/stores/useModalStore';
import { AccountForm, AccountType } from '@/types/account';
import { useState } from 'react';

interface Props {
  userInfo: AccountType;
}

const MyInfo = ({ userInfo }: Props) => {
  const { mutate: patchAccount } = usePatchAccount();
  const { openModal } = useModalStore();
  const [username, setUsername] = useState(userInfo.userName);
  const [email, setEmail] = useState(userInfo.email);
  const [storeName, setStoreName] = useState(userInfo.storeName);
  const [storeAddress, setStoreAddress] = useState(userInfo.address);

  const handlePatchAccount = () => {
    const account: AccountForm = {
      userName: username,
      email: email,
      storeName: storeName,
      address: storeAddress,
    };

    patchAccount(
      { account },
      {
        onSuccess: () => {
          openModal(
            <CompleteModal
              title='수정 완료'
              description='수정이 완료되었습니다.'
              buttonText='확인'
            />
          );
        },
        onError: (error) => {
          console.error('Account patch error:', error);
          openModal(
            <CompleteModal
              title='수정 실패'
              description='수정에 실패했습니다. 다시 시도해주세요.'
              buttonText='확인'
            />
          );
        },
      }
    );
  };

  return (
    <form className='w-full flex flex-col items-center gap-5'>
      <div className='w-full flex flex-col gap-5'>
        <Input
          id='username'
          label='사용자 이름'
          placeholder='이름'
          value={username}
          type='text'
          onChange={(e) => setUsername(e.target.value)}
        />
        <Input
          id='email'
          label='이메일'
          placeholder='이메일'
          value={email}
          type='text'
          onChange={(e) => setEmail(e.target.value)}
          disabled
        />
        <Input
          id='storeName'
          label='가게 이름'
          placeholder='가게 이름'
          value={storeName}
          type='text'
          onChange={(e) => setStoreName(e.target.value)}
        />
        <Input
          id='storeAddress'
          label='가게 주소'
          placeholder='가게 주소'
          value={storeAddress}
          type='text'
          onChange={(e) => setStoreAddress(e.target.value)}
        />
      </div>
      <Button type='button' text='수정' onClick={handlePatchAccount} />
    </form>
  );
};

export default MyInfo;
