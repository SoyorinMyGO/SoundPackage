<template>
<Teleport to="body">
  <Transition name="fade">
    <div v-if="modelValue" id="mask" @click.self="close">
      <div class="main">
        <!--顶部操作栏-->
        <div class="top">
          <button @click="deleteFileHandle">
            <i class="icon icon-delete" id="deleteFile"></i>
          </button>
          <button @click="addToDirHandle">
            <i class="icon icon-add-to-dir"></i>
          </button>
          <SearchInput :is-simple=false v-model="formData.name" class="search"/>
          <package-select :list="packageNameList"/>
        </div>
        <!--语音列表操作-->
        <div class="mid-div">
          <button @click="descHandle" id="desc-button" class="button-group">
          <i class="icon-down" v-if="isDesc"></i>
          <i class="icon-up" v-if="!isDesc"></i>
        </button>
        <el-dropdown placement="bottom" trigger="click">
            <el-button id="sort-menu" class="button-group">
              <i class="icon-sort"></i>
            </el-button>
          <template #dropdown>
            <el-dropdown-menu>
              <el-dropdown-item @click="fieldHandle('used_times')">使用次数</el-dropdown-item>
              <el-dropdown-item @click="fieldHandle('length')">时长</el-dropdown-item>
              <el-dropdown-item @click="fieldHandle('name')">名称</el-dropdown-item>
              <el-dropdown-item @click="fieldHandle('updated_at')">更新日期</el-dropdown-item>
            </el-dropdown-menu>
          </template>
        </el-dropdown>
        <button id="choose-all-button" class="button-group">
          <i class="icon-choose-all"></i>
        </button>
        </div>
        <!--语音内容-->
        <div>
        </div>
      </div>
    </div>
  </Transition>
</Teleport>
</template>

<script setup lang="ts">
import SearchInput from "./SearchInput.vue";
import {computed, ref} from "vue";
import {getLocalStorage} from "../utils/LocalStorage/local_storage";
import {PackageItem} from "../model/Package";
import PackageSelect from "./PackageSelect.vue";

const props = defineProps({
  modelValue: {
    type: Boolean,
    default: false,
  }
});
const emit = defineEmits<{
  (e: 'update:modelValue', val: boolean): void
}>();

const formData = ref({name: ''});
const packageInfo = ref<PackageItem[] | null>(getLocalStorage<PackageItem[] | null>("package_info"));
const currentPackage = ref<string>('全部语音');
const isDesc = ref<boolean>(false);
const field = ref<String>("used_times");
 
const search = computed(() => formData.value.name.trim());
const packageNameList = computed(() => {
  let list: string[] = ['全部语音'];
  return [...list, ...(packageInfo.value ?? []).map((item: PackageItem) => item.name)];
})

// 点击事件
// 关闭弹窗
const close = () => {
  emit('update:modelValue', false);
}

// 删除语音
const deleteFileHandle = () => {
  console.log('DEBUG(packageNameList):', packageNameList.value);
}

// 将语音添加至语音包
const addToDirHandle = () => {

}

// 改变是否降序排列
const descHandle = () => {
  isDesc.value = !isDesc.value;
  return;
}

// 改变排序依据
const fieldHandle = (val: string) => {
  field.value = val;
  return;
}
</script>

<style scoped>
i {
  font-family: "iconfont", serif;
  color: var(--primaryColor);
}

#mask {
  position: fixed;
  inset: 0;
  z-index: 1000;
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: rgba(0, 0, 0, 0.3);
  border-radius: 12px;
}

/*淡入淡出动画*/
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

.main {
  width: 70%;
  height: 70%;
  border-radius: 10px;
  background-color: var(--background);
}

.top {
  width: 100%;
  height: 50px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 20px 0 20px;
  gap: 15px;
}
.top>button {
  width: 25px;
  height: 25px;
  border: none;
  border-radius: 5px;
  background: transparent;
  display: flex;
  align-items: center;
  justify-content: center;
}
.top i {
  width: 25px;
  height: 25px;
  font-size: 25px;
}
#deleteFile {
  color: #ba1b26;
}
.search {
  flex: 1;
  margin: 7px 0 8px 0;
  height: 35px;
}

.mid-div {
  width: 100%;
  height: 35px;
  padding: 20px;
  display: flex;
  justify-content: flex-end;
  align-items: center;
}
.mid-div button {
  width: 30px;
  height: 30px;
}
/*取消el-dropdown默认的边缘*/
.el-button {
  border-radius: 0;
  border-left: 1px solid var(--borderColor);
  border-right: 1px solid var(--borderColor);
  border-top: none;
  border-bottom: none;
}
#desc-button {
  border-radius: 5px 0 0 5px;
  border: none;
}
#choose-all-button {
  border-radius: 0 5px 5px 0;
  border: none;
}
.button-group {
  background-color: var(--primaryColor);
}
/*取消默认动效*/
:deep(.el-tooltip__trigger:focus-visible) {
  outline: none !important;
}
.mid-div>button:active {
  transform: scale(0.95);
}

.mid-div>.el-dropdown:active {
  transform: scale(0.95);
}
.mid-div i {
  font-size: 20px;
  color: var(--textColor);
}
</style>