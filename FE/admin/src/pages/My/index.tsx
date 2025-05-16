import { Suspense } from 'react';
import { ErrorBoundary } from 'react-error-boundary';

import Error from '@/components/common/Error';
import Loading from '@/components/common/Loading';
import MyContent from '@/components/my/MyContent';

const My = () => {
  return (
    <ErrorBoundary fallbackRender={() => <Error />}>
      <Suspense fallback={<Loading />}>
        <MyContent />
      </Suspense>
    </ErrorBoundary>
  );
};

export default My;
