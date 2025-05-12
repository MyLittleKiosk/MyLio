import React, { useState } from 'react';

import Button from '@/components/common/Button';
import Input from '@/components/common/Input';
import ModalHeader from '@/components/common/Modal/ModalHeader';
import CompleteModal from '@/components/common/CompleteModal';

import useModalStore from '@/stores/useModalStore';

import { OptionGroup } from '@/types/options';

import { useAddOptionDetail } from '@/service/queries/option';

interface AddOptionDetailModalProps {
  row: OptionGroup;
}

const AddOptionDetailModal = ({ row }: AddOptionDetailModalProps) => {
  const { closeModal, openModal } = useModalStore();

  const [optionDetailName, setOptionDetailName] = useState('');
  const [optionDetailPrice, setOptionDetailPrice] = useState('');

  const { mutate: addOptionDetail } = useAddOptionDetail();

  function handleSubmit(e: React.FormEvent) {
    e.preventDefault();

    if (!optionDetailName || !optionDetailPrice) {
      alert('모든 필드를 입력해주세요.');
      return;
    }

    addOptionDetail(
      {
        optionId: row.optionId,
        value: optionDetailName,
        additionalPrice: Number(optionDetailPrice),
      },
      {
        onSuccess: () => {
          openModal(
            <CompleteModal
              title='추가 성공'
              description='옵션 상세 추가가 완료되었습니다.'
              buttonText='확인'
            />,
            'sm'
          );
        },
      }
    );
  }

  return (
    <div className='flex flex-col gap-8 px-10 py-8'>
      <ModalHeader
        title='옵션 상세 추가'
        description='새로운 옵션 상세 정보를 입력하세요. '
      />

      <form onSubmit={handleSubmit}>
        <div className='w-full flex flex-col gap-4'>
          <div className='w-full flex items-center gap-6'>
            <span className='font-preSemiBold text-md'>옵션 그룹명</span>
            <span className='font-preMedium text-md text-longContent'>
              {row.optionNameKr}
            </span>
          </div>

          <div className='w-full flex flex-col gap-2'>
            <Input
              inputId='optionDetailName'
              label='상세 이름'
              inputType='text'
              onChange={(e) => setOptionDetailName(e.target.value)}
              placeholder='상세 이름을 입력하세요. ex) SMALL'
              inputValue={optionDetailName}
            />

            <Input
              inputId='optionDetailPrice'
              label='가격'
              inputType='number'
              onChange={(e) => setOptionDetailPrice(e.target.value)}
              placeholder='가격을 입력하세요. ex) 500'
              inputValue={optionDetailPrice}
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
            <Button
              buttonType='submit'
              text='추가'
              buttonId='addOptionDetail'
            />
          </div>
        </div>
      </form>
    </div>
  );
};

export default AddOptionDetailModal;
