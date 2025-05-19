const { app, BrowserWindow, globalShortcut } = require('electron');

function createWindow() {
  const win = new BrowserWindow({
    width: 1080,
    height: 1920,
    icon: 'mylio-favi.ico',
    webPreferences: {
      nodeIntegration: true,
      contextIsolation: false,
    },
  });

  win.loadURL('https://k12b102.p.ssafy.io/kiosk/');
  win.setFullScreen(true);
  win.webContents.openDevTools();

  // Alt+Enter로 전체화면 토글
  globalShortcut.register('Alt+Enter', () => {
    win.setFullScreen(!win.isFullScreen());
  });
}

app.whenReady().then(createWindow);

app.on('window-all-closed', () => {
  if (process.platform !== 'darwin') {
    app.quit();
  }
});

app.on('activate', () => {
  if (BrowserWindow.getAllWindows().length === 0) {
    createWindow();
  }
});

app.on('will-quit', () => {
  // 모든 단축키 해제
  globalShortcut.unregisterAll();
}); 