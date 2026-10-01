import {PackageItem} from "../../model/Package";
import {Voice} from "../../model/Voice";

/**
 * 从单个语音包中移除部分语音
 * @param voiceList - 需要移除的语音列表
 * @param dir - 语音包目录
 * @param packageInfo - 所有语音包信息
 * @returns 更新后的语音包信息
 */
export function rm_voices_from_dir(voiceList: number[], dir: string, packageInfo: PackageItem[]): PackageItem[] | null {
    return packageInfo.map((pkg: PackageItem) => {
        if (pkg.name === dir) {
          const updatedVoices = pkg.voice_list?.filter(id => !voiceList.includes(id));
          return { ...pkg, voice_list: updatedVoices };
        }
        return pkg;
    });
}

/**
 * 从所有语音包中移除部分语音
 * @param voiceList - 需要移除的语音列表
 * @param packageInfo - 所有语音包信息
 * @returns 更新后的语音包信息
 */
export function rm_voices_from_all_dirs(voiceList: number[], packageInfo: PackageItem[]): PackageItem[] | null {
    return packageInfo.map((pkg: PackageItem) => {
        const updatedVoices = pkg.voice_list?.filter(id => !voiceList.includes(id));
        return {...pkg, voice_list: updatedVoices};
    });
}

/**
 * 从语音列表中删除
 * @param voiceList - 需要移除的语音列表
 * @param voiceInfo - 语音信息字典
 * @returns 更新后的语音信息字典
 */
export function rm_voices_from_voice_list(voiceList: number[], voiceInfo: Record<string, Voice>): Record<number, Voice> | null{
    return Object.fromEntries(
        Object.entries(voiceInfo).filter(([, v]) => !voiceList.includes(v.id))
    );
}