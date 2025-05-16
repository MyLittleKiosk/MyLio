import React, { useState } from 'react';

import Button from '@/components/common/Button';
import CompleteModal from '@/components/common/CompleteModal';
import Input from '@/components/common/Input';
import ModalHeader from '@/components/common/Modal/ModalHeader';

import { usePostIngredient } from '@/service/queries/ingredient';
import useModalStore from '@/stores/useModalStore';
import translator from '@/utils/translator';

const AddIngredientModal = () => {
  const { closeModal, openModal } = useModalStore();
  const { mutate } = usePostIngredient();

  const [ingredientValueKr, setIngredientValueKr] = useState('');
  const [ingredientValueEn, setIngredientValueEn] = useState('');

  async function translateIngredientValue() {
    const translatedValue = await translator(ingredientValueKr);
    setIngredientValueEn(translatedValue);
  }

  function handleSubmit(e: React.FormEvent<HTMLFormElement>) {
    e.preventDefault();

    if (ingredientValueKr === '' || ingredientValueEn === '') {
      alert('재료명을 입력하세요.');
      return;
    }
    mutate(
      {
        ingredientTemplateName: ingredientValueKr,
        ingredientTemplateNameEn: ingredientValueEn,
      },
      {
        onSuccess: () => {
          openModal(
            <CompleteModal
              title='재료 추가'
              description='재료 추가가 완료되었습니다.'
              buttonText='확인'
            />
          );
        },
        onError: (error: unknown) => {
          if (error instanceof Error) {
            alert(error.message);
          }
        },
      }
    );
  }

  return (
    <div className='flex flex-col gap-8 px-10 py-8'>
      <ModalHeader
        title='새 재료 추가'
        description='새로운 재료를 입력하세요. '
      />

      <form onSubmit={handleSubmit}>
        <div className='w-full flex flex-col gap-2 '>
          <div className='w-full flex items-center gap-2'>
            <span className='font-preSemiBold text-md break-keep'>
              재료 한글명
            </span>
            <Input
              id='ingredientAdd'
              type='text'
              onChange={(e) => setIngredientValueKr(e.target.value)}
              value={ingredientValueKr}
              placeholder='재료명을 입력하세요.'
            />

            <Button
              className='w-[30%]'
              type='button'
              text='번역하기'
              onClick={() => {
                translateIngredientValue();
              }}
            />
          </div>

          <div className='w-full flex items-center gap-2'>
            <span className='font-preSemiBold text-md break-keep'>
              재료 영문명
            </span>
            <Input
              id='engIngredient'
              className='w-full'
              type='text'
              value={ingredientValueEn}
              placeholder='번역 대기 중'
              onChange={(e) => setIngredientValueEn(e.target.value)}
            />
          </div>

          <div className='flex justify-end gap-2'>
            <Button
              type='button'
              text='취소'
              onClick={() => {
                closeModal();
              }}
              cancel
            />
            <Button type='submit' text='추가' id='addCategory' />
          </div>
        </div>
      </form>
    </div>
  );
};

export default AddIngredientModal;
