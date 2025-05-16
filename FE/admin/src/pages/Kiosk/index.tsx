import { Suspense } from 'react';
import { ErrorBoundary } from 'react-error-boundary';

import Error from '@/components/common/Error';
import Loading from '@/components/common/Loading';
import KioskContent from '@/components/kiosks/KioskContent';

const Kiosk = () => {
  return (
    <ErrorBoundary fallbackRender={() => <Error />}>
      <Suspense fallback={<Loading />}>
        <KioskContent />
      </Suspense>
    </ErrorBoundary>
  );
};

export default Kiosk;
