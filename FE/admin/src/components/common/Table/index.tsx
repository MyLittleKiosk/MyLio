import IconEdit from '@/assets/icons/IconEdit';
import IconTrashCan from '@/assets/icons/IconTrashCan';

import { Column, TableProps } from '@/types/tableProps';

const Table = <T extends object>({
  title,
  description,
  columns,
  data,
  className = '',
  onEdit,
  onDelete,
  onView,
}: TableProps<T>) => {
  function checkColumn(column: Column<T>, row: T) {
    switch (column.accessor) {
      case 'optionDetail':
        return (
          <div>
            {(
              row[column.accessor as keyof T] as unknown as Array<{
                optionDetailValue: string;
                additionalPrice: number;
              }>
            ).map((option, index) => (
              <p key={index}>
                {option.optionDetailValue} +{option.additionalPrice}
              </p>
            ))}
          </div>
        );
      case 'imageUrl':
        console.log(
          'row[column.accessor as keyof T]:',
          row[column.accessor as keyof T]
        );
        return (
          <img
            src={String(row[column.accessor as keyof T])}
            alt='메뉴 이미지'
            className='w-10 h-10 rounded-md object-cover'
          />
        );
      case 'edit':
        return (
          <button
            id='edit'
            className='p-1 hover:bg-gray-100 rounded-md'
            onClick={() => onEdit?.(row)}
          >
            <IconEdit />
          </button>
        );
      case 'delete':
        return (
          <button
            id='delete'
            className='p-1 hover:bg-gray-100 rounded-md'
            onClick={() => onDelete?.(row)}
          >
            <IconTrashCan fillColor='#D44848' />
          </button>
        );
      case 'price':
      case 'orderPrice':
        return `₩${String(row[column.accessor as keyof T]).toLocaleString()}`;
      case 'isActivate':
        return (
          <div
            className={`ms-2 w-3 h-3 rounded-full ${
              row[column.accessor as keyof T] ? 'bg-green-500' : 'bg-red-500'
            }`}
          />
        );
      case 'password':
        return '********';
      default:
        return String(row[column.accessor as keyof T]);
    }
  }

  return (
    <article className='w-full flex flex-col gap-2 border border-subContent rounded-md p-4'>
      <h2 className='text-xl font-preBold'>{title}</h2>
      <p className='text-sm font-preRegular'>{description}</p>
      <div className='overflow-x-auto overflow-y-scroll'>
        <table className={`w-full border-collapse ${className}`}>
          <thead className='border-b border-subContent'>
            <tr>
              {columns.map((column, index) => (
                <th
                  key={index}
                  className='px-4 py-3 text-left text-sm font-preLight text-content'
                >
                  {column.header}
                </th>
              ))}
            </tr>
          </thead>
          <tbody className='divide-y divide-subContent'>
            {data.map((row, rowIndex) => (
              <tr
                key={rowIndex}
                className={`hover:bg-subContent/50 ${
                  onView ? 'cursor-pointer' : ''
                }`}
                onClick={() => {
                  onView?.(row);
                }}
              >
                {columns.map((column, colIndex) => (
                  <td
                    key={colIndex}
                    className={
                      column.className || 'px-4 py-3 text-sm font-preRegular'
                    }
                  >
                    {checkColumn(column, row)}
                  </td>
                ))}
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </article>
  );
};

export default Table;
