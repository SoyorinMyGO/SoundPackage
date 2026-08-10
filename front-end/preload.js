// Support both CommonJS (require) and ESM environments without using a
// static `import` statement (which can trigger "Cannot use import
// statement outside a module" when the loader runs the script as a
// non-module). We try to require first (CommonJS), and fall back to
// dynamic import() (works in module contexts).
(async () => {
  let contextBridge, ipcRenderer
  if (typeof require !== 'undefined') {
    // CommonJS environment
    ({ contextBridge, ipcRenderer } = require('electron'))
  } else {
    // ESM environment — use dynamic import to avoid parse-time errors
    const electron = await import('electron')
    contextBridge = electron.contextBridge
    ipcRenderer = electron.ipcRenderer
  }

  // 暴露安全的API给渲染进程
  try {
    contextBridge.exposeInMainWorld('electronAPI', {
      minimize: () => ipcRenderer.send('window-minimize'),
      maximize: () => ipcRenderer.send('window-maximize'),
      close: () => ipcRenderer.send('window-close'),
    })
  } catch (e) {
    // 如果 contextBridge 不可用（极少见），在渲染器中不注入也不抛错
    // 例如在浏览器环境或构建工具的沙箱里运行时会触发
    // 这让开发时能在浏览器打开页面而不会中断脚本执行
    // console.warn('[preload] could not expose electronAPI', e)
  }

  // 调试用：确认 preload 脚本已加载（在 Electron 的渲染器 DevTools 中可见）
  try {
    console.log('[preload] loaded')
  } catch (e) {
    // 忽略在非 Electron 环境下的错误
  }
})()

