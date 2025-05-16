import Button from '@/components/common/Button';
import CompleteModal from '@/components/common/CompleteModal';
import Input from '@/components/common/Input';
import ModalHeader from '@/components/common/Modal/ModalHeader';
import { usePatchNutritionTemplate } from '@/service/queries/nutrient';

import useModalStore from '@/stores/useModalStore';
import { NutrientType } from '@/types/nutrient';
import translator from '@/utils/translator';
import React, { useState } from 'react';

interface Props {
  row: NutrientType;
}

const EditNutrientModal = ({ row }: Props) => {
  const { closeModal, openModal } = useModalStore();

  const [nutrientValueKr, setNutrientValueKr] = useState(
    row.nutritionTemplateName
  );
  const [nutrientValueEn, setNutrientValueEn] = useState(
    row.nutritionTemplateNameEn
  );
  const [nutrientType, setNutrientType] = useState(row.nutritionTemplateType);

  const { mutate: patchNutritionTemplate } = usePatchNutritionTemplate();

  async function translateNutrientValue() {
    const translatedValue = await translator(nutrientValueKr);
    setNutrientValueEn(translatedValue);
  }

  function handleSubmit(e: React.FormEvent<HTMLFormElement>) {
    e.preventDefault();

    patchNutritionTemplate(
      {
        nutritionId: row.nutritionTemplateId,
        nutrition: {
          nutritionTemplateName: nutrientValueKr,
          nutritionTemplateNameEn: nutrientValueEn,
          nutritionTemplateType: nutrientType,
        },
      },
      {
        onSuccess: () => {
          openModal(
            <CompleteModal
              title='수정 완료'
              description='영양성분 수정이 완료되었습니다.'
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
        title='영양성분 수정'
        description={`영양성분을 수정하세요. \n 번역 버튼을 누르면 자동으로 번역됩니다.`}
      />

      <form onSubmit={handleSubmit}>
        <div className='w-full flex flex-col gap-2 '>
          <div className='w-full flex items-center gap-2'>
            <span className='font-preSemiBold text-md break-keep'>
              영양성분 한글명
            </span>
            <Input
              id='korNutrient'
              type='text'
              onChange={(e) => setNutrientValueKr(e.target.value)}
              value={nutrientValueKr}
              placeholder='영양성분명을 입력하세요.'
            />

            <Button
              type='button'
              text='번역하기'
              onClick={() => {
                translateNutrientValue();
              }}
              className='w-[30%]'
            />
          </div>

          <div className='w-full flex items-center gap-2'>
            <span className='font-preSemiBold text-md break-keep'>
              영양성분 영문명
            </span>
            <Input
              id='engNutrient'
              className='w-full'
              type='text'
              value={nutrientValueEn}
              placeholder='번역 대기 중'
              onChange={(e) => setNutrientValueEn(e.target.value)}
            />
          </div>

          <div className='w-full flex items-center gap-2'>
            <span className='font-preSemiBold text-md break-keep'>
              영양성분 단위
            </span>
            <Input
              id='typeNutrient'
              className='w-full'
              type='text'
              value={nutrientType}
              placeholder='영양성분 단위를 입력하세요. EX) kg, kcal'
              onChange={(e) => setNutrientType(e.target.value)}
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

export default EditNutrientModal;
