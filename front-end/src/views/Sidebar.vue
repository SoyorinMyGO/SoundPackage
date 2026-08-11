<template>
<div class="side-bar" :class="{ collapsed: isCollapsed }">
  <!-- 侧边栏 -->
</div>
</template>

<script setup>
defineProps({
  isCollapsed: Boolean
})

</script>

<style scoped>
.side-bar {
  width: 0;
  background: var(--side-bar);
  overflow: auto;
  transition: width 0.5s ease;
}

.collapsed {
  width: 250px;
}
</style>