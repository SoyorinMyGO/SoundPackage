<template>
<div class="card">
  <audio
      ref="audioRef"
      :src="position"
      @timeupdate="onTimeUpdate"
      @ended="onEnded"
      @play="onPlay"
      @pause="onPause"
  ></audio>
  <!--播放/暂停按钮-->
  <button @click="togglePlay" class="isPlay">
    <i v-if="isPause" class="icon-play"></i>
    <i v-if="!isPause" class="icon-pause"></i>
  </button>
  <!--循环播放按钮-->
  <button @click="toggleLoop" class="isLoop">
    <i v-if="isLoop" class="icon-loop"></i>
    <i v-if="!isLoop" class="icon-unloop"></i>
  </button>
  <!--语音名（去后缀）-->
  <span :title="fullName">{{ nameWithoutSuffix }}</span>
</div>
</template>

<script setup lang="ts">
import {computed, ref} from "vue";

const props = defineProps({
  resource: {
    type: Object,
    required: true,
    default: null,
  }
})

const fileName = ref<string>('');
const alias = ref<string | null>('');
const audioRef = ref<HTMLAudioElement | null>(null) // 媒体对象
const isPause = ref<boolean>(true);  // 是否暂停
const isLoop = ref<boolean>(false);

// 去后缀文件名
const nameWithoutSuffix = computed(() => {
  if (!fileName.value) {
    return '';
  }
  return fileName.value.split('.')[0];
})

// 悬浮显示的全名（名字+（别名））
const fullName = computed(() => {
  if (!alias.value) {
    return fileName.value;
  }
  return `${fileName.value}(${alias.value})`;
})

// 获取文件路径
const position = computed(() => {
  if (!props.resource) { return '' }

  fileName.value = props.resource.name || '';
  if (!fileName.value) { return '' }

  const ext = fileName.value.includes('.') ? `.${fileName.value.split('.').pop()}` : '';
  const actualFileName = (props.resource.hash_content || fileName.value.replace(/\.[^/.]+$/, '')) + ext;

  try {
    // 实际音频文件按 hash_content 存储，name 只是展示名称。
    return `http://localhost:24990/assets/voices/${actualFileName}`;
  } catch (e) {
    console.error('音频路径生成失败', e);
    return '';
  }
})

// 监听事件
const onTimeUpdate = () => {}
const onEnded = () => {
  // 如果循环播放开启
  if (isLoop.value) {
    togglePlay();
    return;
  }
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
    try {
      await audio.play();
    } catch (e) {
      console.error('播放失败', e);
    }
  } else {
    console.log('DEBUG(audio): 暂停');
    audio.pause();
  }
}

// 循环事件
const toggleLoop = () => {
  isLoop.value = !isLoop.value;
  const audio = audioRef.value;
  if (audio) {
    audio.loop = isLoop.value;
  }
}
</script>

<style scoped>
button {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 22px;
  height: 22px;
  border-radius: 50%;
  border: none;
  color: var(--textColor);
  background-color: var(--primaryColor);
}

i {
  font-family: "iconfont", serif;
}

span {
  font-size: 12px;
  white-space: nowrap;
  overflow: hidden;
  margin-left: 3px;
}

.card {
  display: flex;
  flex-direction: row;
  align-items: center;
  flex: 1;
  height: 40px;
  padding: 6px;
  border-radius: 8px;
  border: 1px solid var(--borderColor);
  background-color: var(--cardColor);
  color: var(--textColor);
}

/*播放/暂停按钮*/
.isPlay {
  margin: 3px 5px 3px 0;
  flex-shrink: 0;
}

/*循环按钮*/
.isLoop {
  margin: 3px 3px 3px 0;
  flex-shrink: 0;
}

button>i {
  font-size: 13px;
}

.card>button:active {
  transform: scale(0.9);
}

</style>