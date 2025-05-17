import { ADMIN_NAVLIST, SUPERADMIN_NAVLIST } from '@/datas/sideBarList';
import { useGetRole } from '@/service/queries/user';
import { useUserStore } from '@/stores/useUserStore';
import { Response } from '@/types/apiResponse';
import { User } from '@/types/user';
import { AxiosError } from 'axios';
import { useEffect, useMemo, useState } from 'react';
import { useLocation, useNavigate } from 'react-router-dom';

// 실제 역할 타입으로 정의 (SUPER, STORE만 존재)
type UserRole = 'STORE' | 'SUPER';

// 역할별 기본 경로 정의
const defaultRoutesForRole: Record<UserRole, string> = {
  STORE: ADMIN_NAVLIST[0]?.link || '/', // STORE 역할의 첫 번째 메뉴 링크 또는 '/'
  SUPER: SUPERADMIN_NAVLIST[0]?.link || '/accounts', // SUPER 역할의 첫 번째 메뉴 링크 또는 '/accounts'
};

const generatePermissions = () => {
  const permissions: Record<UserRole, string[]> = {
    // STORE 역할은 ADMIN_NAVLIST 링크만 접근 가능
    STORE: ADMIN_NAVLIST.map((item) => item.link),
    // SUPER 역할은 SUPERADMIN_NAVLIST 링크만 접근 가능
    SUPER: SUPERADMIN_NAVLIST.map((item) => item.link),
  };
  return permissions;
};

export const useAuthGuard = () => {
  const {
    data: roleInfo,
    isLoading: isLoadingRole,
    isError,
    error,
  } = useGetRole() as {
    data?: Response<User>;
    isLoading: boolean;
    isError: boolean;
    error?:
      | AxiosError<{ message?: string; code?: string; error?: string }>
      | Error
      | null;
  }; // 역할 정보 조회
  const { user, setUser, logout: setUserLogout } = useUserStore(); // 사용자 정보 관리
  const navigate = useNavigate(); // 네비게이션 이동
  const location = useLocation(); // 현재 경로 조회

  const [isLoadingAuth, setIsLoadingAuth] = useState(true); // 인증 로딩 상태

  const routePermissions = useMemo(() => generatePermissions(), []); // 경로 권한 생성

  useEffect(() => {
    if (isLoadingRole) {
      setIsLoadingAuth(true);
      return;
    }

    // 역할 정보 조회 오류 또는 성공 여부 확인
    if (isError || !roleInfo?.success) {
      let errorMessage = '세션이 만료되었거나 인증에 실패했습니다.';
      if (isError && error) {
        if (error instanceof AxiosError && error.response?.data) {
          errorMessage =
            error.response.data.message ||
            error.response.data.error ||
            (error as Error).message;
        } else if (error instanceof Error) {
          errorMessage = error.message;
        }
        console.error('Authentication error:', errorMessage, error);
      } else if (!roleInfo?.success) {
        console.error('Role fetch not successful:', roleInfo);
      }
      setUserLogout();
      setIsLoadingAuth(true);
      navigate('/login', { replace: true });
      return;
    }

    // 역할 정보가 조회되었으면 사용자 정보 업데이트
    if (roleInfo.data) {
      if (
        !user ||
        user.userId !== roleInfo.data.userId ||
        user.role !== roleInfo.data.role
      ) {
        setUser(roleInfo.data);
      }

      const userRoleFromAPI = roleInfo.data.role as UserRole; // 역할 정보 추출
      const currentPath = location.pathname; // 현재 경로 추출

      // 로그인 페이지 접근 시 역할별 기본 페이지로 리디렉션
      if (currentPath === '/login') {
        setIsLoadingAuth(true);
        navigate(defaultRoutesForRole[userRoleFromAPI] || '/', {
          replace: true,
        });
        return;
      }

      const allowedRoutes = routePermissions[userRoleFromAPI]; // 허용된 경로 추출

      // 허용된 경로 존재 여부 확인
      if (allowedRoutes) {
        const isPathAllowed = allowedRoutes.some((allowedPath) => {
          if (allowedPath === '/') {
            return currentPath === '/' || currentPath.startsWith('/#/');
          }
          return currentPath.startsWith(allowedPath);
        });

        // 허용된 경로가 없으면 역할별 기본 페이지로 리디렉션
        if (!isPathAllowed) {
          console.warn(
            `현재 역할(${userRoleFromAPI})은 '${currentPath}' 경로에 접근할 수 없습니다. 역할의 기본 페이지로 이동합니다.`
          );
          setIsLoadingAuth(true);
          navigate(defaultRoutesForRole[userRoleFromAPI] || '/', {
            replace: true,
          });
          return;
        }
      } else {
        // 경로 권한 설정 오류 처리
        console.error(
          `'${userRoleFromAPI}' 역할에 대한 경로 권한이 설정되지 않았습니다. 시스템 관리자에게 문의하세요.`
        );
        setUserLogout();
        setIsLoadingAuth(true);
        navigate('/login', { replace: true });
        return;
      }
    } else {
      // 사용자 정보 조회 실패 시 로그인 페이지로 리디렉션
      console.error(
        '사용자 정보를 가져오는데 실패했습니다. 다시 로그인해주세요.'
      );
      setUserLogout();
      setIsLoadingAuth(true);
      navigate('/login', { replace: true });
      return;
    }

    setIsLoadingAuth(false);
  }, [
    isLoadingRole,
    isError,
    error,
    roleInfo,
    navigate,
    setUser,
    setUserLogout,
    location.pathname,
    routePermissions,
    user,
  ]);

  const redirectToDashboard = () => {
    if (user) {
      navigate(defaultRoutesForRole[user.role as UserRole] || '/', {
        replace: true,
      });
    }
  };

  return { isLoadingAuth, user, redirectToDashboard };
};
