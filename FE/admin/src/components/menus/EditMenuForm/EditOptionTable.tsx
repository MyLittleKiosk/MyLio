import { OptionDetailType, OptionGroup } from '@/types/options';
import { useMenuEditContext } from '@/components/menus/EditMenuForm/MenuEditContext';

interface OptionTableProps {
  options: OptionGroup[];
}

const EditOptionTable = ({ options }: OptionTableProps) => {
  const {
    selectedOptions,
    handleOptionSelect,
    handleDetailSelect,
    handleRequiredSelect,
  } = useMenuEditContext();

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
        {options &&
          options.map((option) => {
            const selectedOption = selectedOptions.find(
              (selected) => selected.optionId === option.optionId
            );

            return option.optionDetails.map(
              (detail: OptionDetailType, index: number) => (
                <tr key={`${option.optionId}-${detail.optionDetailId}`}>
                  {index === 0 && (
                    <>
                      <td
                        rowSpan={option.optionDetails.length}
                        className='text-center'
                      >
                        <input
                          type='checkbox'
                          checked={selectedOption?.isSelected || false}
                          onChange={() => handleOptionSelect(option.optionId)}
                        />
                      </td>
                      <td
                        rowSpan={option.optionDetails.length}
                        className='px-4 py-3 text-sm font-preRegular text-center'
                      >
                        {option.optionNameKr}
                      </td>
                    </>
                  )}
                  <td className='px-4 py-3 text-sm font-preRegular flex gap-2 items-center justify-center'>
                    <span className='w-[50%]'>{detail.optionDetailValue}</span>
                    <input
                      type='checkbox'
                      checked={
                        selectedOption?.selectedDetails.includes(
                          detail.optionDetailId
                        ) || false
                      }
                      onChange={() =>
                        handleDetailSelect(
                          option.optionId,
                          detail.optionDetailId
                        )
                      }
                    />
                  </td>
                  {index === 0 && (
                    <td
                      rowSpan={option.optionDetails.length}
                      className='text-center'
                    >
                      <input
                        type='checkbox'
                        checked={selectedOption?.isRequired || false}
                        onChange={() => handleRequiredSelect(option.optionId)}
                      />
                    </td>
                  )}
                </tr>
              )
            );
          })}
      </tbody>
    </table>
  );
};

export default EditOptionTable;
