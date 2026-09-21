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
    <span class="voice-name">{{ name }}</span>
    <span class="voice-length">{{ length }}</span>
    <span class="voice-used-time">使用次数:{{ props.resource.used_times }}</span>
    <span class="voice-updated-at">{{ updatedAt }}</span>
  </div>
</template>

<script setup lang="ts">
import AudioComponent from "./AudioComponent.vue";
import { computed, PropType, ref } from "vue";
import { Voice } from "../../model/Voice";

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
  return props.resource.alias ? props.resource.alias : props.resource.name.split(".")[0];
})
const length = computed<string>(() => {
  return `${props.resource.length / 1000}s`
})
const updatedAt = computed<string>(() => {
  return props.resource.updated_at.split('T')[0];
})

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

.voice-item {
  display: flex;
  align-items: center;
  margin: 0 20px 0 20px;
}
.voice-item:hover {
  border: 1px solid var(--primaryColor);
}

.voice-name {
  flex: 3;
  font-size: 16px;
  padding-left: 5px;
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