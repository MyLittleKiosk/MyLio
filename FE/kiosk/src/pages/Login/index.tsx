import Button from '@/components/common/Button';

const Login = () => {
  return (
    <>
      <div className='flex flex-col items-center justify-center h-screen bg-primary gap-3'>
        <section className='flex flex-col gap-3 max-w-md bg-white p-10 rounded-md'>
          <h1 className='text-7xl font-preBold text-primary text-center'>
            MaLio
          </h1>
          <div className='flex flex-col'>
            <label htmlFor='id' className='text-sm text-gray-500'>
              아이디
            </label>
            <input
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
              className='w-full rounded-md border border-gray-300 px-3 py-3 max-w-sm'
              type='password'
            />
          </div>
          <div>
            <label htmlFor='kiosk' className='text-sm text-gray-500'>
              키오스크 아이디
            </label>
            <input
              className='w-full rounded-md border border-gray-300 px-3 py-3 max-w-sm'
              type='text'
            />
          </div>
          <Button content='로그인' onClick={() => {}} />
        </section>
      </div>
    </>
  );
};

export default Login;
