import React, { useState } from 'react';

import IconAdd from '@/assets/icons/IconAdd';
import IconEdit from '@/assets/icons/IconEdit';
import IconTrashCan from '@/assets/icons/IconTrashCan';

import Button from '@/components/common/Button';
import Input from '@/components/common/Input';
import ModalHeader from '@/components/common/Modal/ModalHeader';
import CompleteModal from '@/components/common/CompleteModal';

import { OptionGroup } from '@/types/options';
import {
  useAddOptionDetail,
  useEditOptionGroup,
} from '@/service/queries/option';
import useModalStore from '@/stores/useModalStore';

interface Props {
  row: OptionGroup;
}

const EditOptionModal = ({ row }: Props) => {
  const { openModal } = useModalStore();

  const [optionGroupNameKrEdit, setOptionGroupNameKrEdit] = useState(
    row.optionNameKr
  );
  const [optionGroupNameEnEdit, setOptionGroupNameEnEdit] = useState(
    row.optionNameEn
  );
  const [optionDetailValueEdit, setOptionDetailValueEdit] = useState(
    row.optionDetail.map((optionDetail) => optionDetail.optionDetailValue)
  );
  const [optionDetailPriceEdit, setOptionDetailPriceEdit] = useState(
    row.optionDetail.map((optionDetail) => optionDetail.additionalPrice)
  );
  const [optionDetailNameAdd, setOptionDetailNameAdd] = useState('');
  const [optionDetailPriceAdd, setOptionDetailPriceAdd] = useState(0);

  const { mutate: editOptionGroup } = useEditOptionGroup();
  const { mutate: addOptionDetail } = useAddOptionDetail();

  function handleOptionGroupEdit(e: React.FormEvent) {
    e.preventDefault();

    editOptionGroup(
      {
        optionId: row.optionId,
        optionNameKr: optionGroupNameKrEdit,
        optionNameEn: optionGroupNameEnEdit,
      },
      {
        onSuccess: () => {
          openModal(
            <CompleteModal
              title='옵션 그룹명 수정'
              description='옵션 그룹명 수정이 완료되었습니다.'
              buttonText='확인'
            />,
            'sm'
          );
        },
      }
    );
  }

  function handleOptionDetailEdit(e: React.FormEvent) {
    e.preventDefault();
  }

  function handleOptionDetailAdd(e: React.FormEvent) {
    e.preventDefault();

    if (!optionDetailNameAdd || !optionDetailPriceAdd) {
      alert('모든 필드를 입력해주세요.');
      return;
    }

    addOptionDetail(
      {
        optionId: row.optionId,
        value: optionDetailNameAdd,
        additionalPrice: Number(optionDetailPriceAdd),
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
        title='옵션 편집'
        description='옵션 내용을 수정, 삭제, 추가할 수 있습니다.'
      />

      <form onSubmit={handleOptionGroupEdit}>
        <div className='w-full flex gap-4'>
          <Input
            inputId='optionGroupNameEdit'
            label='옵션 그룹명'
            inputType='text'
            onChange={(e) => setOptionGroupNameKrEdit(e.target.value)}
            placeholder='한글명'
            inputValue={optionGroupNameKrEdit}
            className='w-[60%]'
          />

          <Input
            inputId='optionGroupNameEnEdit'
            inputType='text'
            onChange={(e) => setOptionGroupNameEnEdit(e.target.value)}
            placeholder='영문명'
            inputValue={optionGroupNameEnEdit}
            className='w-[30%]'
          />
          <Button
            buttonId='optionGroupNameEdit'
            buttonType='submit'
            text='수정'
            className='w-[15%]'
          />
        </div>
      </form>

      <form onSubmit={handleOptionDetailEdit}>
        <div className='flex flex-col gap-4 w-full'>
          <p className='w-[10%] font-preSemiBold text-md'>옵션 상세</p>
          <table className='w-[90%] border-collapse'>
            <thead className='w-full border-b border-subContent'>
              <tr className='w-full font-preRegular text-sm text-content2'>
                <th className='w-[30%] p-2'>옵션 상세명</th>
                <th className='w-[30%]'>추가 가격</th>
                <th className='w-[20%]'>수정</th>
                <th className='w-[20%]'>삭제</th>
              </tr>
            </thead>
            <tbody>
              {row.optionDetail.map((optionDetail, index) => (
                <tr key={optionDetail.optionDetailId} className='w-full'>
                  <td className='w-[30%] text-center p-2'>
                    <Input
                      inputId={`optionDetailValueEdit-${optionDetail.optionDetailId}`}
                      inputType='text'
                      inputValue={optionDetailValueEdit[index]}
                      onChange={(e) =>
                        setOptionDetailValueEdit(
                          optionDetailValueEdit.map((value, i) =>
                            i === index ? e.target.value : value
                          )
                        )
                      }
                      placeholder='옵션 상세명'
                      inputClassName='w-[60%] mx-auto'
                    />
                  </td>
                  <td className='w-[30%] text-center'>
                    <Input
                      inputId={`optionDetailPriceEdit-${optionDetail.optionDetailId}`}
                      inputType='number'
                      inputValue={optionDetailPriceEdit[index]}
                      onChange={(e) =>
                        setOptionDetailPriceEdit(
                          optionDetailPriceEdit.map((value, i) =>
                            i === index ? Number(e.target.value) : value
                          )
                        )
                      }
                      placeholder='추가 가격'
                      inputClassName='w-[60%] mx-auto'
                    />
                  </td>
                  <td className='w-[20%] text-center'>
                    <div className='flex justify-center'>
                      <IconEdit onClick={() => {}} />
                    </div>
                  </td>
                  <td className='w-[20%] text-center'>
                    <div className='flex justify-center'>
                      <IconTrashCan onClick={() => {}} />
                    </div>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </form>

      <form onSubmit={handleOptionDetailAdd}>
        <div className='flex gap-4 items-center'>
          <p className='font-preSemiBold text-md'>옵션 상세 추가</p>
          <Input
            inputId={`optionDetailNameAdd`}
            inputType='text'
            inputValue={optionDetailNameAdd}
            onChange={(e) => setOptionDetailNameAdd(e.target.value)}
            placeholder='옵션 상세명'
            inputClassName='w-[80%]'
          />

          <Input
            inputId={`optionDetailPriceAdd`}
            inputType='number'
            inputValue={optionDetailPriceAdd}
            onChange={(e) => setOptionDetailPriceAdd(Number(e.target.value))}
            placeholder='추가 가격'
            inputClassName='w-[80%]'
          />

          <button id='optionDetailAdd' type='submit' className='cursor-pointer'>
            <IconAdd />
          </button>
        </div>
      </form>
    </div>
  );
};

export default EditOptionModal;
