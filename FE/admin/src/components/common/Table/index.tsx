import IconEdit from '@/assets/icons/IconEdit';
import IconTrashCan from '@/assets/icons/IconTrashCan';
import { TableProps } from '@/types/tableProps';

const Table = <T extends object>({
  title,
  description,
  columns,
  data,
  className = '',
}: TableProps<T>) => {
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
              <tr key={rowIndex} className='hover:bg-subContent/50'>
                {columns.map((column, colIndex) => (
                  <td
                    key={colIndex}
                    className={
                      column.className || 'px-4 py-3 text-sm font-preRegular'
                    }
                  >
                    {column.accessor === 'option_detail' ? (
                      <div>
                        {(
                          row[column.accessor as keyof T] as unknown as Array<{
                            option_detail_value: string;
                            additional_price: number;
                          }>
                        ).map((option, index) => (
                          <p key={index}>
                            {option.option_detail_value} +
                            {option.additional_price}
                          </p>
                        ))}
                      </div>
                    ) : column.accessor === 'image_url' ? (
                      <img
                        src={String(row[column.accessor as keyof T])}
                        alt='메뉴 이미지'
                        className='w-10 h-10 rounded-md object-cover'
                      />
                    ) : column.accessor === 'edit' ? (
                      <button className='p-1 hover:bg-gray-100 rounded-md'>
                        <IconEdit />
                      </button>
                    ) : column.accessor === 'delete' ? (
                      <button className='p-1 hover:bg-gray-100 rounded-md'>
                        <IconTrashCan fillColor='#D44848' />
                      </button>
                    ) : column.accessor === 'price' ? (
                      `₩${String(row[column.accessor as keyof T]).toLocaleString()}`
                    ) : (
                      String(row[column.accessor as keyof T])
                    )}
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
