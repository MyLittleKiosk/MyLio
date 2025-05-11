import { AccountType } from '@/types/account';
import { Column } from '@/types/tableProps';

// 실제 Account에 존재하지 않는 컬럼은 따로 타입 선언
interface AccountTableColumn extends AccountType {
  password?: string;
  delete?: string;
}

const ACCOUNT_COLUMNS: Column<AccountTableColumn>[] = [
  {
    header: '이름',
    accessor: 'userName',
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
    accessor: 'storeName',
  },
  {
    header: '삭제',
    accessor: 'delete',
  },
];

const DUMMY_ACCOUNT_LIST = {
  accounts: [
    {
      accountId: 1,
      userName: '김하늘',
      email: 'haneul.kim@example.com',
      storeName: '하늘 커피',
      address: '서울특별시 강남구 강남대로 123',
    },
    {
      accountId: 2,
      userName: '이준호',
      email: 'junho.lee@example.com',
      storeName: '준호 커피',
      address: '서울특별시 서초구 반포대로 201',
    },
    {
      accountId: 3,
      userName: '박지수',
      email: 'jisu.park@example.com',
      storeName: '지수 커피공방',
      address: '서울특별시 마포구 월드컵북로 58',
    },
    {
      accountId: 4,
      userName: '최다연',
      email: 'dayeon.choi@example.com',
      storeName: '다연 커피하우스',
      address: '서울특별시 성동구 왕십리로 85',
    },
    {
      accountId: 5,
      userName: '정우성',
      email: 'woosung.jung@example.com',
      storeName: '우성 브루잉 카페',
      address: '서울특별시 용산구 한강대로 320',
    },
  ],
  pageNumber: 1,
  totalPages: 1,
  totalElements: 5,
  pageSize: 10,
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
