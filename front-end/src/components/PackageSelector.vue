<template>
  <div class="selector" ref="rootRef">
    <!-- 触发器 -->
    <div class="trigger" :class="{'dropdown-open': isOpen}" @click="toggle">
      <span>{{ selected.name }}</span>
    </div>
    <button class="add-button" :class="{'dropdown-open': isOpen}" @click="addDir">
      <span> + </span>
    </button>

    <!-- 下拉面板 -->
    <transition
      @before-enter="beforeEnter"
      @enter="enter"
      @after-enter="afterEnter"
      @before-leave="beforeLeave"
      @leave="leave"
      @after-leave="afterLeave"
    >
      <div v-if="isOpen" class="dropdown" ref="dropdownRef">

        <!-- 滚动区 -->
        <div class="scroll-area">
          <div
            v-for="item in props.list"
            :key="item.id"
            class="option"
            @click="select(item.id, item.name)"
          >
            {{ item.name }}
          </div>
          <div v-if="!props.list.length" class="empty">无数据</div>
        </div>
      </div>
    </transition>
  </div>
</template>

<script setup lang="ts">
import {ref, onMounted, onBeforeUnmount, PropType} from 'vue';

export interface PackageInfo {
  id: number;
  name: string;
}

const props = defineProps({
  list: {type: Array as PropType<PackageInfo[]>, default: () => []},
});
const emits = defineEmits<{(e: 'selected', choosePackage: PackageInfo): PackageInfo}>();

const isOpen = ref<boolean>(false);
const rootRef = ref<HTMLElement | null>(null);
const dropdownRef = ref<HTMLElement | null>(null);
const selected = ref<PackageInfo>({
  id: 0,
  name: '全部语音',
});

const toggle = () => { isOpen.value = !isOpen.value; }
const select = (id: number, name: string) => {
  selected.value.id = id;
  selected.value.name = name;
  isOpen.value = false;
  // 传递数据到父组件
  emits('selected', {id, name});
};

// 点击外部关闭
const handleClickOutside = (e: Event) => {
  const root = rootRef.value as HTMLElement | null;
  if (root && !root.contains(e.target as Node)) {
    isOpen.value = false
  }
};

// 添加新语音包
const addDir = () => {

};

function setHeight(el: HTMLElement, height: number | string) {
  el.style.height = typeof height === 'number' ? `${height}px` : (height as string);
}

function getInnerContentHeight(el: HTMLElement) {
  const content = el.querySelector('.scroll-area') as HTMLElement | null;
  if (content) return content.scrollHeight;
  return el.scrollHeight;
}

const beforeEnter = (el: HTMLElement) => {
  el.style.overflow = 'hidden';
  setHeight(el, 0);
};
const enter = (el: HTMLElement, done?: () => void) => {
  const height = getInnerContentHeight(el);
  void el.offsetHeight; // force reflow
  el.style.transition = 'height 0.25s ease';
  setHeight(el, height);
  const onEnd = (e: Event) => {
    if ((e as TransitionEvent).propertyName !== 'height') return;
    el.removeEventListener('transitionend', onEnd);
    if (done) done();
  };
  el.addEventListener('transitionend', onEnd);
};
const afterEnter = (el: HTMLElement) => {
  el.style.height = '';
  el.style.overflow = '';
  el.style.transition = '';
};

const beforeLeave = (el: HTMLElement) => {
  el.style.overflow = 'hidden';
  setHeight(el, getInnerContentHeight(el));
};
const leave = (el: HTMLElement, done?: () => void) => {
  void el.offsetHeight;
  el.style.transition = 'height 0.25s ease';
  setHeight(el, 0);
  const onEnd = (e: Event) => {
    if ((e as TransitionEvent).propertyName !== 'height') return;
    el.removeEventListener('transitionend', onEnd);
    if (done) done();
  };
  el.addEventListener('transitionend', onEnd);
};
const afterLeave = (el: HTMLElement) => {
  el.style.height = '';
  el.style.overflow = '';
  el.style.transition = '';
};

onMounted(() => document.addEventListener('click', handleClickOutside));
onBeforeUnmount(() => document.removeEventListener('click', handleClickOutside));
</script>

<style scoped>
.option,
.trigger,
.add-button {
  border: none;
  background-color: var(--primaryColor);
  color: var(--textColor);
}
.selector {
  position: relative;
  width: 160px;
  height: 35px;
  display: flex;
}
.trigger {
  flex: 5;
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 8px 12px;
  border: none;
  border-radius: 4px 0 0 4px;
  cursor: pointer;
}
.add-button {
  display: flex;
  align-items: center;
  justify-content: center;
  flex: 2;
  border-left: 1px solid var(--secondaryColor);
  border-radius: 0 4px 4px 0;
}
.add-button>span {
  font-size: 27px;
}
.add-button:active {
  transform: scale(0.95);
}

.arrow {
  transition: transform 0.2s;
}
.arrow.open {
  transform: rotate(180deg);
}

/* 下拉面板绝对定位 */
.dropdown {
  position: absolute;
  top: 100%;
  left: 0;
  right: 0;
  border: none;
  border-radius: 0 0 4px 4px;
  z-index: 1000;
  display: flex;
  flex-direction: column;
  max-height: 300px;
}
.dropdown-open {
  border-bottom: 1px solid var(--secondaryColor);
}
.dropdown-close {
  height: 0;
}

.scroll-area {
  overflow-y: auto;
  flex: 1;
  min-height: 0;
  border-radius: 0 0 4px 4px;
}

.option {
  padding: 8px 12px;
  cursor: pointer;
}
.option:hover {
  background: var(--hover);
}
.empty {
  padding: 16px;
  text-align: center;
  color: #999;
}

.scroll-area::-webkit-scrollbar {
  width: 6px;
}
.scroll-area::-webkit-scrollbar-thumb {
  background: #c0c4cc;
  border-radius: 3px;
}
</style>