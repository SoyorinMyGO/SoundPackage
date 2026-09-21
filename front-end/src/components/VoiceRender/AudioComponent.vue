<template>
  <audio
      ref="audioRef"
      :src="position"
      @timeupdate="onTimeUpdate"
      @ended="onEnded"
      @play="onPlay"
      @pause="onPause"
      @error="onError"
  ></audio>
</template>

<script setup lang="ts">
import { updateUsedTimes } from "../../utils/LocalStorage/update_used_times";
import {PropType, ref} from "vue";
import {Voice} from "../../model/Voice";
import {getPosition} from "../../utils/get_voice_resource";

const props = defineProps({
  resource: {
      type: Object as PropType<Voice>,
      required: true,
      default: null,
  }
})

// 本组件内部状态
const audioRef = ref<HTMLAudioElement | null>(null);
const isPause = ref<boolean>(true);
const isLoop = ref<boolean>(false);
const position = getPosition(props.resource);

// 监听事件
const onTimeUpdate = () => {}
const onEnded = () => {
  // 若父组件传入 resource 则记录使用次数
  try { if (props.resource) updateUsedTimes(props.resource); } catch (e) { /* noop */ }
  isPause.value = true;
  return;
}
const onPlay = () => {
  isPause.value = false;
  return;
}
const onPause = () => {
  isPause.value = true;
  return;
}
const onError = () => {
  isPause.value = true;
  console.error('音频资源加载失败', { src: audioRef.value?.src, position: position });
  return;
}

// 播放/暂停事件
const togglePlay = async () => {
  const audio = audioRef.value;
  // 若媒体不存在或没有可用来源则退出
  if (!audio || !audio.currentSrc) {
    console.warn('音频未准备好或无有效来源，无法播放');
    return;
  }

  if (audio.paused) {
    console.log('DEBUG(audio): 播放');
    // 将 loop 状态同步到元素
    audio.loop = isLoop.value;
    audio.load();
    try {
      await audio.play();
    } catch (e) {
      console.error('播放失败', e);
      console.error('音频源', audio.currentSrc);
    }
  } else {
    console.log('DEBUG(audio): 暂停');
    audio.pause();
  }
}

// 切换循环状态
const toggleLoop = () => {
  isLoop.value = !isLoop.value;
  if (audioRef.value) {
    audioRef.value.loop = isLoop.value;
  }
}

// 向父组件暴露的方法/状态
defineExpose({
  togglePlay,
  toggleLoop,
  isPause,
  isLoop,
  audioRef
});
</script>

<style scoped>

</style>