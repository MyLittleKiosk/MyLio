import { useState } from 'react';

import Input from '@/components/common/Input';
import Button from '@/components/common/Button';
import CompleteModal from '@/components/common/CompleteModal';

import useModalStore from '@/stores/useModalStore';
import { useUpdateKiosk } from '@/service/queries/kiosk';
import { KioskType } from '@/types/kiosk';

interface Props {
  row: KioskType;
}

const EditKioskModal = ({ row }: Props) => {
  const [kioskName, setKioskName] = useState(row.name);
  const [groupName, setGroupName] = useState(row.startOrder);

  const [groupNameError, setGroupNameError] = useState({
    error: false,
    message: '',
  });

  const { openModal, closeModal } = useModalStore();
  const { mutate: updateKiosk } = useUpdateKiosk();

  function handleGroupNameChange(value: string) {
    if (/^[A-Z]$/.test(value) || value === '') {
      setGroupNameError({
        error: false,
        message: '',
      });
    } else {
      setGroupNameError({
        error: true,
        message: '알파벳 한 글자만 입력 가능합니다.',
      });
    }

    setGroupName(value.toUpperCase());
  }

  function handleSave() {
    if (kioskName === '' || groupName === '' || groupNameError.error) {
      alert('올바르지 않은 키오스크명 혹은 그룹명입니다.');
      return;
    }

    updateKiosk(
      { kioskId: row.kioskId, name: kioskName, startOrder: groupName },
      {
        onSuccess: () => {
          openModal(
            <CompleteModal
              title='수정 성공'
              description='키오스크 수정에 성공했습니다.'
              buttonText='닫기'
            />
          );
        },
      }
    );
  }

  return (
    <div className='bg-white rounded-xl p-8 flex flex-col gap-6'>
      <div>
        <h2 className='text-xl font-preBold mb-1'>키오스크 정보 수정</h2>
        <p className='text-sm text-gray-500 mb-4'>
          키오스크 정보를 수정합니다.
        </p>
        <div className='flex flex-col gap-4'>
          <Input
            id='kioskName'
            label='키오스크명'
            placeholder='키오스크명을 입력하세요'
            type='text'
            value={kioskName}
            onChange={(e) => setKioskName(e.target.value)}
          />

          <Input
            id='groupName'
            label='그룹명 (A-Z)'
            placeholder='그룹명을 입력하세요'
            type='text'
            value={groupName}
            onChange={(e) => handleGroupNameChange(e.target.value)}
            error={groupNameError.error}
            errorMessage={groupNameError.message}
          />
        </div>
      </div>
      <div className='flex justify-end gap-2 mt-4'>
        <Button type='button' text='취소' cancel onClick={closeModal} />
        <Button type='button' text='저장' onClick={handleSave} />
      </div>
    </div>
  );
};

export default EditKioskModal;
