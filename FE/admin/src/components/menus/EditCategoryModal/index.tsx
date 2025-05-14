import React, { useState } from 'react';

import Button from '@/components/common/Button';
import Input from '@/components/common/Input';
import ModalHeader from '@/components/common/Modal/ModalHeader';
import CompleteModal from '@/components/common/CompleteModal';

import useModalStore from '@/stores/useModalStore';
import translator from '@/utils/translator';

import { useEditCategory } from '@/service/queries/category';
import { CategoryType } from '@/types/categories';

interface Props {
  row: CategoryType;
}

const EditCategoryModal = ({ row }: Props) => {
  const { closeModal, openModal } = useModalStore();
  const { mutate } = useEditCategory();

  const [categoryValueKr, setCategoryValueKr] = useState(row.nameKr);
  const [categoryValueEn, setCategoryValueEn] = useState(row.nameEn);

  async function translateCategoryValue() {
    const translatedValue = await translator(categoryValueKr);
    setCategoryValueEn(translatedValue);
  }

  function handleSubmit(e: React.FormEvent<HTMLFormElement>) {
    e.preventDefault();
    mutate(
      {
        categoryId: row.categoryId,
        nameKr: categoryValueKr,
        nameEn: categoryValueEn,
      },
      {
        onSuccess: () => {
          openModal(
            <CompleteModal
              title='수정 완료'
              description='카테고리 수정이 완료되었습니다.'
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
        title='카테고리 수정'
        description='카테고리명을 수정하세요. '
      />

      <form onSubmit={handleSubmit}>
        <div className='w-full flex flex-col gap-2 '>
          <div className='w-full flex items-center gap-2'>
            <Input
              id='categoryAdd'
              label='카테고리명'
              type='text'
              onChange={(e) => setCategoryValueKr(e.target.value)}
              value={categoryValueKr}
              placeholder='카테고리명을 입력하세요.'
            />

            <Button
              type='button'
              text='번역하기'
              onClick={() => {
                translateCategoryValue();
              }}
            />
          </div>

          <div className='w-full flex items-center gap-2'>
            <span className='font-preSemiBold text-md'>카테고리 영문명</span>
            <Input
              id='engCategory'
              type='text'
              value={categoryValueEn}
              placeholder='번역 대기 중'
              onChange={(e) => setCategoryValueEn(e.target.value)}
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
            <Button type='submit' text='수정' id='addCategory' />
          </div>
        </div>
      </form>
    </div>
  );
};

export default EditCategoryModal;
