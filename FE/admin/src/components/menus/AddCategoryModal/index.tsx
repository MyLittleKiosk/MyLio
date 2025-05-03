import React, { useState } from 'react';

import Button from '@/components/common/Button';
import Input from '@/components/common/Input';
import ModalHeader from '@/components/common/Modal/ModalHeader';

import useModalStore from '@/stores/useModalStore';

const AddCategoryModal = () => {
  const { closeModal } = useModalStore();

  const [tagValue, setTagValue] = useState('');

  function handleSubmit(e: React.FormEvent<HTMLFormElement>) {
    e.preventDefault();
    closeModal();
  }

  return (
    <div className='flex flex-col gap-8 px-10 py-8'>
      <ModalHeader
        title='새 태그 추가'
        description='새로운 태그 이름을 입력하세요. '
      />

      <form onSubmit={handleSubmit}>
        <div className='w-full flex flex-col gap-2 '>
          <Input
            inputId='tagAdd'
            label='태그명'
            inputType='text'
            onChange={(e) => setTagValue(e.target.value)}
            inputValue={tagValue}
            placeholder='태그명을 입력하세요.'
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
