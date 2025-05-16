import { Suspense } from 'react';
import { ErrorBoundary } from 'react-error-boundary';

import Error from '@/components/common/Error';
import Loading from '@/components/common/Loading';
import NutrientsContent from '@/components/nutrients/NutrientsContent';

const Nutrients = () => {
  return (
    <ErrorBoundary fallbackRender={() => <Error />}>
      <Suspense fallback={<Loading />}>
        <NutrientsContent />
      </Suspense>
    </ErrorBoundary>
  );
};

export default Nutrients;
