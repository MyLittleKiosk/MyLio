import { useState } from 'react';

import Input from '@/components/common/Input';
import Button from '@/components/common/Button';
import CompleteModal from '@/components/common/CompleteModal';

import useModalStore from '@/stores/useModalStore';
import { useAddKiosk } from '@/service/queries/kiosk';

const AddKioskModal = () => {
  const [kioskName, setKioskName] = useState('');
  const [groupName, setGroupName] = useState('');

  const [groupNameError, setGroupNameError] = useState({
    error: false,
    message: '',
  });

  const { openModal, closeModal } = useModalStore();
  const { mutate: addKiosk } = useAddKiosk();

  function handleGroupNameChange(value: string) {
    if (/^[A-Z]$/.test(value) || value === '') {
      setGroupNameError({
        error: false,
        message: '',
      });
    } else {
      setGroupNameError({
        error: true,
        message: '알파벳 한 글자만 입력 가능합니다.',
      });
    }

    setGroupName(value.toUpperCase());
  }

  function handleSave() {
    if (kioskName === '' || groupName === '' || groupNameError.error) {
      alert('올바르지 않은 키오스크명 혹은 그룹명입니다.');
      return;
    }

    addKiosk(
      { name: kioskName, startOrder: groupName },
      {
        onSuccess: () => {
          openModal(
            <CompleteModal
              title='등록 성공'
              description='키오스크 등록에 성공했습니다.'
              buttonText='닫기'
            />
          );
        },
      }
    );
  }

  return (
    <div className='bg-white rounded-xl p-8 flex flex-col gap-6'>
      <div>
        <h2 className='text-xl font-preBold mb-1'>키오스크 등록</h2>
        <p className='text-sm text-gray-500 mb-4'>
          키오스크 정보를 등록합니다.
        </p>
        <div className='flex flex-col gap-4'>
          <Input
            inputId='kioskName'
            label='키오스크명'
            placeholder='키오스크명을 입력하세요'
            inputType='text'
            inputValue={kioskName}
            onChange={(e) => setKioskName(e.target.value)}
          />

          <Input
            inputId='groupName'
            label='그룹명 (A-Z)'
            placeholder='그룹명을 입력하세요'
            inputType='text'
            inputValue={groupName}
            onChange={(e) => handleGroupNameChange(e.target.value)}
            error={groupNameError.error}
            errorMessage={groupNameError.message}
          />
        </div>
      </div>
      <div className='flex justify-end gap-2 mt-4'>
        <Button buttonType='button' text='취소' cancel onClick={closeModal} />
        <Button
          buttonType='button'
          text='저장'
          buttonId='saveAddKiosk'
          onClick={handleSave}
        />
      </div>
    </div>
  );
};

export default AddKioskModal;
