import ErrorHandler from '@/components/common/ErrorHandler';
import NutrientsContent from '@/components/nutrients/NutrientsContent';

const Nutrients = () => {
  return (
    <ErrorHandler>
      <NutrientsContent />
    </ErrorHandler>
  );
};

export default Nutrients;
