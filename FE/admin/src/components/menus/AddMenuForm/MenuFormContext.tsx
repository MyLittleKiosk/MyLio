import React, { createContext, useContext } from 'react';
import { useMenuAdd } from '@/components/menus/AddMenuForm/useMenuAdd';

const MenuFormContext = createContext<ReturnType<typeof useMenuAdd> | null>(
  null
);

export const MenuFormProvider: React.FC<{ children: React.ReactNode }> = ({
  children,
}) => {
  const menuFormValues = useMenuAdd();

  return (
    <MenuFormContext.Provider value={menuFormValues}>
      {children}
    </MenuFormContext.Provider>
  );
};

export const useMenuFormContext = () => {
  const context = useContext(MenuFormContext);
  if (!context) {
    throw new Error(
      'useMenuFormContext must be used within a MenuFormProvider'
    );
  }
  return context;
};
