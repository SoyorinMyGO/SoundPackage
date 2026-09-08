export const StorageKeys = {
    USER_INFO: 'app_user',          // 用户信息
    THEME: 'app_theme',             // 主题
    VOICEALIAS: 'voice_alias',      // 语音别名
    PACKAGEALIAS: 'package_alias',  // 语音包别名
} as const

export function setLocalStorage<T>(key: string, value: T | null = null): void {
/*
* 设置缓存信息
* params:
*   key(string): 缓存的键
*   value(any): 缓存的值
* */
    try {
        localStorage.setItem(key, JSON.stringify(value));
    } catch (e) {
        console.warn(`写入${key}失败`, e);
    }
}

export function getLocalStorage<T>(key: string): T | null {
/*
* 获取缓存信息
* params:
*   key(string): 缓存的键
* return:
*   value(any): 缓存的值
* */
    try {
        const item = localStorage.getItem(key);
        if(!item) return null;
        return JSON.parse(item) as T;
    } catch (e) {
        console.warn(`读取${key}失败`, e);
        return null;
    }
}

export function removeLocalStorage(key: string): void {
/*
* 删除缓存信息
* params:
*   key(string): 缓存的键
* */
    localStorage.removeItem(key);
}