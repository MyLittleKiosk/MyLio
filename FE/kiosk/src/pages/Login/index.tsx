import Button from '@/components/common/Button';

const Login = () => {
  return (
    <>
      <div className='flex flex-col items-center justify-center h-screen bg-primary/10 gap-3'>
        <div className='flex flex-col gap-3 max-w-md'>
          <h1 className='text-7xl font-bold text-primary text-center'>MaLio</h1>
          <div className='flex flex-col'>
            <label htmlFor='id' className='text-sm text-gray-500'>
              아이디
            </label>
            <input
              className='w-full rounded-md border border-gray-300 px-3 py-3 max-w-sm'
              type='text'
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
          <Button content='로그인' onClick={() => {}} />
        </div>
      </div>
    </>
  );
};

export default Login;
