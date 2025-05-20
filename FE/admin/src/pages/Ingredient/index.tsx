import IngredientContent from '@/components/ingredient/IngredientContent';
import ErrorHandler from '@/components/common/ErrorHandler';

const Ingredient = () => {
  return (
    <ErrorHandler>
      <IngredientContent />
    </ErrorHandler>
  );
};

export default Ingredient;
