"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
// 예시: Renderer와 Main 간의 안전한 통신을 위한 preload
const electron_1 = require("electron");
electron_1.contextBridge.exposeInMainWorld('api', {
// 여기에 필요한 함수나 값을 추가할 수 있습니다.
});
