import Button from '@/components/common/Button';
import { useLogin } from '@/service/queries/useLogin';
import React, { useRef } from 'react';
const Login = () => {
  const { mutate: login } = useLogin();
  const emailRef = useRef<HTMLInputElement>(null);
  const passwordRef = useRef<HTMLInputElement>(null);
  const kioskIdRef = useRef<HTMLInputElement>(null);
  function handleSubmit(e: React.FormEvent<HTMLFormElement>) {
    e.preventDefault();
    if (!emailRef.current || !passwordRef.current || !kioskIdRef.current) {
      alert('모든 필드를 입력해주세요.');
      return;
    }
    login({
      email: emailRef.current?.value,
      password: passwordRef.current?.value,
      kioskId: Number(kioskIdRef.current?.value),
    });
  }

  return (
    <>
      <div className='flex flex-col items-center justify-center h-screen bg-primary gap-3'>
        <form
          onSubmit={handleSubmit}
          className='flex flex-col gap-3 max-w-md bg-white p-10 rounded-md'
        >
          <h1 className='text-7xl font-preBold text-primary text-center'>
            MaLio
          </h1>
          <div className='flex flex-col'>
            <label htmlFor='id' className='text-sm text-gray-500'>
              아이디
            </label>
            <input
              ref={emailRef}
              id='email'
              className='w-full rounded-md border border-gray-300 px-3 py-3 max-w-sm'
              type='text'
              inputMode='text'
            />
          </div>
          <div>
            <label htmlFor='password' className='text-sm text-gray-500'>
              비밀번호
            </label>
            <input
              ref={passwordRef}
              id='password'
              className='w-full rounded-md border border-gray-300 px-3 py-3 max-w-sm'
              type='password'
            />
          </div>
          <div>
            <label htmlFor='kiosk' className='text-sm text-gray-500'>
              키오스크 아이디
            </label>
            <input
              ref={kioskIdRef}
              id='kiosk'
              className='w-full rounded-md border border-gray-300 px-3 py-3 max-w-sm'
              type='number'
            />
          </div>
          <Button type='submit' content='로그인' />
        </form>
      </div>
    </>
  );
};

export default Login;
