import Button from '@/components/common/Button';
import Input from '@/components/common/Input';
import { useState } from 'react';

const Login = () => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [autoLogin, setAutoLogin] = useState(false);

  return (
    <div className='w-full h-screen flex flex-col justify-center items-center bg-[#5B8CFF]'>
      <section className='w-[400px] bg-white rounded-xl shadow-lg p-10 flex flex-col gap-6'>
        <h1 className='text-2xl font-preBold text-center mb-4'>로그인</h1>
        <Input
          inputId='email'
          placeholder='이메일'
          inputType='text'
          inputValue={email}
          onChange={(e) => setEmail(e.target.value)}
        />
        <Input
          inputId='password'
          placeholder='비밀번호'
          inputType='password'
          inputValue={password}
          onChange={(e) => setPassword(e.target.value)}
        />
        <div className='flex items-center gap-2 mt-2'>
          <input
            id='auto-login'
            type='checkbox'
            checked={autoLogin}
            onChange={() => setAutoLogin((prev) => !prev)}
            className='accent-[#5B8CFF] w-4 h-4'
          />
          <label
            htmlFor='auto-login'
            className='text-sm font-preRegular text-gray-700'
          >
            자동 로그인
          </label>
        </div>
        <Button
          buttonType='submit'
          className='w-full h-[50px] flex justify-center items-center mt-4 font-preSemiBold bg-[#5B8CFF] hover:bg-[#4072e6]'
          onClick={() => {}}
          text='로그인'
        />
      </section>
    </div>
  );
};

export default Login;
