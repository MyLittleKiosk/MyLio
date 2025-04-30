import React, { useState } from 'react';
import Input from '@/components/common/Input';
import Modal from '@/components/common/Modal';
import useModalStore from '@/stores/useModalStore';

const Statistics = () => {
  const { openModal } = useModalStore();

  const [inputValue, setInputValue] = useState('');

  function handleInputChange(event: React.ChangeEvent<HTMLInputElement>) {
    setInputValue(event.target.value);
  }

  return (
    <>
      <div className='w-full p-2'>
        <button
          onClick={() => openModal(<div className='w-12 h-10'>Modal</div>)}
          className='bg-primary text-white px-4 py-2 rounded-md mb-2'
        >
          Open Modal
        </button>

        <Input
          label='Label'
          id='input'
          placeholder='placeholder'
          type='text'
          value={inputValue}
          onChange={handleInputChange}
          error={false}
          disabled
        />
      </div>
      <Modal />
    </>
  );
};

export default Statistics;
