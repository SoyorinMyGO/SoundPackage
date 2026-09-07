// Support both CommonJS (require) and ESM environments without using a
// static `import` statement (which can trigger "Cannot use import
// statement outside a module" when the loader runs the script as a
// non-module). We try to require first (CommonJS), and fall back to
// dynamic import() (works in module contexts).
(async () => {
  let contextBridge, ipcRenderer
  if (typeof require !== 'undefined') {
    ({ contextBridge, ipcRenderer } = require('electron'))
  } else {
    const electron = await import('electron')
    contextBridge = electron.contextBridge
    ipcRenderer = electron.ipcRenderer
  }

  try {
    contextBridge.exposeInMainWorld('electronAPI', {
      selectVoiceFile: (options) => ipcRenderer.invoke('select-voice-file', options),
      selectCompressedFile: (options) => ipcRenderer.invoke('select-compressed-file', options),
      selectDirectory: (options) => ipcRenderer.invoke('select-directory', options),
      minimize: () => ipcRenderer.send('window-minimize'),
      maximize: () => ipcRenderer.send('window-maximize'),
      close: () => ipcRenderer.send('window-close'),
    })
  } catch (e) {
    // ignore in non-Electron environment
  }

  try {
    console.log('[preload] loaded')
  } catch (e) {
    // ignore
  }
})()

