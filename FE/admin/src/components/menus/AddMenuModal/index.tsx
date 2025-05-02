import React, { useState } from 'react';
import Step1 from './Step1';
import Step2 from './Step2';
import Button from '@/components/common/Button';
import ModalHeader from '@/components/common/Modal/ModalHeader';

import useModalStore from '@/stores/useModalStore';

const AddMenuModal = () => {
  const { closeModal } = useModalStore();

  const [nextStep, setNextStep] = useState<number>(1);

  function handleSubmit(e: React.FormEvent<HTMLFormElement>) {
    e.preventDefault();
    closeModal();
  }

  return (
    <div className='flex flex-col gap-8 px-10 py-8'>
      <ModalHeader
        title='새 메뉴 추가'
        description='새로운 메뉴 정보를 입력하세요. 추가 후 상세 정보를 편집할 수 있습니다.'
      />

      <form onSubmit={handleSubmit}>
        {nextStep === 1 && <Step1 />}
        {nextStep === 2 && <Step2 />}

        <div className='w-full mt-8 flex justify-end gap-2'>
          {nextStep === 1 && (
            <>
              <Button
                buttonType='button'
                text='취소'
                onClick={() => {
                  closeModal();
                }}
                cancel
              />
              <Button
                buttonType='button'
                text='다음'
                onClick={() => {
                  setNextStep(2);
                }}
              />
            </>
          )}
          {nextStep === 2 && (
            <>
              <Button
                buttonType='button'
                text='이전'
                onClick={() => {
                  setNextStep(1);
                }}
                cancel
              />
              <Button buttonType='submit' text='추가' />
            </>
          )}
        </div>
      </form>
    </div>
  );
};

export default AddMenuModal;
