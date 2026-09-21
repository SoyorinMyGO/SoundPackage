<template>
<div class="card">
  <AudioComponent ref="audioComp" :resource="props.resource"/>
  <!--播放/暂停按钮-->
  <button @click="togglePlay" class="isPlay">
    <i v-if="isPauseComputed" class="icon-play"></i>
    <i v-if="!isPauseComputed" class="icon-pause"></i>
  </button>
  <!--循环播放按钮-->
  <button @click="toggleLoop" class="isLoop">
    <i v-if="isLoopComputed" class="icon-loop"></i>
    <i v-if="!isLoopComputed" class="icon-unloop"></i>
  </button>
  <!--语音名（去后缀）-->
  <span>{{ showedName }}</span>
</div>
</template>

<script setup lang="ts">
import { computed, PropType, ref } from "vue";
import { Voice } from "../../model/Voice";
import AudioComponent from "./AudioComponent.vue";
import {getPosition, getShowedName} from "../../utils/get_voice_resource";

const props = defineProps({
  resource: {
    type: Object as PropType<Voice>,
    required: true,
    default: null,
  }
})

const showedName = getShowedName(props.resource.name, props.resource.alias);

// 通过 ref 获取子组件暴露的方法和状态
const audioComp = ref<any>(null);

// 使用子组件暴露的方法
const togglePlay = () => {
  audioComp.value?.togglePlay?.();
}
const toggleLoop = () => {
  audioComp.value?.toggleLoop?.();
}

// 将子组件的 refs 映射到计算属性
const isPauseComputed = computed(() => audioComp.value?.isPause?.value ?? true);
const isLoopComputed = computed(() => audioComp.value?.isLoop?.value ?? false);
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