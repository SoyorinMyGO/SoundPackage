<template>
  <div class="main-view">
    <div class="top">
      <span>{{  }}</span>
    </div>
    <el-scrollbar class="card-container">
      <div class="card-grid">
          <ButtonCard :resource="item"
                      v-for="item in voiceList"
                      :key="item.id"
          />
      </div>
    </el-scrollbar>
    <div class="bottom">

    </div>
  </div>
</template>

<script setup lang="ts">
import {computed, onMounted, ref} from "vue";
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
})

const responseData = ref<VoiceItem[]>([]);
const orderBy = ref("");
const isDesc = ref(false);
// 获取语音列表
const get_list = async() => {
  try {
    const res = await apiClient.get("/api/voice");
    responseData.value = res.data.data;
    console.log('DEBUG(voice_list):返回全部', responseData.value);
  }
  catch (e) {
    console.error(error);
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
  height: 50px;
  width: 100%;
}

.card-container {
  width: 90%;
  flex: 1;
}

.card-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(120px, 1fr));
  grid-template-rows: repeat(auto-fit, 45px);
  gap: 12px;
  padding: 30px 0 30px 0;
}

.bottom {
  height: 50px;
  width: 100%;
}
</style>