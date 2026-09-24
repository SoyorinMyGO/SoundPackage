<template>
  <!--语音列表-->
  <AudioComponent ref="audioComp" :resource="props.resource"/>
  <div class="voice-item">
    <!--语音操作按钮组-->
    <!--播放/暂停按钮-->
    <button @click="togglePlay">
      <i v-if="isPauseComputed" class="icon-play"></i>
      <i v-if="!isPauseComputed" class="icon-pause"></i>
    </button>
    <!--语音信息-->
    <div class="name-container">
      <span class="voice-name" v-if="!rename">{{ name }}</span>
      <input type="text" v-if="rename" :placeholder="name" v-model="alias">
      <button @click="renameHandle(alias)">
        <i v-if="!rename" class="icon-rename"/>
        <i v-if="rename" class="icon-rename-confirm"/>
      </button>
    </div>
    <span class="voice-length">{{ length }}</span>
    <span class="voice-used-time">使用次数:{{ props.resource.used_times }}</span>
    <span class="voice-updated-at">{{ updatedAt }}</span>
  </div>
</template>

<script setup lang="ts">
import AudioComponent from "./AudioComponent.vue";
import { computed, PropType, ref } from "vue";
import { Voice } from "../../model/Voice";
import {useLocalStorage} from "../../utils/LocalStorage/use_storage";

const props = defineProps({
  resource: {
    type: Object as PropType<Voice>,
    required: true,
    default: null,
  }
})

// 通过 ref 获取子组件暴露的方法和状态
const audioComp = ref<any>(null);
// 获取语音的信息
const name = computed<string>(() => {
  // 优先检查是否存在刚修改的alias
  if (alias.value) return alias.value;
  return props.resource.alias ? props.resource.alias : props.resource.name.split(".")[0];
});
const length = computed<string>(() => {
  return `${props.resource.length / 1000}s`
});
const updatedAt = computed<string>(() => {
  return props.resource.updated_at.split('T')[0];
});
const alias = ref<string>('');
const rename = ref<boolean>();
const voiceInfo = useLocalStorage<Record<string, Voice>>('voice_info', {});

const renameHandle = (alias: string) => {
  // 开启重命名
  if (!rename.value) {
    rename.value = true;
    return;
  }
  // 完成重命名
  const aliasValue = alias.trim();
  if (aliasValue) {
    const hash = props.resource.hash_content;
    const current = voiceInfo.value[hash];
    console.log('DEBUG(packageManagement.renameHandle):before change:voiceInfo', voiceInfo.value);
    console.log('DEBUG(packageManagement):current', current)
    if (current) {
      voiceInfo.value = {
        ...voiceInfo.value,
        [hash]: {
          ...current,
          alias: aliasValue,
        }
      }
      console.log('DEBUG(packageManagement.renameHandle):after change:voiceInfo', voiceInfo.value);
      // 同步到当前对象
      props.resource.alias = aliasValue;
    }
  }
  rename.value = false;
}

// 使用子组件暴露的方法
const togglePlay = () => {
  audioComp.value?.togglePlay?.();
}
// 将子组件的 refs 映射到计算属性
const isPauseComputed = computed(() => audioComp.value?.isPause?.value ?? true);
</script>

<style scoped>
i {
  font-family: "iconfont", serif;
  font-size: 13px;
}
button {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 22px;
  height: 22px;
  border: none;
  border-radius: 50%;
  margin: 5px;
  background-color: var(--primaryColor);
  color: var(--textColor);
}
button:active {
  transform: scale(0.95);
}
span {
  overflow: hidden;
}
input {
  flex: 1;
  height: stretch;
  background: transparent;
  border: 1px solid var(--primaryColor);
  border-radius: 4px;
  color: var(--textColor);
}

.voice-item {
  display: flex;
  align-items: center;
  margin: 0 20px 0 20px;
}
.voice-item:hover {
  border: 1px solid var(--primaryColor);
}

.name-container {
  display: flex;
  align-items: center;
  justify-content: space-between;
  flex: 3;
  padding: 5px;
  gap: 10px;
}
.voice-name {
  font-size: 16px;
  color: var(--textColor);
}

.voice-length {
  flex: 1;
  font-size: 13px;
}
.voice-used-time {
  flex: 1;
  font-size: 13px;
}
.voice-updated-at {
  flex: 1;
  display: flex;
  justify-content: flex-end;
  font-size: 13px;
  padding-right: 5px;
}
</style>