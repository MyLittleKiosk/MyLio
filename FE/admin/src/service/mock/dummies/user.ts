import { User, Role } from '@/types/user';
import { Response } from '@/types/apiResponse';
const userRole: Response<User> = {
  success: true,
  data: {
    userId: 1,
    role: Role.SUPER,
  },
  error: null,
  timestamp: new Date().toISOString(),
};

export { userRole };
