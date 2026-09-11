import {getLocalStorage} from "../LocalStorage/local_storage";
import { Voice } from "../../model/Voice"
import { PackageItem } from "../../model/Package"

interface Tag {
  id: number;
  path: string;
}

interface VoiceBelongTag {
  voice_id: number;
  tag_id: number;
}

/**
 * 获取语音列表（前端筛选版本）
 * @param voices - 所有语音数据
 * @param voiceTags - 语音与标签的关联数据
 * @param allTags - 所有标签数据
 * @param packageId - 选择的语音包id，0表示所有语音包
 * @param selectedTagIds - 选择的筛选标签id列表
 * @returns 筛选后的语音列表
 */
export function getVoiceListOptimized(
  voices: Voice[],
  voiceTags: VoiceBelongTag[],
  allTags: Tag[],
  packageId: number,
  selectedTagIds: number[] | null
): Voice[] {
  // 构建索引Map
  const voiceMap = new Map<number, Voice>();
  voices.forEach(v => voiceMap.set(v.id, v));

  // 构建标签Map
  const tagMap = new Map<number, Tag>();
  allTags.forEach(t => tagMap.set(t.id, t));

  // 构建语音-标签关系索引
  const voiceToTags = new Map<number, Set<number>>();
  voiceTags.forEach(vt => {
    // 若voiceToTags中还没有当前语音
    if (!voiceToTags.has(vt.voice_id)) {
      voiceToTags.set(vt.voice_id, new Set());
    }
    voiceToTags.get(vt.voice_id)!.add(vt.tag_id);
  });

  // 筛选package
  let filteredVoiceIds: Set<number>;
  if (packageId === 0) {
    filteredVoiceIds = new Set(voiceMap.keys());
  } else {
    filteredVoiceIds = getVoiceIdsByPackageId(packageId);
  }
  console.log('DEBUG(get_voice_bt_package):', filteredVoiceIds);

  if (!selectedTagIds || selectedTagIds.length === 0) {
    return sortVoices(
        voices.filter(v => filteredVoiceIds.has(v.id)),
        'updated_at'
    );
  }

  // 获取选中标签及其所有子标签
  const matchedTagIds = new Set<number>();
  const selectedTags = selectedTagIds
    .map(id => tagMap.get(id))
    .filter((t): t is Tag => t !== undefined);

  for (const tag of allTags) {
    for (const selectedTag of selectedTags) {
      if (selectedTag.path) {
        if (tag.path.startsWith(selectedTag.path)) {
          matchedTagIds.add(tag.id);
          break;
        }
      } else if (tag.id === selectedTag.id) {
        matchedTagIds.add(tag.id);
        break;
      }
    }
  }

  // 筛选符合条件的语音
  const result: Voice[] = [];
  for (const voiceId of filteredVoiceIds) {
    const voiceTagsSet = voiceToTags.get(voiceId);
    if (voiceTagsSet) {
      for (const tagId of voiceTagsSet) {
        if (matchedTagIds.has(tagId)) {
          const voice = voiceMap.get(voiceId);
          if (voice) {
            result.push(voice);
            break;
          }
        }
      }
    }
  }

  return sortVoices(result, 'created_at');
}


function getVoiceIdsByPackageId(packageId: number): Set<number> {
  // 获取语音包信息
  const packageInfo = getLocalStorage('package_info') as PackageItem[];
  // 根据语音包id筛选
  const targetPackage: PackageItem | undefined = packageInfo.find(item => item.id === packageId);
  if(!targetPackage) {
    return new Set();
  }
  return new Set(targetPackage.voice_list);
}

function sortVoices(voices: Voice[], dateField: 'updated_at' | 'created_at'): Voice[] {
  return voices.sort((a, b) => {
    if (b.used_times !== a.used_times) {
      return b.used_times - a.used_times;
    }
    return new Date(b[dateField]).getTime() - new Date(a[dateField]).getTime();
  });
}