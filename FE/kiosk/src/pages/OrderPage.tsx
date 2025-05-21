import React, { useEffect, useState } from 'react';

const OrderPage: React.FC = () => {
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    const timer = setTimeout(() => {
      setIsLoading(false);
    }, 2000);

    return () => {
      clearTimeout(timer);
    };
  }, []);

  return <div>{/* Render your component content here */}</div>;
};

export default OrderPage;
