import ErrorHandler from '@/components/common/ErrorHandler';
import KioskContent from '@/components/kiosks/KioskContent';

const Kiosk = () => {
  return (
    <ErrorHandler>
      <KioskContent />
    </ErrorHandler>
  );
};

export default Kiosk;
