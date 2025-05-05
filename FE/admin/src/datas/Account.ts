import { Account } from '@/types/account';
import { Column } from '@/types/tableProps';

// 실제 Account에 존재하지 않는 컬럼은 따로 타입 선언
interface AccountTableColumn extends Account {
  password?: string;
  delete?: string;
}

const ACCOUNT_COLUMNS: Column<AccountTableColumn>[] = [
  {
    header: '이름',
    accessor: 'user_name',
  },
  {
    header: '이메일',
    accessor: 'email',
  },
  {
    header: '비밀번호',
    accessor: 'password',
  },
  {
    header: '매장 이름',
    accessor: 'store_name',
  },
  {
    header: '삭제',
    accessor: 'delete',
  },
];

const DUMMY_ACCOUNT_LIST = {
  accounts: [
    {
      account_id: 1,
      user_name: '김하늘',
      email: 'haneul.kim@example.com',
      store_name: '하늘 커피',
      address: '서울특별시 강남구 강남대로 123',
      password: '********',
    },
    {
      account_id: 2,
      user_name: '이준호',
      email: 'junho.lee@example.com',
      store_name: '준호 커피',
      address: '서울특별시 서초구 반포대로 201',
      password: '********',
    },
    {
      account_id: 3,
      user_name: '박지수',
      email: 'jisu.park@example.com',
      store_name: '지수 커피공방',
      address: '서울특별시 마포구 월드컵북로 58',
      password: '********',
    },
    {
      account_id: 4,
      user_name: '최다연',
      email: 'dayeon.choi@example.com',
      store_name: '다연 커피하우스',
      address: '서울특별시 성동구 왕십리로 85',
      password: '********',
    },
    {
      account_id: 5,
      user_name: '정우성',
      email: 'woosung.jung@example.com',
      store_name: '우성 브루잉 카페',
      address: '서울특별시 용산구 한강대로 320',
      password: '********',
    },
  ],
  page_number: 1,
  total_pages: 1,
  total_elements: 5,
  page_size: 10,
  first: true,
  last: true,
};

const EMAIL_DMAIN = [
  'gmail.com',
  'naver.com',
  'daum.net',
  'hotmail.com',
  'outlook.com',
  'yahoo.com',
  'msn.com',
];

export { ACCOUNT_COLUMNS, DUMMY_ACCOUNT_LIST, EMAIL_DMAIN };
