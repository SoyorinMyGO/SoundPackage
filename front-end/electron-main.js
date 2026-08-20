import { app, BrowserWindow, ipcMain } from 'electron'
import { fileURLToPath } from 'url'
import { dirname, join } from 'path'

// 获取当前文件所在目录
const __filename = fileURLToPath(import.meta.url)
const __dirname = dirname(__filename)

let win = null  // 保留窗口实例

// 创建窗口函数
function createWindow() {
  // 将窗口实例赋值给外层的 `win` 变量（避免遮蔽/作用域问题）
  win = new BrowserWindow({
    width: 960,
    height: 600,
    frame: false, // 去除原生窗口框架（标题栏 / 边框）
    transparent: true,
    backgroundColor: '#00000000',
    titleBarStyle: 'hidden',  // 隐藏标题栏（主要用于 macOS）
    webPreferences: {
      nodeIntegration: false,
      contextIsolation: true,
      preload: join(__dirname, 'preload.js'),
    }
  })

  // 加载Vite开发服务器地址（开发环境）
  win.loadURL('http://localhost:52798')

  // 打开开发者工具（方便调试）
  win.webContents.openDevTools()

  // 当窗口被关闭时，清理外层引用
  win.on('closed', () => {
    win = null
  })

  // 监听键盘事件，按 F12 切换 DevTools（一些平台下 F12 默认未绑定）
  win.webContents.on('before-input-event', (event, input) => {
    // input.key 在 Windows 上为 'F12'
    if (input.key === 'F12') {
      win.webContents.toggleDevTools()
      event.preventDefault()
    }
  })
}

// 当 Electron 完成初始化时创建窗口
app.whenReady().then(() => {
  createWindow()
})

// 所有窗口关闭时退出应用（macOS 除外）
app.on('window-all-closed', () => {
  if (process.platform !== 'darwin') {
    app.quit()
  }
})

// 最小化
ipcMain.on('window-minimize', () => {
  console.log('[main] received window-minimize')
  if (win) {
    win.minimize()
  } else {
    console.warn('[main] window is null when trying to minimize')
  }
})

// 最小化
ipcMain.on('window-maximize', () => {
  console.log('[main] received window-maximize')
  if (win) {
    if (win.isMaximized()) {
      win.unmaximize()
    } else {
      win.maximize()
    }
  } else {
    console.warn('[main] window is null when trying to maximize/unmaximize')
  }
})

// 关闭
ipcMain.on("window-close", () => {
  console.log('[main] received window-close')
  if (win) {
    win.close()
  } else {
    console.warn('[main] window is null when trying to close')
  }
})
