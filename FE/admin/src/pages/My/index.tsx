import ErrorHandler from '@/components/common/ErrorHandler';
import MyContent from '@/components/my/MyContent';

const My = () => {
  return (
    <ErrorHandler>
      <MyContent />
    </ErrorHandler>
  );
};

export default My;
