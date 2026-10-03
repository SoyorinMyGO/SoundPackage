import {PackageItem} from "../../model/Package";
import {getLocalStorage, setLocalStorage} from "../LocalStorage/local_storage";

/**
 * 添加新的语音包
 * @param newPackage - 新的语音包名称
 * @returns 更新后的语音包信息
 */
export function add_new_package(newPackage: string): void {
    let packageInfo: PackageItem[] = getLocalStorage('package_info') || [];
    let nextId: number = getLocalStorage('next_package_id') || 1;
    const newItem: PackageItem = {
        id: nextId,
        name: newPackage,
        alias: null,
        isTop: false,
        voice_list: [],
        created_at: new Date().toISOString(),
        updated_at: new Date().toISOString(),
    }
    packageInfo.push(newItem);
    setLocalStorage('next_package_id', ++nextId);
    setLocalStorage('package_info', packageInfo);
}