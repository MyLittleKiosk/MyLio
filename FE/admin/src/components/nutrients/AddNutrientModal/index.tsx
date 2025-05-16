import React, { useState } from 'react';

import Button from '@/components/common/Button';
import CompleteModal from '@/components/common/CompleteModal';
import Input from '@/components/common/Input';
import ModalHeader from '@/components/common/Modal/ModalHeader';

import { useAddNutritionTemplate } from '@/service/queries/nutrient';
import useModalStore from '@/stores/useModalStore';
import translator from '@/utils/translator';

const AddNutrientModal = () => {
  const { closeModal, openModal } = useModalStore();

  const [nutrientValueKr, setNutrientValueKr] = useState('');
  const [nutrientValueEn, setNutrientValueEn] = useState('');
  const [nutrientType, setNutrientType] = useState('');

  const { mutate: addNutritionTemplate } = useAddNutritionTemplate();

  async function translateNutrientValue() {
    const translatedValue = await translator(nutrientValueKr);
    setNutrientValueEn(translatedValue);
  }

  function handleSubmit(e: React.FormEvent<HTMLFormElement>) {
    e.preventDefault();

    if (nutrientValueKr === '' || nutrientValueEn === '') {
      alert('영양성분명을 입력하세요.');
      return;
    }

    if (nutrientType === '') {
      alert('영양성분 단위를 입력하세요.');
      return;
    }

    addNutritionTemplate(
      {
        nutritionTemplateName: nutrientValueKr,
        nutritionTemplateNameEn: nutrientValueEn,
        nutritionTemplateType: nutrientType,
      },
      {
        onSuccess: () => {
          openModal(
            <CompleteModal
              title='영양성분 추가'
              description='영양성분 추가가 완료되었습니다.'
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
        title='새 영양성분 추가'
        description='새로운 영양성분을 입력하세요. '
      />

      <form onSubmit={handleSubmit}>
        <div className='w-full flex flex-col gap-2 '>
          <div className='w-full flex items-center gap-2'>
            <span className='font-preSemiBold text-md break-keep'>
              영양성분 한글명
            </span>
            <Input
              id='nutrientAdd'
              type='text'
              onChange={(e) => setNutrientValueKr(e.target.value)}
              value={nutrientValueKr}
              placeholder='영양성분명을 입력하세요.'
            />

            <Button
              className='w-[30%]'
              type='button'
              text='번역하기'
              onClick={() => {
                translateNutrientValue();
              }}
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
            <Button type='submit' text='추가' id='addNutrient' />
          </div>
        </div>
      </form>
    </div>
  );
};

export default AddNutrientModal;
