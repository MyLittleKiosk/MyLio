import Button from '@/components/common/Button';
import Input from '@/components/common/Input';
import ModalHeader from '@/components/common/Modal/ModalHeader';
import useModalStore from '@/stores/useModalStore';
import React, { useState } from 'react';

const AddOptionGroupModal = () => {
  const { closeModal } = useModalStore();

  const [optionGroupValueKor, setOptionGroupValueKor] = useState('');
  const [optionGroupValueEng, setOptionGroupValueEng] = useState('');

  function handleSubmit(e: React.FormEvent<HTMLFormElement>) {
    e.preventDefault();
    closeModal();
  }

  return (
    <div className='flex flex-col gap-8 px-10 py-8'>
      <ModalHeader
        title='옵션 그룹 추가'
        description='새로운 옵션 그룹 이름을 입력하세요. '
      />

      <form onSubmit={handleSubmit}>
        <div className='w-full flex flex-col gap-2 '>
          <Input
            inputId='optionGroupAdd'
            label='옵션 그룹명'
            inputType='text'
            onChange={(e) => setOptionGroupValueKor(e.target.value)}
            inputValue={optionGroupValueKor}
            placeholder='옵션 그룹명을 입력하세요.'
          />
          <Input
            inputId='optionGroupAdd'
            label='옵션 그룹 영문명'
            inputType='text'
            onChange={(e) => setOptionGroupValueEng(e.target.value)}
            inputValue={optionGroupValueEng}
            placeholder='옵션 그룹 영문명을 입력하세요.'
          />
          <div className='flex justify-end gap-2'>
            <Button
              buttonType='button'
              text='취소'
              onClick={() => {
                closeModal();
              }}
              cancel
            />
            <Button buttonType='submit' text='추가' />
          </div>
        </div>
      </form>
    </div>
  );
};

export default AddOptionGroupModal;
