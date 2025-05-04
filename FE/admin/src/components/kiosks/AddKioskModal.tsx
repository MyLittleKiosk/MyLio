import React, { useState } from 'react';
import Input from '@/components/common/Input';
import Button from '@/components/common/Button';
import Select from '../common/Select';

interface AddKioskModalProps {
  initialData?: {
    kioskName: string;
    groupName: string;
    status: string;
  };
}

const AddKioskModal = ({ initialData }: AddKioskModalProps) => {
  const [kioskName, setKioskName] = useState(initialData?.kioskName || '');
  const [groupName, setGroupName] = useState(initialData?.groupName || '');
  const [status, setStatus] = useState(initialData?.status || '활성화');

  function handleStatusChange(e: React.ChangeEvent<HTMLSelectElement>) {
    setStatus(e.target.value);
  }

  function handleGroupNameChange(value: string) {
    if (/^[A-Z]$/.test(value) || value === '') {
      setGroupName(value);
    }
  }

  return (
    <div className='w-[420px] bg-white rounded-xl p-8 flex flex-col gap-6'>
      <div>
        <h2 className='text-xl font-preBold mb-1'>키오스크 수정</h2>
        <p className='text-sm text-gray-500 mb-4'>
          키오스크 정보를 수정합니다.
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
              getOptionLabel={(option) => option}
              getOptionValue={(option) => option}
            />
          </label>
        </div>
      </div>
      <div className='flex justify-end gap-2 mt-4'>
        <Button buttonType='button' text='취소' cancel onClick={() => {}} />
        <Button buttonType='button' text='저장' onClick={() => {}} />
      </div>
    </div>
  );
};

export default AddKioskModal;
