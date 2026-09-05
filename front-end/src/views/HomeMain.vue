<template>
  <div class="main-view glass-background">
    <!--顶部信息-->
    <div class="top">
      <!--当前语音包名称-->
      <span>{{ packageChoose.name }}</span>

      <div class="top-button-group">
        <!--选择渲染模式-->
        <RadioGroup class="radio">
          <RadioButton :icon="ButtonRender" buttonValue="button"
                       class="leftest-radio-button"></RadioButton>
          <RadioButton :icon="GridRender" buttonValue="grid"></RadioButton>
          <RadioButton :icon="DetailRender" buttonValue="detail"
                       class="rightest-radio-button"></RadioButton>
        </RadioGroup>
        <!--筛选语音包-->
        <button @click="descHandle" id="desc-button" class="right-button-group">
          <i class="icon-down" v-if="isDesc"></i>
          <i class="icon-up" v-if="!isDesc"></i>
        </button>
        <el-dropdown placement="bottom" trigger="click">
            <el-button id="sort-menu" class="right-button-group">
              <i class="icon-sort"></i>
            </el-button>
          <template #dropdown>
            <el-dropdown-menu>
              <el-dropdown-item class="custom-menu-item" @click="fieldHandle('used_times')">使用次数</el-dropdown-item>
              <el-dropdown-item class="custom-menu-item" @click="fieldHandle('name')">名称</el-dropdown-item>
              <el-dropdown-item class="custom-menu-item" @click="fieldHandle('updated_at')">更新日期</el-dropdown-item>
            </el-dropdown-menu>
          </template>
        </el-dropdown>
        <button id="filter-button" class="right-button-group">
          <i class="icon-filter"></i>
        </button>
      </div>
    </div>
    <!--语音列表-->
    <el-scrollbar class="card-container">
      <div class="card-grid">
          <ButtonCard :resource="item"
                      v-for="item in sortedList"
                      :key="item.id"
          />
      </div>
    </el-scrollbar>
    <!--底部栏-->
    <div class="bottom">

    </div>
  </div>
</template>

<script setup lang="ts">
import {computed, ComputedRef, onMounted, ref, watch} from "vue";
import ButtonCard from "../components/ButtonCard.vue";
import apiClient from "../config/axios_config.js";
import RadioGroup from "../components/RadioGroup.vue";
import RadioButton from "../components/RadioButton.vue";

interface VoiceItem{
  id: number;
  name: string;
  alias: string | null;
  length: number;
  used_times: number;
  created_at: string;
  updated_at: string;
}

const props = defineProps({
  search: {
    type: String,
    dafault: '',
  },
  packageChoose: {
    type: Object,
    default: null,
  },
})

const responseData = ref<VoiceItem[]>([]);
const field = ref<String>("used_times");
const isDesc = ref<boolean>(true);
// 默认按钮模式渲染
const renderMode = ref<string>("button");
// 渲染模式变量
const ButtonRender: string = "icon-button";
const GridRender: string = "icon-grid";
const DetailRender: string = "icon-detail";

//初始化
// 获取选择的语音包
const getPackageId = () => {
  // 如果 packageChoose 不存在或没有 id，返回 0（表示全部）
  if (!props.packageChoose || !props.packageChoose.id) {
    return 0;
  }
  return props.packageChoose.id;
}

// 获取语音列表
const get_list = async() => {
  try {
    const packageId = getPackageId();
    const params = {
      package_id: packageId,
      tag_ids: []
    }
    const res = await apiClient.get("/api/voice", {params});
    responseData.value = res.data.data;
  }
  catch (e) {
    console.error(e);
  }
}

// 解包
const voiceDatas: ComputedRef<VoiceItem[]> = computed(() => {
  // 检查是否有数据
  if (!responseData.value || responseData.value.length === 0) {
    return [];
  }
  return responseData.value;
})

// 按字段过滤排序
const sortedList = computed(() => {
  let list = [...voiceDatas.value];
  // 搜索过滤
  const search: string = props.search;
  if (search !== '') {
    list = responseData.value.filter(item => {
      const lowerKeyword = search.toLowerCase();
      const nameMatch = item.name && item.name.toLowerCase().includes(lowerKeyword);
      const aliasMatch = item.alias && item.alias.toLowerCase().includes(lowerKeyword);
      return nameMatch || aliasMatch;
    })
  }
  const derection = isDesc.value === true ? -1 : 1;
  return list.sort((a, b) => {
    const key = field.value as keyof VoiceItem;
    let valA: string | number = a[key];
    let valB: string | number = b[key];
    let result:number;
    if (field.value === 'name') {
      // 按名字进行排序
      if (typeof valA !== 'string') valA = String(valA);
      if (typeof valB !== 'string') valB = String(valB);
      result = valA.localeCompare(valB, 'zh-Hans-CN', {sensitivity: 'base'});
    } else {
      // 数字或日期：a > b 返回 1，a < b 返回 -1
      result = (valA > valB ? 1 : (valA < valB ? -1 : 0));
    }
    return derection * result;
  })
})

// 事件处理
// 改变是否降序排列
const  descHandle = () => {
  isDesc.value = !isDesc.value;
  return;
}

// 改变排序依据
const fieldHandle = (val: string) => {
  field.value = val;
  return;
}

watch(
  () => props.packageChoose,
  (newVal, oldVal) => {
    // 避免重复请求
    if (JSON.stringify(newVal) === JSON.stringify(oldVal)) {
      return;
    }
    get_list();
  },
  { deep: true }
)

onMounted(() => {
  get_list();
})
</script>

<style scoped>
i { font-family: "iconfont", serif; }

.main-view {
  display: flex;
  flex-direction: column;
  align-items: center;
  flex: 1;
  background-color: var(--background);
  overflow: auto;
  border-radius: 12px 0 0 0;
}

.top {
  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: space-between;
  height: 50px;
  width: 100%;
}

.top>span {
  font-size: 20px;
  margin: 15px;
  max-width: 300px;
  overflow: hidden;
  white-space: nowrap;
}

.radio {
  width: 100px;
  height: 34px;
  margin-right: 15px;
}

.leftest-radio-button { border-radius: 4px 0 0 4px; }
.rightest-radio-button { border-radius: 0 4px 4px 0; }
.radio i {
  font-size: 30px;
}

.top-button-group {
  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: end;
  height: 100%;
  width: 50%;
  margin: 0 30px 0 30px;
}

.top-button-group button {
  width: 30px;
  height: 30px;
}
.right-button-group {
  background-color: var(--primaryColor);
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
#filter-button {
  border-radius: 0 5px 5px 0;
  border: none;
}

/*取消默认动效*/
:deep(.el-tooltip__trigger:focus-visible) {
  outline: none !important;
}

.top-button-group>button:active {
  transform: scale(0.95);
}

.top-button-group>.el-dropdown:active {
  transform: scale(0.95);
}

.top-button-group i {
  font-size: 20px;
  color: var(--textColor);
}

.card-container {
  width: 90%;
  flex: 1;
}

.card-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(120px, 1fr));
  grid-template-rows: repeat(auto-fill, 45px);
  gap: 12px;
  padding: 30px 0 30px 0;
}

.bottom {
  height: 50px;
  width: 100%;
}
</style>