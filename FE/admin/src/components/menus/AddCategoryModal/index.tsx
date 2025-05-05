import React, { useState } from 'react';

import Button from '@/components/common/Button';
import Input from '@/components/common/Input';
import ModalHeader from '@/components/common/Modal/ModalHeader';

import useModalStore from '@/stores/useModalStore';

const AddCategoryModal = () => {
  const { closeModal } = useModalStore();

  const [categoryValue, setCategoryValue] = useState('');

  function handleSubmit(e: React.FormEvent<HTMLFormElement>) {
    e.preventDefault();
    closeModal();
  }

  return (
    <div className='flex flex-col gap-8 px-10 py-8'>
      <ModalHeader
        title='새 카테고리 추가'
        description='새로운 카테고리를 입력하세요. '
      />

      <form onSubmit={handleSubmit}>
        <div className='w-full flex flex-col gap-2 '>
          <Input
            inputId='categoryAdd'
            label='카테고리명'
            inputType='text'
            onChange={(e) => setCategoryValue(e.target.value)}
            inputValue={categoryValue}
            placeholder='카테고리명을 입력하세요.'
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

export default AddCategoryModal;
