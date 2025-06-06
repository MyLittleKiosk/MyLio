import React, { useState } from 'react';

import EmailElement from '@/components/account/AddAccountModal/EmailElement';
import Button from '@/components/common/Button';
import CompleteModal from '@/components/common/CompleteModal';
import Input from '@/components/common/Input';
import ModalHeader from '@/components/common/Modal/ModalHeader';
import useModalStore from '@/stores/useModalStore';

import { usePostAccount } from '@/service/queries/account';
import { AccountForm } from '@/types/account';

interface AccountFormData {
  userName: string;
  emailId: string;
  emailDomain: string;
  storeName: string;
  address: string;
}

interface AccountFormErrors {
  userName?: string;
  emailId?: string;
  emailDomain?: string;
  storeName?: string;
  address?: string;
}

const AddAccountModal = () => {
  const { closeModal } = useModalStore();
  const { openModal } = useModalStore();
  const { mutate: createAccount } = usePostAccount();

  const [formData, setFormData] = useState<AccountFormData>({
    userName: '',
    emailId: '',
    emailDomain: '',
    storeName: '',
    address: '',
  });

  const [errors, setErrors] = useState<AccountFormErrors>({});

  function handleChange(field: keyof AccountFormData, value: string) {
    setFormData((prev) => ({ ...prev, [field]: value }));

    if (errors[field as keyof AccountFormErrors]) {
      setErrors((prev) => ({ ...prev, [field]: undefined }));
    } else if (field === 'emailId' && errors.emailDomain) {
      setErrors((prev) => ({ ...prev, emailDomain: undefined }));
    }
  }

  /**
   * 유효성 검사 함수
   * @returns isValid: 유효성 검사 결과, errors: 에러 메시지
   */
  function validateForm(): { isValid: boolean; errors: AccountFormErrors } {
    const newErrors: AccountFormErrors = {};
    let isValid = true;

    if (!formData.userName.trim()) {
      newErrors.userName = '사용자 이름을 입력해주세요.';
      isValid = false;
    }
    if (!formData.emailId.trim()) {
      newErrors.emailId = '이메일 아이디를 입력해주세요.';
      isValid = false;
    }
    if (!formData.emailDomain) {
      newErrors.emailDomain = '도메인을 선택해주세요.';
      isValid = false;
    }
    if (!formData.storeName.trim()) {
      newErrors.storeName = '매장 이름을 입력해주세요.';
      isValid = false;
    }
    if (!formData.address.trim()) {
      newErrors.address = '주소를 입력하세요.';
      isValid = false;
    }

    return { isValid, errors: newErrors };
  }

  function handleSubmit(e: React.FormEvent<HTMLFormElement>) {
    e.preventDefault();

    const validationResult = validateForm();
    setErrors(validationResult.errors);

    // 유효성 검사 통과 시 처리
    if (validationResult.isValid) {
      const email = `${formData.emailId}@${formData.emailDomain}`;
      const accountForm: AccountForm = {
        userName: formData.userName,
        email,
        storeName: formData.storeName,
        address: formData.address,
      };
      createAccount({ account: accountForm });
      openModal(
        <CompleteModal
          title='계정 추가'
          description='계정 추가가 완료되었습니다.'
          buttonText='확인'
        />
      );
    }
  }

  return (
    <div id='add-account-modal' className='flex flex-col gap-8 px-10 py-8'>
      <ModalHeader
        title='계정 추가'
        description='새로운 매장 정보를 입력하세요. 추가 후 매장 계정에서 편집할 수 있습니다.'
      />
      <form onSubmit={handleSubmit}>
        <div className='flex flex-col gap-2'>
          <div id='account-name-input'>
            <Input
              id='accountId'
              label='사용자 이름'
              placeholder='사용자 이름을 입력하세요.'
              type='text'
              value={formData.userName}
              onChange={(e) => handleChange('userName', e.target.value)}
              error={!!errors.userName}
            />
            {errors.userName && (
              <p className='text-error text-xs mt-1'>{errors.userName}</p>
            )}
          </div>

          <div className='flex flex-col gap-2'>
            <EmailElement
              emailId={formData.emailId}
              onEmailIdChange={(value) => handleChange('emailId', value)}
              emailIdError={errors.emailId || ''}
              emailDomain={formData.emailDomain}
              onEmailDomainChange={(value) =>
                handleChange('emailDomain', value)
              }
              domainError={errors.emailDomain || ''}
            />
          </div>

          <div id='store-name-input'>
            <Input
              id='storeId'
              label='매장 이름'
              placeholder='매장 이름을 입력하세요.'
              type='text'
              value={formData.storeName}
              onChange={(e) => handleChange('storeName', e.target.value)}
              error={!!errors.storeName}
            />
            {errors.storeName && (
              <p className='text-error text-xs mt-1'>{errors.storeName}</p>
            )}
          </div>

          <div id='address-input'>
            <Input
              id='addressId'
              label='매장 주소'
              placeholder='주소를 입력하세요.'
              type='text'
              value={formData.address}
              onChange={(e) => handleChange('address', e.target.value)}
              error={!!errors.address}
            />
            {errors.address && (
              <p className='text-error text-xs mt-1'>{errors.address}</p>
            )}
          </div>
        </div>
        <div className='w-full mt-8 flex justify-end gap-2'>
          <Button type='button' text='취소' onClick={closeModal} cancel />
          <Button type='submit' text='생성' />
        </div>
      </form>
    </div>
  );
};

export default AddAccountModal;
