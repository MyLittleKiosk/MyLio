import React, { useState } from 'react';
import Button from '@/components/common/Button';
import Input from '@/components/common/Input';
import { useLogin } from '@/service/queries/user';
const Login = () => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [autoLogin, setAutoLogin] = useState(false);
  const [error, setError] = useState({ email: false, password: false });
  const { mutate } = useLogin();
  function handleLogin() {
    const newError = {
      email: email === '',
      password: password === '',
    };
    setError(newError);
    if (newError.email || newError.password) return;
    mutate({ email, password });
  }

  function handleEmailChange(e: React.ChangeEvent<HTMLInputElement>) {
    setEmail(e.target.value);
    if (error.email) setError((prev) => ({ ...prev, email: false }));
  }

  function handlePasswordChange(e: React.ChangeEvent<HTMLInputElement>) {
    setPassword(e.target.value);
    if (error.password) setError((prev) => ({ ...prev, password: false }));
  }

  return (
    <div className='w-full h-screen flex flex-col justify-center items-center bg-[#5B8CFF]'>
      <section className='w-[400px] bg-white rounded-xl shadow-lg p-10 flex flex-col gap-6 box-border'>
        <h1 className='text-2xl font-preBold text-center mb-4'>로그인</h1>
        <Input
          inputId='email'
          placeholder='이메일'
          inputType='text'
          className='box-border'
          inputValue={email}
          onChange={handleEmailChange}
          error={error.email}
        />
        <Input
          inputId='password'
          placeholder='비밀번호'
          className='box-border'
          inputType='password'
          inputValue={password}
          onChange={handlePasswordChange}
          error={error.password}
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
          onClick={handleLogin}
          text='로그인'
        />
      </section>
    </div>
  );
};

export default Login;
