import { useState } from 'react';

function useBooleanState(initialValue: boolean) {
  const [value, setValue] = useState(initialValue);

  return [value, setValue];
}

export default useBooleanState;
