import { Pagenation } from '@/types/apiResponse';
import clsx from 'clsx';

interface Props {
  pageInfo: Pagenation;
  onChangePage: (page: number) => void;
}

const PageNavigation = ({ pageInfo, onChangePage }: Props) => {
  const boundary = Math.floor((pageInfo.pageNumber - 1) / 10) * 10;
  const len =
    Math.floor((pageInfo.totalPages - 1) / 10) ==
    Math.floor((pageInfo.pageNumber - 1) / 10)
      ? pageInfo.totalPages - boundary
      : 10;

  const pageBtnCount = Array.from(
    { length: len },
    (_, index) => boundary + index + 1
  );

  const nextBtn =
    boundary + 10 > pageInfo.totalPages ? pageInfo.totalPages : boundary + 11;
  const prevBtn = boundary < 1 ? 1 : boundary;

  return (
    <div className='flex items-center justify-center gap-2 font-preRegular'>
      <div
        id='firstPage'
        className='cursor-pointer'
        onClick={() => onChangePage(1)}
      >
        처음
      </div>
      <div
        id='prevPage'
        className='cursor-pointer'
        onClick={() => onChangePage(prevBtn)}
      >
        이전
      </div>
      <div className='flex items-center justify-center gap-2'>
        {pageBtnCount.map((page) => (
          <div
            key={page}
            className={clsx(
              'cursor-pointer px-1',
              pageInfo.pageNumber === page
                ? 'font-preBold underline'
                : 'hover:text-content'
            )}
            onClick={() => onChangePage(page)}
          >
            {page}
          </div>
        ))}
      </div>
      <div
        id='nextPage'
        className='cursor-pointer'
        onClick={() => onChangePage(nextBtn)}
      >
        다음
      </div>
      <div
        id='lastPage'
        className='cursor-pointer'
        onClick={() => onChangePage(pageInfo.totalPages)}
      >
        끝
      </div>
    </div>
  );
};

export default PageNavigation;
