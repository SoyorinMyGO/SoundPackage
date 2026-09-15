<template>
<div class="head glass-background">
  <!--左侧按钮组-->
  <div class="left-button-group">
    <button @click="emit('toggle')">
      <i class="icon icon-unfold" v-if="isCollapsed"></i>
      <i class="icon icon-fold" v-if="!isCollapsed"></i>
    </button>
    <button @click="toggleTheme">
      <i class="icon icon-moon" v-if="currentTheme === 'dark'"></i>
      <i class="icon icon-sun" v-if="currentTheme === 'light'"></i>
    </button>
  </div>
  <!--搜索栏-->
  <div class="search-group">
    <search-input
        ref="searchInputRef"
        :isSimple=true
        :model-value="formData"
        @update:modelValue="handleInput"
        @blur="handleBlur"
        class="search">
    </search-input>
  </div>
  <!--右侧按钮组-->
  <div class="right-button-group">
    <el-dropdown class="import-dropdown" placement="bottom" trigger="click">
      <el-button>
        <i class="icon-import"></i>
      </el-button>
      <template #dropdown>
        <el-dropdown-menu>
          <el-dropdown-item @click="importVoiceFileHandle">导入语音</el-dropdown-item>
          <el-dropdown-item @click="importPackageHandle">导入语音包</el-dropdown-item>
        </el-dropdown-menu>
      </template>
    </el-dropdown>
    <button @click="exportPackageHandle" title="导出语音包">
      <i class="icon-export"></i>
    </button>
    <button>
      <i class="icon-file-manager"></i>
    </button>
  </div>
</div>
</template>

<script setup lang="ts">
import SearchInput from "../components/SearchInput.vue";
import { computed, onMounted, onUnmounted, Ref, ref, UnwrapRef } from "vue";
import { localApi } from "../config/axios_config"
import { userThemeStore } from "../store/theme.js";
import { getLocalStorage, setLocalStorage } from "../utils/LocalStorage/local_storage";
import { Voice } from "../model/Voice";
import { PackageItem } from "../model/Package";
import { useLocalStorage } from "../utils/LocalStorage/use_storage";

const props = defineProps({
  isCollapsed: Boolean,
  packageChoose: Object,
})

const emit = defineEmits(["toggle", "submit"]);
const themeStore = userThemeStore();

declare global {
  interface Window {
    electronAPI: {
      selectVoiceFile: (options?: any) => Promise<string[] | null>;
      selectCompressedFile: (options?: any) => Promise<string[] | null>;
      selectDirectory: (options?: { title?: string }) => Promise<string | null>;
    };
  }
}

// 主题类型
const currentTheme = computed(() => themeStore.currentTheme);
// 搜索栏关键字
const formData: Ref<UnwrapRef<string>, UnwrapRef<string> | string> = ref('');
const search = computed(() => formData.value.trim());
// 获取搜索栏的引用
const searchInputRef = ref<typeof SearchInput | null>(null);

function handleInput(value: string) {
  formData.value = value;
}

function handleBlur() {
  emit('submit', search.value);
}

const handleKeyDown = (e: KeyboardEvent) => {
  if ((e.ctrlKey || e.metaKey) && e.key === 'k') {
    console.log('DEBUG(keyboardWatch):按下了Ctrl+K');
    e.preventDefault(); // 阻止浏览器默认行为
    if (searchInputRef.value) {
      searchInputRef.value.focus?.();
      searchInputRef.value.select?.();
    }
  }
  if (e.key === 'Escape' || e.key === 'Enter') {
    console.log("DEBUG(keyboardWatch): 按下了失焦键");
    searchInputRef.value.blur?.();
  }
}

// 事件处理
// 切换主题
const toggleTheme = () => {
  console.log('DEBUG(toggleTheme): 切换主题');
  const nextTheme = currentTheme.value === 'dark' ? 'light' : 'dark';
  themeStore.setTheme(nextTheme);
}

// IO方法
// 导入音频文件（可多选）
const importVoiceFileHandle = async () => {
  const api = window.electronAPI;
  if (!api || typeof api.selectVoiceFile !== 'function') {
    console.warn('electronAPI.selectVoiceFile 不可用，当前环境非 Electron 或 preload 未加载');
    return;
  }

  const files: string[] = await api.selectVoiceFile({
    title: '选择音频文件',
    filters: [
      { name: '音频文件', extensions: ['wav', 'mp3', 'flac', 'm4a', 'ogg', 'webm'] },
      { name: '所有文件', extensions: ['*'] },
    ],
  });

  if (files && files.length > 0) {
    console.log('DEBUG(selectFile): 选择的音频文件路径为', files);
    // 本地导入
    const res = await localApi.post("/api/io/import/file", {paths: files});
    const results = res.data.data;
    console.log('DEBUG(import_file):results', results);
    let nextId = Number(getLocalStorage("next_id") || 1);
    console.log('DEBUG(import_file):nextId', nextId)
    const store: Voice[] = getLocalStorage("voice_info") || [];

    for (const r of results) {
      const v = r.voice;
      if (r.status === 'failed') {
        continue;
      }
      v.id = nextId;
      store.push(v);
      nextId++;
    }
    // 将数据存入缓存
    setLocalStorage("voice_info", store);
    setLocalStorage("next_id", nextId);
  } else {
    console.log('DEBUG(selectFile): 用户取消了音频文件选择');
  }
}

