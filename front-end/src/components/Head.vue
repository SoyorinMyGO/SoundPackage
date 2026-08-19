<template>
<div class="head">
  <!-- 顶部栏 -->
  <button @click="emit('toggle')" id="toggleButton">
    <i class="icon icon-unfold" v-if="isCollapsed"></i>
    <i class="icon icon-fold" v-if="!isCollapsed"></i>

  </button>
</div>
</template>

<script setup>
defineProps({
  isCollapsed: Boolean
})

const emit = defineEmits(["toggle"]);

</script>

<style scoped>
.head {
  display: flex;
  flex-direction: row;
  justify-content: flex-start;
  height: 50px;
  flex: 0 0 50px;
  margin-top: 0;
  background-color: var(--head);
}
#toggleButton {
  margin-left: 10px;
  margin-top: 12px;
  width: 30px;
  height: 30px;
  align-self: flex-start;
  border: none;
  border-radius: 15px;
  background: transparent;
  color: #ffffff;
  position: relative;
  overflow: hidden;
}
/* 按钮动效 */
#toggleButton:active {
  transform: scale(0.9)
}
#toggleButton i{
  font-family: "iconfont",serif !important;
  color: var(--primaryColor)
}
</style>