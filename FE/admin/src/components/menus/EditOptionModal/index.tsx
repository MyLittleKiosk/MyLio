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
  useDeleteOptionDetail,
  useEditOptionDetail,
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
    row.optionDetails.map((optionDetail) => optionDetail.optionDetailValue)
  );
  const [optionDetailPriceEdit, setOptionDetailPriceEdit] = useState(
    row.optionDetails.map((optionDetail) => optionDetail.additionalPrice)
  );
  const [optionDetailNameAdd, setOptionDetailNameAdd] = useState('');
  const [optionDetailPriceAdd, setOptionDetailPriceAdd] = useState(0);

  const { mutate: editOptionGroup } = useEditOptionGroup();
  const { mutate: addOptionDetail } = useAddOptionDetail();
  const { mutate: editOptionDetail } = useEditOptionDetail();
  const { mutate: deleteOptionDetail } = useDeleteOptionDetail();

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

  function handleOptionDetailEdit(optionDetailId: number) {
    const index = row.optionDetails.findIndex(
      (detail) => detail.optionDetailId === optionDetailId
    );

    editOptionDetail(
      {
        optionDetailId,
        value: optionDetailValueEdit[index],
        additionalPrice: optionDetailPriceEdit[index],
      },
      {
        onSuccess: () => {
          openModal(
            <CompleteModal
              title='옵션 상세 수정'
              description='옵션 상세 수정이 완료되었습니다.'
              buttonText='확인'
            />,
            'sm'
          );
        },
      }
    );
  }

  function handleOptionDetailDelete(optionDetailId: number) {
    if (confirm('정말 삭제하시겠습니까?')) {
      deleteOptionDetail(optionDetailId, {
        onSuccess: () => {
          openModal(
            <CompleteModal
              title='옵션 상세 삭제'
              description='옵션 상세 삭제가 완료되었습니다.'
              buttonText='확인'
            />,
            'sm'
          );
        },
      });
    }
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
            id='optionGroupNameEdit'
            label='옵션 그룹명'
            type='text'
            onChange={(e) => setOptionGroupNameKrEdit(e.target.value)}
            placeholder='한글명'
            value={optionGroupNameKrEdit}
            className='w-[60%]'
          />

          <Input
            id='optionGroupNameEnEdit'
            type='text'
            onChange={(e) => setOptionGroupNameEnEdit(e.target.value)}
            placeholder='영문명'
            value={optionGroupNameEnEdit}
            className='w-[30%]'
          />
          <Button
            id='optionGroupNameEditBtn'
            type='submit'
            text='수정'
            className='w-[15%]'
          />
        </div>
      </form>

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
            {row.optionDetails.map((optionDetail, index) => (
              <tr key={optionDetail.optionDetailId} className='w-full'>
                <td className='w-[30%] text-center p-2'>
                  <Input
                    id={`optionDetailValueEdit-${optionDetail.optionDetailId}`}
                    type='text'
                    value={optionDetailValueEdit[index]}
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
                    id={`optionDetailPriceEdit-${optionDetail.optionDetailId}`}
                    type='number'
                    value={optionDetailPriceEdit[index]}
                    min={0}
                    max={1000000}
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
                  <button
                    id='optionDetailEdit'
                    className='w-full flex justify-center cursor-pointer'
                    onClick={() =>
                      handleOptionDetailEdit(optionDetail.optionDetailId)
                    }
                  >
                    <IconEdit />
                  </button>
                </td>
                <td className='w-[20%] text-center'>
                  <button
                    id='optionDetailDelete'
                    className='w-full flex justify-center cursor-pointer'
                    onClick={() =>
                      handleOptionDetailDelete(optionDetail.optionDetailId)
                    }
                  >
                    <IconTrashCan fillColor='#D44848' />
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      <form onSubmit={handleOptionDetailAdd}>
        <div className='flex gap-4 items-center'>
          <p className='font-preSemiBold text-md'>옵션 상세 추가</p>
          <Input
            id={`optionDetailNameAdd`}
            type='text'
            value={optionDetailNameAdd}
            onChange={(e) => setOptionDetailNameAdd(e.target.value)}
            placeholder='옵션 상세명'
            inputClassName='w-[80%]'
          />

          <Input
            id={`optionDetailPriceAdd`}
            type='number'
            min={0}
            max={1000000}
            value={optionDetailPriceAdd}
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
