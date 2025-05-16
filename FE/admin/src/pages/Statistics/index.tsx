import { Suspense } from 'react';
import { ErrorBoundary } from 'react-error-boundary';

import Error from '@/components/common/Error';
import Loading from '@/components/common/Loading';
import StatisticsContent from '@/components/statistics/StatisticsContent';

const Statistics = () => {
  return (
    <ErrorBoundary fallbackRender={() => <Error />}>
      <Suspense fallback={<Loading />}>
        <StatisticsContent />
      </Suspense>
    </ErrorBoundary>
  );
};

export default Statistics;
