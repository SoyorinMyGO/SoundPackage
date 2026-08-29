<template>
  <div class="main-view">
    <!--顶部信息-->
    <div class="top">
      <span>{{ packageChoose.name }}</span>
      <div class="top-button-group">
        <button @click="descHandle" class="desc-button">
          <i class="icon-down" v-if="isDesc"></i>
          <i class="icon-up" v-if="!isDesc"></i>
        </button>
        <el-dropdown placement="bottom">
            <el-button id="sort-menu">
              <i class="icon-sort"></i>
            </el-button>
          <template #dropdown>
            <el-dropdown-menu>
              <el-dropdown-item @click="">desc</el-dropdown-item>
              <el-dropdown-item @click="">sort</el-dropdown-item>
              <el-dropdown-item @click="">filt</el-dropdown-item>
            </el-dropdown-menu>
          </template>
        </el-dropdown>
        <button class="filter-button">
          <i class="icon-filter"></i>
        </button>
      </div>
    </div>
    <!--语音列表-->
    <el-scrollbar class="card-container">
      <div class="card-grid">
          <ButtonCard :resource="item"
                      v-for="item in voiceList"
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
import {computed, onMounted, ref, watch} from "vue";
import ButtonCard from "../components/ButtonCard.vue";
import apiClient from "../config/axios_config.js";

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
const orderBy = ref<String>("used_times");
const isDesc = ref<Number>(true);

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
const voiceList: VoiceItem[] = computed(() => {
  console.log('DEBUG(get_voiceList): 触发解包计算属性')
  // 检查是否有数据
  if (!responseData.value || responseData.value.length === 0) {
    return [];
  }
  let result = responseData.value;
  // 搜索过滤
  const search: string = props.search;
  if (search !== '') {
    result = responseData.value.filter(item => {
      const lowerKeyword = search.toLowerCase();
      const nameMatch = item.name && item.name.toLowerCase().includes(lowerKeyword);
      const aliasMatch = item.alias && item.alias.toLowerCase().includes(lowerKeyword);
      return nameMatch || aliasMatch;
    })
  }
  // 默认按照使用次数降序 -> 更新时间降序排序
  if (orderBy.value === "used_times" && isDesc.value === true) {
    console.log('DEBUG(voiceList):', responseData.value)
    return result;
  }
})

watch(
  () => props.packageChoose,
  (newVal, oldVal) => {
    // 避免重复请求
    if (JSON.stringify(newVal) === JSON.stringify(oldVal)) {
      return;
    }
    console.log('packageChoose 变化，重新获取数据');
    get_list();
  },
  { deep: true }
)

onMounted(() => {
  get_list();
})
</script>

<style scoped>
i {
  font-family: "iconfont", serif;
}

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
.desc-button {
  border-radius: 5px 0 0 5px;
  border: none;
}
.filter-button {
  border-radius: 0 5px 5px 0;
  border: none;
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