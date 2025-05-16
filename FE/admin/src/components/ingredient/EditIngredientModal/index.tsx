import Button from '@/components/common/Button';
import CompleteModal from '@/components/common/CompleteModal';
import Input from '@/components/common/Input';
import ModalHeader from '@/components/common/Modal/ModalHeader';
import { usePatchIngredient } from '@/service/queries/ingredient';
import useModalStore from '@/stores/useModalStore';
import { IngredientType } from '@/types/ingredient';
import translator from '@/utils/translator';
import React, { useState } from 'react';

interface Props {
  row: IngredientType;
}

const EditIngredientModal = ({ row }: Props) => {
  const { closeModal, openModal } = useModalStore();
  const { mutate } = usePatchIngredient();

  const [ingredientValueKr, setIngredientValueKr] = useState(
    row.ingredientTemplateName
  );
  const [ingredientValueEn, setIngredientValueEn] = useState(
    row.ingredientTemplateNameEn
  );

  async function translateIngredientValue() {
    const translatedValue = await translator(ingredientValueKr);
    setIngredientValueEn(translatedValue);
  }

  function handleSubmit(e: React.FormEvent<HTMLFormElement>) {
    e.preventDefault();
    mutate(
      {
        ingredientTemplateId: row.ingredientTemplateId,
        ingredientTemplateName: ingredientValueKr,
        ingredientTemplateNameEn: ingredientValueEn,
      },
      {
        onSuccess: () => {
          openModal(
            <CompleteModal
              title='수정 완료'
              description='재료 수정이 완료되었습니다.'
              buttonText='확인'
            />
          );
        },
      }
    );
  }

  return (
    <div className='flex flex-col gap-8 px-10 py-8'>
      <ModalHeader
        title='재료 수정'
        description={`재료명을 수정하세요. \n 번역 버튼을 누르면 자동으로 번역됩니다.`}
      />

      <form onSubmit={handleSubmit}>
        <div className='w-full flex flex-col gap-2 '>
          <div className='w-full flex items-center gap-2'>
            <span className='font-preSemiBold text-md break-keep'>
              재료 한글명
            </span>
            <Input
              id='korIngredient'
              type='text'
              onChange={(e) => setIngredientValueKr(e.target.value)}
              value={ingredientValueKr}
              placeholder='재료명을 입력하세요.'
            />

            <Button
              type='button'
              text='번역하기'
              onClick={() => {
                translateIngredientValue();
              }}
              className='w-[30%]'
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
            <Button type='submit' text='수정' id='editIngredient' />
          </div>
        </div>
      </form>
    </div>
  );
};

export default EditIngredientModal;
