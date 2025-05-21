# app/services/session_cleanup_service.py
import threading
import time
import schedule
from datetime import datetime
from typing import Dict, Any, List

from app.services.redis_session_manager import RedisSessionManager

class SessionCleanupService:
    """세션 정리 서비스"""
    
    def __init__(self, session_manager: RedisSessionManager):
        """세션 정리 서비스 초기화"""
        self.session_manager = session_manager
        self.running = False
        self.scheduler_thread = None
        self.cleanup_stats = {
            "last_run": None,
            "total_cleaned": 0,
            "last_cleaned": 0,
            "error_count": 0,
        }
    
    def start_scheduler(self) -> bool:
        """세션 정리 스케줄러 시작"""
        if self.running:
            # print("[세션 정리] 스케줄러가 이미 실행 중입니다.")
            return False
        
        # 스케줄 설정
        # 1. 매시간 오래된 세션 정리 (1시간 이상 미사용)
        schedule.every().hour.do(self.cleanup_expired_sessions, max_idle_time_minutes=60)
        
        # 2. 매일 자정에 대규모 세션 정리 (6시간 이상 미사용)
        schedule.every().day.at("00:00").do(self.cleanup_expired_sessions, max_idle_time_minutes=360)
        
        # 3. 매일 새벽 1시에 큰 세션 정리 (100KB 초과)
        schedule.every().day.at("01:00").do(self.cleanup_large_sessions, max_size_kb=100)
        
        # 스케줄러 스레드 시작
        self.running = True
        self.scheduler_thread = threading.Thread(target=self._run_scheduler)
        self.scheduler_thread.daemon = True  # 메인 스레드 종료 시 함께 종료
        self.scheduler_thread.start()
        
        # print("[세션 정리] 스케줄러가 시작되었습니다.")
        return True
    
    def stop_scheduler(self) -> bool:
        """세션 정리 스케줄러 중지"""
        if not self.running:
            # print("[세션 정리] 스케줄러가 실행 중이 아닙니다.")
            return False
        
        self.running = False
        if self.scheduler_thread:
            self.scheduler_thread.join(timeout=1.0)
        
        # print("[세션 정리] 스케줄러가 중지되었습니다.")
        return True
    
    def _run_scheduler(self) -> None:
        """스케줄러 실행 스레드"""
        while self.running:
            schedule.run_pending()
            time.sleep(1)
    
    def cleanup_expired_sessions(self, max_idle_time_minutes: int = 60) -> int:
        """만료된 세션 정리 (스케줄러에서 호출)"""
        try:
            # print(f"[세션 정리] 만료된 세션 정리 시작 (최대 유휴 시간: {max_idle_time_minutes}분)")
            
            # 세션 정리 실행
            cleaned = self.session_manager.cleanup_expired_sessions(max_idle_time_minutes)
            
            # 통계 업데이트
            self.cleanup_stats["last_run"] = datetime.now().isoformat()
            self.cleanup_stats["total_cleaned"] += cleaned
            self.cleanup_stats["last_cleaned"] = cleaned
            
            # print(f"[세션 정리] 완료: {cleaned}개 세션 정리됨")
            return cleaned
        
        except Exception as e:
            # print(f"[세션 정리] 오류: {e}")
            self.cleanup_stats["error_count"] += 1
            return 0
    
    def cleanup_large_sessions(self, max_size_kb: int = 100) -> int:
        """큰 세션 정리 (스케줄러에서 호출)"""
        try:
            # print(f"[세션 정리] 큰 세션 정리 시작 (최대 크기: {max_size_kb}KB)")
            
            # 큰 세션 정리 실행
            cleaned = self.session_manager.cleanup_large_sessions(max_size_kb)
            
            # 통계 업데이트
            self.cleanup_stats["last_run"] = datetime.now().isoformat()
            self.cleanup_stats["total_cleaned"] += cleaned
            self.cleanup_stats["last_cleaned"] = cleaned
            
            # print(f"[세션 정리] 완료: {cleaned}개 큰 세션 정리됨")
            return cleaned
        
        except Exception as e:
            # print(f"[세션 정리] 오류: {e}")
            self.cleanup_stats["error_count"] += 1
            return 0
    
    def get_cleanup_stats(self) -> Dict[str, Any]:
        """세션 정리 통계 조회"""
        # 현재 세션 정보 추가
        session_info = self.session_manager.get_all_sessions_info()
        
        return {
            **self.cleanup_stats,
            "session_info": session_info,
            "scheduler_running": self.running
        }
    
    def manual_cleanup(self, idle_minutes: int = 30, size_kb: int = 50) -> Dict[str, int]:
        """수동 세션 정리"""
        expired_count = self.cleanup_expired_sessions(idle_minutes)
        large_count = self.cleanup_large_sessions(size_kb)
        
        return {
            "expired_sessions_cleaned": expired_count,
            "large_sessions_cleaned": large_count,
            "total_cleaned": expired_count + large_count
        }
    
    def delete_sessions(self, session_ids: List[str]) -> Dict[str, Any]:
        """세션 목록 명시적 삭제"""
        if not session_ids:
            return {"deleted": 0, "failed": 0}
        
        deleted = 0
        failed = 0
        
        for session_id in session_ids:
            if self.session_manager.delete_session(session_id):
                deleted += 1
            else:
                failed += 1
        
        return {
            "deleted": deleted,
            "failed": failed
        }

# app/routes/admin_routes.py (FastAPI 라우트에 추가)
from fastapi import APIRouter, Depends, HTTPException, status
from typing import List, Dict, Any

# 의존성 주입을 위한 함수
def get_session_cleanup_service():
    from app.dependencies import get_session_manager
    from app.services.session_cleanup_service import SessionCleanupService
    
    session_manager = get_session_manager()
    return SessionCleanupService(session_manager)

# 라우터 설정
router = APIRouter(
    prefix="/admin",
    tags=["admin"],
    responses={404: {"description": "Not found"}},
)

@router.post("/sessions/cleanup")
async def cleanup_sessions(
    idle_minutes: int = 30,
    size_kb: int = 50,
    cleanup_service: SessionCleanupService = Depends(get_session_cleanup_service)
):
    """세션 수동 정리"""
    result = cleanup_service.manual_cleanup(idle_minutes, size_kb)
    return result

@router.delete("/sessions")
async def delete_sessions(
    session_ids: List[str],
    cleanup_service: SessionCleanupService = Depends(get_session_cleanup_service)
):
    """세션 명시적 삭제"""
    result = cleanup_service.delete_sessions(session_ids)
    return result

@router.get("/sessions/stats")
async def get_session_stats(
    cleanup_service: SessionCleanupService = Depends(get_session_cleanup_service)
):
    """세션 정리 통계 조회"""
    return cleanup_service.get_cleanup_stats()

@router.post("/sessions/scheduler/start")
async def start_cleanup_scheduler(
    cleanup_service: SessionCleanupService = Depends(get_session_cleanup_service)
):
    """세션 정리 스케줄러 시작"""
    success = cleanup_service.start_scheduler()
    if not success:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Scheduler is already running"
        )
    return {"status": "started"}

@router.post("/sessions/scheduler/stop")
async def stop_cleanup_scheduler(
    cleanup_service: SessionCleanupService = Depends(get_session_cleanup_service)
):
    """세션 정리 스케줄러 중지"""
    success = cleanup_service.stop_scheduler()
    if not success:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Scheduler is not running"
        )
    return {"status": "stopped"}