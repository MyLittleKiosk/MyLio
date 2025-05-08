import authClient from '../authClient';

async function getMenus() {
  try {
    const response = await authClient.get('/menus');
    return response.data;
  } catch (error: unknown) {
    if (error instanceof Error) {
      throw error.message;
    }
    throw new Error('Unknown error');
  }
}

export default getMenus;
