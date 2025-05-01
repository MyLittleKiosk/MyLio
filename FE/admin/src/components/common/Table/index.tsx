import { TableProps } from '@/types/tableProps';

const Table = <T extends object>({
  columns,
  data,
  className = '',
}: TableProps<T>) => {
  return (
    <div className='overflow-x-auto'>
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
        <tbody className='divide-y divide-gray-200'>
          {data.map((row, rowIndex) => (
            <tr key={rowIndex} className='hover:bg-gray-50'>
              {columns.map((column, colIndex) => (
                <td
                  key={colIndex}
                  className={
                    column.className || 'px-4 py-3 text-sm font-preRegular'
                  }
                >
                  {typeof column.accessor === 'function'
                    ? column.accessor(row)
                    : column.accessor === 'price'
                      ? `₩${String(row[column.accessor as keyof T]).toLocaleString()}`
                      : String(row[column.accessor as keyof T])}
                </td>
              ))}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default Table;
