import { User, Role } from '@/types/user';
import { Response } from '@/types/apiResponse';
const userRole: Response<User> = {
  success: true,
  data: {
    userId: 1,
    role: Role.SUPER,
  },
  timestamp: new Date().toISOString(),
};

export { userRole };
