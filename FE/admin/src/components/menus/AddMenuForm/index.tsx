import React from 'react';

import useModalStore from '@/stores/useModalStore';
import { useAddMenu } from '@/service/queries/menu';

import Button from '@/components/common/Button';
import ModalHeader from '@/components/common/Modal/ModalHeader';
import MenuForm from '@/components/menus/AddMenuForm/MenuForm';
import {
  MenuFormProvider,
  useMenuFormContext,
} from '@/components/menus/AddMenuForm/MenuFormContext';
import CompleteModal from '@/components/common/CompleteModal';

interface Props {
  setIsAddMenuClicked: (value: boolean) => void;
}

const AddMenuForm = ({ setIsAddMenuClicked }: Props) => {
  return (
    <MenuFormProvider>
      <AddMenuFormContent setIsAddMenuClicked={setIsAddMenuClicked} />
    </MenuFormProvider>
  );
};

const AddMenuFormContent = ({
  setIsAddMenuClicked,
}: {
  setIsAddMenuClicked: (value: boolean) => void;
}) => {
  const { menuAddData, imageFile, checkValidation } = useMenuFormContext();
  const { openModal } = useModalStore();

  const { mutate: addMenu } = useAddMenu();

  function handleSubmit(e: React.FormEvent<HTMLFormElement>) {
    e.preventDefault();

    if (!checkValidation()) {
      alert('모든 항목을 입력해주세요.');
      return;
    }

    // API 호출
    addMenu(
      { menu: menuAddData, file: imageFile || undefined },
      {
        onSuccess: () => {
          openModal(
            <CompleteModal
              title='메뉴 추가 성공'
              description='메뉴가 추가되었습니다.'
              buttonText='확인'
            />
          );
          setIsAddMenuClicked(false);
        },
      }
    );
  }

  return (
    <div className='w-full flex flex-col gap-8 p-4 border border-subContent rounded-md max-h-[80vh]'>
      <ModalHeader
        title='새 메뉴 추가'
        description='새로운 메뉴 정보를 입력하세요. 추가 후 상세 정보를 편집할 수 있습니다.'
      />

      <form
        onSubmit={handleSubmit}
        className='overflow-y-auto w-full flex flex-col items-center'
      >
        <MenuForm />

        <div className='w-full mt-8 flex justify-end gap-2'>
          <Button
            type='button'
            text='취소'
            onClick={() => {
              setIsAddMenuClicked(false);
            }}
            cancel
          />
          <Button type='submit' text='추가' />
        </div>
      </form>
    </div>
  );
};

export default AddMenuForm;
