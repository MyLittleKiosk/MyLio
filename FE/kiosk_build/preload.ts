// 예시: Renderer와 Main 간의 안전한 통신을 위한 preload
import { contextBridge } from 'electron';

contextBridge.exposeInMainWorld('api', {
  // 여기에 필요한 함수나 값을 추가할 수 있습니다.
}); 