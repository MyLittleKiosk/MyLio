import Button from '@/components/common/Button';
import CompleteModal from '@/components/common/CompleteModal';
import Input from '@/components/common/Input';
import errorMessage from '@/datas/error';
import { usePatchAccountPassword } from '@/service/queries/account';
import useModalStore from '@/stores/useModalStore';
import { verificationPassword } from '@/utils/verificationPassword';
import { useState } from 'react';

const MyPassword = () => {
  const { mutate: patchAccountPassword } = usePatchAccountPassword();
  const { openModal } = useModalStore();
  const [nowPassword, setNowPassword] = useState('');
  const [newPassword, setNewPassword] = useState('');
  const [newPasswordCheck, setNewPasswordCheck] = useState('');
  const [error, setError] = useState('');

  const handlePatchAccountPassword = () => {
    setError(''); // 기존 에러 메시지 초기화
    if (!verificationPassword(newPassword)) {
      setError(errorMessage.password.invalid);
      return;
    }
    if (newPassword !== newPasswordCheck) {
      setError(errorMessage.password.notMatch);
      return;
    }
    patchAccountPassword(
      { nowPassword, newPassword },
      {
        onSuccess: () => {
          openModal(
            <CompleteModal
              title='비밀번호 변경'
              description='비밀번호가 변경되었습니다.'
              buttonText='확인'
            />
          );
          // 성공 시 에러 메시지 초기화 및 입력 필드 초기화 (선택 사항)
          setError('');
          setNowPassword('');
          setNewPassword('');
          setNewPasswordCheck('');
        },
        onError: () => {
          setError(errorMessage.password.unknown);
        },
      }
    );
  };

  return (
    <form className='w-full flex flex-col items-center gap-5'>
      <div className='w-full flex flex-col gap-5'>
        <Input
          inputId='nowPassword'
          label='현재 비밀번호'
          placeholder='현재 비밀번호'
          inputType='password'
          inputValue={nowPassword}
          onChange={(e) => {
            setNowPassword(e.target.value);
            if (error) setError(''); // 입력 시 에러 메시지 초기화
          }}
        />
        <Input
          inputId='newPassword'
          label='새 비밀번호'
          placeholder='새 비밀번호 (8~16자, 영문, 숫자, 특수문자 포함)'
          inputType='password'
          inputValue={newPassword}
          onChange={(e) => {
            setNewPassword(e.target.value);
            if (error) setError(''); // 입력 시 에러 메시지 초기화
          }}
        />
        <Input
          inputId='newPasswordCheck'
          label='새 비밀번호 확인'
          placeholder='새 비밀번호 확인'
          inputType='password'
          inputValue={newPasswordCheck}
          onChange={(e) => {
            setNewPasswordCheck(e.target.value);
            if (error) setError(''); // 입력 시 에러 메시지 초기화
          }}
        />
      </div>
      {error && <p className='text-error mt-2 text-sm'>{error}</p>}
      <Button
        buttonType='button'
        text='변경'
        onClick={handlePatchAccountPassword}
        className='mt-4 w-full md:w-auto'
      />
    </form>
  );
};

export default MyPassword;
