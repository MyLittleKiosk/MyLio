import React from 'react';

import useModalStore from '@/stores/useModalStore';
import { useGetMenuById, useUpdateMenu } from '@/service/queries/menu';

import Button from '@/components/common/Button';
import ModalHeader from '@/components/common/Modal/ModalHeader';
import {
  MenuEditProvider,
  useMenuEditContext,
} from '@/components/menus/EditMenuForm/MenuEditContext';
import CompleteModal from '@/components/common/CompleteModal';
import EditForm from '@/components/menus/EditMenuForm/EditForm';

import { MenuDetailGetType } from '@/types/menus';
import { useGetCategory } from '@/service/queries/category';
import { useGetIngredientList } from '@/service/queries/ingredient';

interface Props {
  setIsEditMenuClicked: (value: boolean) => void;
  clickedMenuId: number;
}

const EditMenuForm = ({ setIsEditMenuClicked, clickedMenuId }: Props) => {
  const { data: menuDetail } = useGetMenuById(clickedMenuId);
  const { data: category } = useGetCategory();
  const { data: ingredient } = useGetIngredientList();

  return (
    <MenuEditProvider
      menuDetail={menuDetail as MenuDetailGetType}
      category={category || []}
      ingredient={ingredient || []}
    >
      <EditMenuFormContent
        setIsEditMenuClicked={setIsEditMenuClicked}
        clickedMenuId={clickedMenuId}
      />
    </MenuEditProvider>
  );
};

const EditMenuFormContent = ({
  setIsEditMenuClicked,
  clickedMenuId,
}: {
  setIsEditMenuClicked: (value: boolean) => void;
  clickedMenuId: number;
}) => {
  const { menuAddData, imageFile, checkValidation } = useMenuEditContext();
  const { openModal } = useModalStore();
  const { mutate: updateMenu } = useUpdateMenu();

  function handleSubmit(e: React.FormEvent<HTMLFormElement>) {
    e.preventDefault();

    if (!checkValidation(false)) {
      return;
    }

    // API 호출
    updateMenu(
      {
        menuId: clickedMenuId,
        menu: menuAddData,
        file: imageFile || undefined,
      },
      {
        onSuccess: () => {
          openModal(
            <CompleteModal
              title='메뉴 편집 성공'
              description='메뉴가 수정되었습니다.'
              buttonText='확인'
            />
          );
          setIsEditMenuClicked(false);
        },
      }
    );
  }

  return (
    <div className='w-full flex flex-col gap-8 p-4 border border-subContent rounded-md max-h-[80vh]'>
      <ModalHeader
        title='메뉴 편집'
        description='메뉴 정보를 편집할 수 있습니다.'
      />

      <form
        onSubmit={handleSubmit}
        className='overflow-y-auto w-full flex flex-col items-center'
      >
        <EditForm />

        <div className='w-full mt-8 flex justify-end gap-2'>
          <Button
            type='button'
            text='취소'
            onClick={() => {
              setIsEditMenuClicked(false);
            }}
            cancel
          />
          <Button type='submit' text='수정' />
        </div>
      </form>
    </div>
  );
};

export default EditMenuForm;
