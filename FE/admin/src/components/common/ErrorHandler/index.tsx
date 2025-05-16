import React, { Suspense } from 'react';
import { ErrorBoundary } from 'react-error-boundary';

import Error from '@/components/common/Error';
import Loading from '@/components/common/Loading';

const ErrorHandler = ({ children }: { children: React.ReactNode }) => {
  return (
    <ErrorBoundary fallback={<Error />}>
      <Suspense fallback={<Loading />}>{children}</Suspense>
    </ErrorBoundary>
  );
};

export default ErrorHandler;
