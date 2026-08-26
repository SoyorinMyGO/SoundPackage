<template>
  <div class="main-view">
    <!--顶部信息-->
    <div class="top">
      <span>{{ packageChoose.name }}</span>
      <div class="top-button-group">

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
  search: String,
  packageChoose: {
    type: Object,
    default: null,
  },
})

const responseData = ref<VoiceItem[]>([]);
const orderBy = ref<String>("");
const isDesc = ref<Number>(false);

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
    console.log('DEBUG(params):', params)
    const res = await apiClient.get("/api/voice", {params});
    responseData.value = res.data.data;
    console.log('DEBUG(voice_list):', responseData.value);
  }
  catch (e) {
    console.error(e);
  }
}

// 解包
const voiceList: VoiceItem[] = computed(() => {
  // 检查是否有数据
  if (!responseData.value || responseData.value.length === 0) {
    return [];
  }
  // 默认按照使用次数降序 -> 更新时间降序排序
  return responseData.value;
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

.top-button-group {
  height: 100%;
  width: 50%;
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