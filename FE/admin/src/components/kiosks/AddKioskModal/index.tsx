import React, { useState } from 'react';

import Input from '@/components/common/Input';
import Button from '@/components/common/Button';
import Select from '@/components/common/Select';
import CompleteModal from '@/components/common/CompleteModal';

import useModalStore from '@/stores/useModalStore';
import { useAddKiosk } from '@/service/queries/kiosk';

const AddKioskModal = () => {
  const [kioskName, setKioskName] = useState('');
  const [groupName, setGroupName] = useState('');
  const [status, setStatus] = useState('활성화');

  const [groupNameError, setGroupNameError] = useState({
    error: false,
    message: '',
  });

  const { openModal, closeModal } = useModalStore();
  const { mutate: addKiosk } = useAddKiosk();

  function handleStatusChange(e: React.ChangeEvent<HTMLSelectElement>) {
    setStatus(e.target.value);
  }

  function handleGroupNameChange(value: string) {
    if (/^[A-Z]$/.test(value) || value === '') {
      setGroupName(value);
      setGroupNameError({
        error: false,
        message: '',
      });
    } else {
      setGroupNameError({
        error: true,
        message: '그룹명은 "대문자 + 한 글자"로 입력해주세요.',
      });
    }
  }

  function handleSave() {
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
    <div className='w-[420px] bg-white rounded-xl p-8 flex flex-col gap-6'>
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
          <label className='flex gap-4 items-center w-full'>
            <span className='min-w-[80px] max-w-[100px] text-md font-preSemiBold whitespace-nowrap'>
              활성화 여부
            </span>
            <Select
              options={['활성화', '비활성화']}
              selected={status}
              onChange={handleStatusChange}
              placeholder='전체'
              className='w-full h-full'
              getOptionLabel={(option) => option as string}
              getOptionValue={(option) => option as string}
            />
          </label>
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
