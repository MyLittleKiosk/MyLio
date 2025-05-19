import ErrorHandler from '@/components/common/ErrorHandler';
import AccountContent from '@/components/account/AccountContent';

const Accounts = () => {
  return (
    <ErrorHandler>
      <AccountContent />
    </ErrorHandler>
  );
};

export default Accounts;
