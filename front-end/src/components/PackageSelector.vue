<template>
  <div class="selector" ref="rootRef">
    <!-- 触发器 -->
    <div class="trigger" :class="{'dropdown-open': isOpen}" @click="toggle">
      <span>{{ selected.name }}</span>
    </div>
    <!--添加语音包按钮-->
    <button class="add-button" :class="{'dropdown-open': isOpen}" @click="openAddPkgDialog">
      <span> + </span>
    </button>
    <el-dialog
      title="添加语音包"
      class="sy-dialog"
      v-model="dialogVisible"
      align-center
    >
      <input v-model="packageName" placeholder="请输入新语音包名称"/>
      <div class="add-pkg-button-group">
        <button @click="addPkgHandle" class="settle-button">确 定</button>
        <button @click="cancelHandle" class="cancel-button">取 消</button>
      </div>
    </el-dialog>

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
import {add_new_package} from "../utils/PackageData/add_new_package";
import {PackageItem} from "../model/Package";

export interface PackageInfo {
  id: number;
  name: string;
}

const props = defineProps({
  list: {type: Array as PropType<PackageInfo[]>, default: () => []},
});
const emits = defineEmits<{
  (e: 'selected', choosePackage: PackageInfo): PackageInfo,
  (e: 'refresh-sidebar'): void,
}>();

const isOpen = ref<boolean>(false);
const rootRef = ref<HTMLElement | null>(null);
const dropdownRef = ref<HTMLElement | null>(null);
const selected = ref<PackageInfo>({
  id: 0,
  name: '全部语音',
});
const dialogVisible = ref(false);
const packageName = ref('');

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
const openAddPkgDialog = () => {
  dialogVisible.value = true;
};
const addPkgHandle = () => {
  if (packageName.value.trim() === '') {
    alert('语音包名称不能为空');
    return;
  }

  add_new_package(packageName.value.trim());

  dialogVisible.value = false;
  packageName.value = '';

  emits('refresh-sidebar');
}
const cancelHandle = () => {
  dialogVisible.value = false;
  packageName.value = '';
}

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
:deep(.sy-dialog) {
  color: var(--textColor);
  background: var(--background);
}
:deep(.sy-dialog .el-dialog__title) {
  color: var(--textColor);
}
.sy-dialog input {
  background-color: transparent;
  border: 1px solid var(--secondaryColor);
  border-radius: 4px;
  height: 40px;
  width: 100%;
  padding: 10px;
  overflow: hidden;
  color: var(--textColor);
}
.add-pkg-button-group {
  display: flex;
  justify-content: flex-end;
  margin-top: 10px;
  gap: 10px;
}
.add-pkg-button-group>button {
  width: 80px;
  height: 30px;
  border-radius: 4px;
  background-color: transparent;
  position: relative;
  overflow: hidden;
}
.settle-button {
  border: 1px solid var(--primaryColor);
  color: var(--primaryColor);
}
.cancel-button {
  border: 1px solid var(--secondaryColor);
  color: var(--secondaryColor);
}
.sy-dialog button:active {
  transform: scale(0.95);
}
.sy-dialog button::after {
  content: '';
  position: absolute;
  top: -50%;
  left: -50%;
  width: 200%;
  height: 200%;
  background: radial-gradient(circle, var(--hover) 20%, transparent 70%);
  opacity: 0.2;
  transition: opacity 0.5s;
}
.sy-dialog button:hover::after {
  opacity: 1;
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