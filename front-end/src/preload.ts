import { contextBridge, ipcRenderer } from 'electron';

contextBridge.exposeInMainWorld('electronAPI', {
  selectVoiceFile: (options?: any) => ipcRenderer.invoke('select-voice-file', options),
  selectCompressedFile: (options?: any) => ipcRenderer.invoke('select-compressed-file', options),
  selectDirectory: (options?: any) => ipcRenderer.invoke('select-directory', options),
  minimize: () => ipcRenderer.send('window-minimize'),
  maximize: () => ipcRenderer.send('window-maximize'),
  close: () => ipcRenderer.send('window-close'),
});
