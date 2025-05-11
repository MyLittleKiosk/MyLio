import Input from '@/components/common/Input';
import Select from '@/components/common/Select';

import { EMAIL_DMAIN } from '@/datas/Account';

interface Props {
  emailId: string;
  onEmailIdChange: (value: string) => void;
  emailIdError: string;
  emailDomain: string | null;
  onEmailDomainChange: (value: string) => void;
  domainError: string;
}

const EmailElement = ({
  emailId,
  onEmailIdChange,
  emailIdError,
  emailDomain,
  onEmailDomainChange,
  domainError,
}: Props) => {
  return (
    <>
      <div className='flex items-center gap-2'>
        <Input
          inputId='email-local-part-input'
          label='이메일'
          placeholder='이메일 아이디를 입력하세요.'
          inputType='text'
          inputValue={emailId}
          onChange={(e) => {
            onEmailIdChange(e.target.value);
          }}
          error={!!emailIdError}
          className='flex-grow'
        />
        <span className='text-subContent'>@</span>
        <Select<string>
          id='email-domain-select'
          options={EMAIL_DMAIN}
          selected={emailDomain}
          placeholder='도메인 선택'
          onChange={(e) => {
            onEmailDomainChange(e.target.value);
          }}
          getOptionLabel={(option) => option}
          getOptionValue={(option) => option}
          className='w-1/3 max-w-[200px]'
          error={!!domainError}
        />
      </div>
      {emailIdError && (
        <p className='text-error text-xs mt-1'>{emailIdError}</p>
      )}
      {domainError && !emailIdError && (
        <p className='text-error text-xs mt-1'>{domainError}</p>
      )}
    </>
  );
};

export default EmailElement;
