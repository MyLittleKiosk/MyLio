import React, { useState } from 'react';

import Input from '@components/common/Input';
import Modal from '@components/common/Modal';
import Button from '@components/common/Button';

import useModalStore from '@/stores/useModalStore';

import IconAccount from '@/assets/icons/IconAccount.tsx';

const Statistics = () => {
  const { openModal } = useModalStore();

  const [inputValue, setInputValue] = useState('');

  function handleInputChange(event: React.ChangeEvent<HTMLInputElement>) {
    setInputValue(event.target.value);
  }

  return (
    <>
      <div className='w-full p-2'>
        <Button
          onClick={() => openModal(<div className='w-12 h-10'>Modal</div>)}
          buttonType='button'
          text='Open Modal'
          className='mb-2'
          icon={<IconAccount fillColor='white' />}
        />

        <Input
          label='Label'
          inputId='input'
          placeholder='placeholder'
          inputType='text'
          inputValue={inputValue}
          onChange={handleInputChange}
          error={false}
          className='mb-3'
          disabled
        />
      </div>
      <Modal />
    </>
  );
};

export default Statistics;
