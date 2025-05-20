import ErrorHandler from '@/components/common/ErrorHandler';
import StatisticsContent from '@/components/statistics/StatisticsContent';

const Statistics = () => {
  return (
    <ErrorHandler>
      <StatisticsContent />
    </ErrorHandler>
  );
};

export default Statistics;
