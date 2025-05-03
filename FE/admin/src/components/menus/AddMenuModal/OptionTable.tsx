import { OptionDetail } from '@/types/options';

interface OptionTableProps {
  options: OptionDetail[];
  onOptionSelect: (optionId: number) => void;
  onDetailSelect: (optionId: number, detailId: number) => void;
  onRequiredSelect: (optionId: number) => void;
  selectedOptions: {
    optionId: number;
    isSelected: boolean;
    isRequired: boolean;
    selectedDetails: number[];
  }[];
}

const OptionTable = ({
  options,
  onOptionSelect,
  onDetailSelect,
  onRequiredSelect,
  selectedOptions,
}: OptionTableProps) => {
  return (
    <table className='w-full border-collapse'>
      <thead className='border-b border-subContent'>
        <tr>
          <th className='px-4 py-3 text-sm font-preLight text-content text-center'>
            추가 여부
          </th>
          <th className='px-4 py-3 text-sm font-preLight text-content text-center'>
            이름
          </th>
          <th className='px-4 py-3 text-sm font-preLight text-content text-center'>
            세부 옵션
          </th>
          <th className='px-4 py-3 text-sm font-preLight text-content text-center'>
            필수 여부
          </th>
        </tr>
      </thead>
      <tbody className='divide-y divide-subContent'>
        {options.map((option) => {
          const selectedOption = selectedOptions.find(
            (selected) => selected.optionId === option.option_id
          );

          return option.option_detail.map((detail, index) => (
            <tr key={`${option.option_id}-${detail.option_detail_id}`}>
              {index === 0 && (
                <>
                  <td
                    rowSpan={option.option_detail.length}
                    className='text-center'
                  >
                    <input
                      type='checkbox'
                      checked={selectedOption?.isSelected || false}
                      onChange={() => onOptionSelect(option.option_id)}
                    />
                  </td>
                  <td
                    rowSpan={option.option_detail.length}
                    className='px-4 py-3 text-sm font-preRegular text-center'
                  >
                    {option.option_name_kr}
                  </td>
                </>
              )}
              <td className='px-4 py-3 text-sm font-preRegular flex gap-2 items-center justify-center'>
                <span className='w-[50%]'>{detail.option_detail_value}</span>
                <input
                  type='checkbox'
                  checked={
                    selectedOption?.selectedDetails.includes(
                      detail.option_detail_id
                    ) || false
                  }
                  onChange={() =>
                    onDetailSelect(option.option_id, detail.option_detail_id)
                  }
                />
              </td>
              {index === 0 && (
                <td
                  rowSpan={option.option_detail.length}
                  className='text-center'
                >
                  <input
                    type='checkbox'
                    checked={selectedOption?.isRequired || false}
                    onChange={() => onRequiredSelect(option.option_id)}
                  />
                </td>
              )}
            </tr>
          ));
        })}
      </tbody>
    </table>
  );
};

export default OptionTable;
