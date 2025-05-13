import React from 'react';

import Button from '@/components/common/Button';
import ModalHeader from '@/components/common/Modal/ModalHeader';
import MenuForm from '@/components/menus/AddMenuForm/MenuForm';

import useModalStore from '@/stores/useModalStore';

interface Props {
  setIsAddMenuClicked: (value: boolean) => void;
}

const AddMenuForm = ({ setIsAddMenuClicked }: Props) => {
  const { closeModal } = useModalStore();

  function handleSubmit(e: React.FormEvent<HTMLFormElement>) {
    e.preventDefault();
    closeModal();
  }

  return (
    <div className='w-full flex flex-col gap-8 p-4 border border-subContent rounded-md max-h-[80vh]'>
      <ModalHeader
        title='새 메뉴 추가'
        description='새로운 메뉴 정보를 입력하세요. 추가 후 상세 정보를 편집할 수 있습니다.'
      />

      <form onSubmit={handleSubmit} className='overflow-y-auto'>
        <MenuForm />

        <div className='w-full mt-8 flex justify-end gap-2'>
          <Button
            buttonType='button'
            text='취소'
            onClick={() => {
              setIsAddMenuClicked(false);
            }}
            cancel
          />
          <Button buttonType='submit' text='추가' />
        </div>
      </form>
    </div>
  );
};

export default AddMenuForm;
