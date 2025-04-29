import { useEffect } from 'react';

const MSWInit = () => {
  useEffect(() => {
    async function enableMocking() {
      if (
        typeof window !== 'undefined' &&
        process.env.NODE_ENV === 'development'
      ) {
        const { worker } = await import('@/service/mock/worker');
        await worker.start();
      }
    }

    enableMocking();
  }, []);
  return <></>;
};

export default MSWInit;
