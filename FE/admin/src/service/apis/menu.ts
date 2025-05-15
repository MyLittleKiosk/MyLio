import { CustomError } from '@/types/apiResponse';
import authClient from '@/service/authClient';
import { MenuAdd } from '@/types/menus';

export async function getMenus(page?: number, categoryId?: number) {
  const params = {
    page: page || 1,
    categoryId: categoryId || 0,
  };
  try {
    const res = await authClient.get('/menu', {
      params,
    });
    return res.data;
  } catch (error: unknown) {
    if (error instanceof Error) {
      const customError = error as CustomError;
      const errorMessage =
        customError.response?.data?.error?.message || error.message;
      throw new Error(errorMessage);
    }
    throw new Error('unknown error');
  }
}

export async function getMenuById(menuId: number) {
  try {
    const res = await authClient.get(`/menu/${menuId}`);
    return res.data;
  } catch (error: unknown) {
    if (error instanceof Error) {
      const customError = error as CustomError;
      const errorMessage =
        customError.response?.data?.error?.message || error.message;
      throw new Error(errorMessage);
    }
    throw new Error('unknown error');
  }
}

export async function addMenu(menu: MenuAdd, file?: File) {
  try {
    const res = await authClient.post('/menu', {
      file: file,
      menuData: menu,
    });
    return res.data;
  } catch (error: unknown) {
    if (error instanceof Error) {
      const customError = error as CustomError;
      const errorMessage =
        customError.response?.data?.error?.message || error.message;
      throw new Error(errorMessage);
    }
    throw new Error('unknown error');
  }
}

export async function updateMenu(menuId: number, menu: MenuAdd, file?: File) {
  try {
    const res = await authClient.put(`/menu/${menuId}`, {
      file: file,
      menuData: menu,
    });
    return res.data;
  } catch (error: unknown) {
    if (error instanceof Error) {
      const customError = error as CustomError;
      const errorMessage =
        customError.response?.data?.error?.message || error.message;
      throw new Error(errorMessage);
    }
    throw new Error('unknown error');
  }
}
