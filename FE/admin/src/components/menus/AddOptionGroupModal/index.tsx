import React, { useState } from 'react';

import Button from '@/components/common/Button';
import Input from '@/components/common/Input';
import ModalHeader from '@/components/common/Modal/ModalHeader';

import { useAddOptionGroup } from '@/service/queries/option';

import useModalStore from '@/stores/useModalStore';

import translator from '@/utils/translator';

const AddOptionGroupModal = () => {
  const { closeModal } = useModalStore();
  const { mutate } = useAddOptionGroup();

  const [optionGroupValueKor, setOptionGroupValueKor] = useState('');
  const [optionGroupValueEng, setOptionGroupValueEng] = useState('');

  async function translateCategoryValue() {
    const translatedValue = await translator(optionGroupValueKor);
    setOptionGroupValueEng(translatedValue);
  }

  function handleSubmit(e: React.FormEvent<HTMLFormElement>) {
    e.preventDefault();
    mutate({
      optionNameKr: optionGroupValueKor,
      optionNameEn: optionGroupValueEng,
    });
  }

  return (
    <div className='flex flex-col gap-8 px-10 py-8'>
      <ModalHeader
        title='옵션 그룹 추가'
        description='새로운 옵션 그룹 이름을 입력하세요. '
      />

      <form onSubmit={handleSubmit}>
        <div className='w-full flex flex-col gap-2 '>
          <div className='w-full flex items-center gap-2'>
            <Input
              inputId='optionGroupAdd'
              label='옵션 그룹명'
              inputType='text'
              onChange={(e) => setOptionGroupValueKor(e.target.value)}
              inputValue={optionGroupValueKor}
              placeholder='옵션 그룹명을 입력하세요.'
            />

            <Button
              buttonType='button'
              text='번역하기'
              onClick={() => {
                translateCategoryValue();
              }}
            />
          </div>
          <Input
            inputId='engOptionGroup'
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
            <Button buttonType='submit' text='추가' buttonId='addOptionGroup' />
          </div>
        </div>
      </form>
    </div>
  );
};

export default AddOptionGroupModal;
