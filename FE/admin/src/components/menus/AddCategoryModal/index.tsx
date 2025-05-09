import React, { useState } from 'react';

import Button from '@/components/common/Button';
import Input from '@/components/common/Input';
import ModalHeader from '@/components/common/Modal/ModalHeader';

import useModalStore from '@/stores/useModalStore';
import translator from '@/utils/translator';

import { usePostCategory } from '@/service/queries/category';

const AddCategoryModal = () => {
  const { closeModal } = useModalStore();
  const { mutate } = usePostCategory();

  const [categoryValueKr, setCategoryValueKr] = useState('');
  const [categoryValueEn, setCategoryValueEn] = useState('');

  async function translateCategoryValue() {
    const translatedValue = await translator(categoryValueKr);
    setCategoryValueEn(translatedValue);
  }

  function handleSubmit(e: React.FormEvent<HTMLFormElement>) {
    e.preventDefault();
    mutate({ nameKr: categoryValueKr, nameEn: categoryValueEn });

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
          <div className='w-full flex items-center gap-2'>
            <Input
              inputId='categoryAdd'
              label='카테고리명'
              inputType='text'
              onChange={(e) => setCategoryValueKr(e.target.value)}
              inputValue={categoryValueKr}
              placeholder='카테고리명을 입력하세요.'
            />

            <Button
              buttonType='button'
              text='번역하기'
              onClick={() => {
                translateCategoryValue();
              }}
            />
          </div>

          <div className='w-full flex items-center gap-2'>
            <span className='font-preSemiBold text-md'>카테고리 영문명</span>
            <Input
              inputId='engCategory'
              inputType='text'
              inputValue={categoryValueEn}
              placeholder='번역 대기 중'
              onChange={(e) => setCategoryValueEn(e.target.value)}
            />
          </div>

          <div className='flex justify-end gap-2'>
            <Button
              buttonType='button'
              text='취소'
              onClick={() => {
                closeModal();
              }}
              cancel
            />
            <Button buttonType='submit' text='추가' buttonId='addCategory' />
          </div>
        </div>
      </form>
    </div>
  );
};

export default AddCategoryModal;
