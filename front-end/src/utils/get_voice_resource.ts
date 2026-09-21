import {computed} from "vue";
import {Voice} from "../model/Voice";
import { assetBaseUrl } from "../config/axios_config.js";

export function getShowedName(fileName: string, alias: string): string {
    // 去后缀文件名
    const nameWithoutSuffix = computed(() => {
      if (!fileName) {
        return '';
      }
      return fileName.split('.')[0];
    })
    // 存在别名的情况下显示别名
    if (!alias) {
        return nameWithoutSuffix.value;
    }
    return alias;
}

// 获取文件路径
export function getPosition(resource: Voice): string {
  if (!resource) { return '' }

  const fileName: string = resource.name || '';
  if (!fileName) { return '' }

  try {
    const hashContent = resource.hash_content || fileName.replace(/\.[^/.]+$/, '');
    if (!hashContent) { return '' }

    const ext = fileName.includes('.')
      ? `.${String(fileName.split('.').pop() || '').toLowerCase()}`
      : '';
    const actualFileName = `${hashContent}${ext}`;
    console.log('DEBUG(audio):actualFileName', actualFileName);

    return encodeURI(`${assetBaseUrl}/assets/voices/${actualFileName}`);
  } catch (e) {
    console.error('音频路径生成失败', e);
    return '';
  }
}