// 导入压缩语音包
const importPackageHandle = async () => {
  const api = window.electronAPI;
  if(!api || typeof api.selectCompressedFile !== 'function') {
    console.warn('electronAPI.selectCompressedFile 不可用，当前环境非 Electron 或 preload 未加载');
    return;
  }

  const filePath: string[] = await api.selectCompressedFile({
    title: '选择要导入的语音包',
  });
  if (!filePath) {
    console.log('用户取消了选择');
    return;
  }
  const response = await localApi.post("/api/io/import/package", null, {params: {path: filePath[0]}});
  const packageJson = response.data.data;
  console.log(packageJson);
  // 获取语音包数据
  let package_id: number = getLocalStorage('next_package_id') || 1
  const package_name: string = packageJson.package_name;
  if (package_name !== "全部语音") {
    const now: string = new Date().toString();
    const Package: PackageItem = {
      id: package_id,
      name: package_name,
      alias: null,
      isTop: false,
      voice_list: null,
      created_at: now,
      updated_at: now,
    };
    // 导入语音包数据
    let packageInfo = useLocalStorage("package_info", []);
    packageInfo.value.push(Package)
    setLocalStorage("next_package_id", ++package_id);
  }

  // 导入语音数据
  const voice_list: Voice[] = packageJson.result;
  let voice_id: number = getLocalStorage("next_id") || 1;
  const voiceInfo: Voice[] = getLocalStorage("voice_info") || [];
  const voice_map = new Map(voiceInfo.map(v => [v.hash_content, v]))
  for(const v of voice_list) {
    if (!voice_map.has(v.hash_content)) {
      v.id = voice_id;
      voice_id++;
      voiceInfo.push(v);
    }
  }
  // 数据写回缓存
  setLocalStorage("next_id", voice_id);
  setLocalStorage("voice_info", voiceInfo);
}

// 导出语音压缩包
const exportPackageHandle = async () => {
  const api = window.electronAPI;
  if (!api || typeof api.selectDirectory !== 'function') {
    console.warn('electronAPI.selectDirectory 不可用，当前环境非 Electron 或 preload 未加载');
    return;
  }

  const filePath = await api.selectDirectory({
    title: '选择目标文件夹',
  });
  if (filePath) {
    const packageId = props.packageChoose.id;
    const voiceInfo = getLocalStorage('voice_info') as Voice[];
    let packageName: string;
    let voiceInfoList: Voice[];
    if (packageId === 0) {
      packageName = "全部语音"
      voiceInfoList = voiceInfo
    } else {
      packageName = props.packageChoose.name;
      const packageInfo = getLocalStorage('package_info') as PackageItem[];

      // 获取语音信息
      const targerPackage = packageInfo.find(item => item.id === packageId);
      const voiceList = targerPackage?.voice_list ?? [];
      // 建立id -> voice索引
      const voiceMap = new Map(voiceInfo.map(v => [v.id, v]))
      // 获得语音信息列表
      voiceInfoList = voiceList
          .map(v => voiceMap.get(v))
          .filter((v): v is Voice => v != undefined);
    }

    const exportPackageRequest = {
      package_name: packageName,
      position: filePath,
      voice_list: voiceInfoList,
    }
    console.log('DEBUG:(exportPackage):', exportPackageRequest);
    await localApi.post(
      `/api/io/export`,
        exportPackageRequest,
        null,
    )
    console.log('DEBUG(export_package): 导出成功')
  } else {
    console.log('DEBUG(select_file): 用户取消了选择')
  }
}

onMounted(() => {
  document.addEventListener('keydown', handleKeyDown)
})

onUnmounted(() => {
  document.removeEventListener('keydown', handleKeyDown)
})
</script>

<style scoped>
i {
  font-family: "iconfont", serif;
  color: var(--primaryColor);
}

button {
  border: none;
  border-radius: 15px;
  background: transparent;
  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: center;
  width: 30px;
  height: 30px;
}

/* 按钮动效 */
button:active {
  transform: scale(0.9)
}

.head {
  display: flex;
  flex-direction: row;
  justify-content: flex-start;
  align-items: center;
  height: 50px;
  flex: 0 0 50px;
  margin-top: 0;
  background-color: var(--head);
}

.left-button-group {
  height: 100%;
  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: flex-start;
  flex: 1;
  margin: 10px;
}

.left-button-group i {
  font-size: 17px;
}

.search-group {
  display: flex;
  flex-direction: row;
  flex: 3;
}

.right-button-group {
  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: flex-end;
  flex: 1;
  margin: 10px;
}

.import-dropdown {
  border: none;
  border-radius: 15px;
  background: transparent;
  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: center;
  width: 30px;
  height: 30px;
}

.import-dropdown :deep(.el-button) {
  background-color: transparent !important;
}

.icon-import { font-size: 23px; }
.icon-export { font-size: 22px; }
.icon-file-manager { font-size: 18px; }

.search {
  flex: 3;
  color: var(--textColor);
}
</style>