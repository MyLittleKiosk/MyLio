import React, { useState } from 'react';

import Input from '@components/common/Input';
import Modal from '@components/common/Modal';
import Select from '@components/common/Select';
import Button from '@components/common/Button';

import useModalStore from '@/stores/useModalStore';

import IconAccount from '@/assets/icons/IconAccount.tsx';

const Statistics = () => {
  const { openModal } = useModalStore();

  const [inputValue, setInputValue] = useState('');
  const [selectedValue, setSelectedValue] = useState('');

  function handleInputChange(event: React.ChangeEvent<HTMLInputElement>) {
    setInputValue(event.target.value);
  }

  function handleSelectChange(event: React.ChangeEvent<HTMLSelectElement>) {
    setSelectedValue(event.target.value);
  }

  return (
    <>
      <div className='w-full p-2'>
        <Button
          onClick={() => openModal(<div className='w-12 h-10'>Modal</div>)}
          type='button'
          text='Open Modal'
          className='mb-2'
          icon={<IconAccount fillColor='white' />}
        />

        <Input
          label='Label'
          id='input'
          placeholder='placeholder'
          type='text'
          value={inputValue}
          onChange={handleInputChange}
          error={false}
          className='mb-3'
          disabled
        />

        <Select
          options={[
            { key: '1', value: '옵션 1' },
            { key: '2', value: '옵션 2' },
            { key: '3', value: '옵션 3' },
          ]}
          label='Select Label'
          selected={selectedValue}
          placeholder='옵션을 선택해 주세요'
          onChange={handleSelectChange}
          error={false}
        />
      </div>
      <Modal />
    </>
  );
};

export default Statistics;
