import { ipcMain, dialog } from 'electron';

export async function registerIpcHandlers() {
    // 选择音频文件
    ipcMain.handle('select-voice-file', async (event, options) => {
        const result = await dialog.showOpenDialog({
            title: options?.title || '选择文件',
            properties: ["openFile", "multiSelections"],
            filters: options?.filters || [
                { name: '音频文件', extensions: ["wav", "mp3", "flac", "m4a", "ogg", "webm"] },
                { name: '所有文件', extensions: ["*"] },
            ]
        });

        if(result.canceled) { return null; }    // 如果取消选择
        return result.filePaths;
    })

    // 选择压缩文件
    ipcMain.handle('select-compressed-file', async (event, options) => {
        const result = await dialog.showOpenDialog({
            title: options?.title || '选择文件',
            properties: ["openFile", "multiSelections"],
            filters: options?.filters || [
                { name: '压缩文件', extensions: ["zip", "rar", "7z", "tar", "gz"] },
                { name: '所有文件', extensions: ["*"] },
            ]
        });

        if(result.canceled) { return null; }    // 如果取消选择
        return result.filePaths;
    })

    // 选择文件夹
    ipcMain.handle('select-directory', async (event, options) => {
        const result = await dialog.showOpenDialog({
            title: options?.title || '选择文件夹',
            properties: ['openDirectory']
        });

        if (result.canceled) {
            return null;
        }   // 如果取消选择
        return result.filePaths[0];
    })
}