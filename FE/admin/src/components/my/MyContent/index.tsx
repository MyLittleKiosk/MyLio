import Modal from '@/components/common/Modal';
import MyInfo from '@/components/my/MyInfo';
import MyPassword from '@/components/my/MyPassword';
import { useGetAccountDetail } from '@/service/queries/account';

const MyContent = () => {
  const { data: userInfo } = useGetAccountDetail();

  return (
    <>
      <div className='w-full h-full p-4 flex flex-col gap-5'>
        <h1 className='text-2xl font-preBold'>마이페이지</h1>
        <div className='w-full h-full flex flex-col gap-5'>
          <div className='w-full max-w-[1000px] flex flex-col gap-5'>
            <h1 className='text-2xl font-preBold'>내 정보</h1>
            <MyInfo userInfo={userInfo} />
          </div>
          <div className='w-full h-[1px] bg-subContent' />
          <div className='w-full max-w-[1000px] flex flex-col gap-5'>
            <h1 className='text-2xl font-preBold'>비밀번호 변경</h1>
            <MyPassword />
          </div>
        </div>
      </div>
      <Modal />
    </>
  );
};

export default MyContent;
