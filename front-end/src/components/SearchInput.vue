<template>
  <div :class="'search-wrapper'">
    <input type="text" v-model="search" class="search-input">
    <i class="icon icon-a-Searchbar_selected"></i>
  </div>
</template>

<script setup>
const search=defineModel()
</script>

<style scoped>
.search-wrapper {
  display: flex;
  align-items: center;
  width: 100%;
  margin-top: 15px;
  background-color: var(--background);
  border-radius: 5px;
  padding: 0 12px;
  min-width: 0;
  align-self: stretch;
}

.search-input {
  height: 35px;
  flex: 1 1 0;
  min-width: 0;
  border: none;
  border-radius: 5px;
  background: var(--background);
}

.search-input:focus {
  outline: none;
}

i {
  color: var(--primaryColor);
  font-size: 18px;
  font-family: "iconfont", serif !important;
  margin-left: 8px;
  flex-shrink: 0;
}
</style>
