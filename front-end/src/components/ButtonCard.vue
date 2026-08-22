<template>
<div class="card">
  <audio src="{{ resource }}"></audio>
</div>
</template>

<script setup>
defineProps({
  resource: String
})
</script>

<style scoped>

</style>