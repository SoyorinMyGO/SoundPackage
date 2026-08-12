<template>
<div class="head">
  <!-- 顶部栏 -->
  <button @click="emit('toggle')" id="toggleButton">
    <i class="icon icon-unfold" v-if="!isCollapsed"></i>
    <i class="icon icon-fold" v-if="isCollapsed"></i>

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
  height: 30px;
  flex: 0 0 50px;
  margin-top: 24px;
  background-color: var(--head);
}
#toggleButton {
  margin-left: 6px;
  margin-top: 8px;
  width: 40px;
  height: 40px;
  align-self: flex-start;
  border: none;
  background: transparent;
  color: #ffffff
}
#toggleButton i{
  font-family: "iconfont",serif !important;
  color: var(--primaryColor)
}
</style>