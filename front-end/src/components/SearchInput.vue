<template>
  <div :class="'search-wrapper'">
    <input type="text" class="search-input"
           :value="modelValue"
            @input="emit('update:modelValue', ($event.target as HTMLInputElement).value)"
            @blur="emit('blur', ($event.target as HTMLInputElement).value)">
    <i class="icon icon-a-Searchbar_selected" v-if="!isSimple"></i>
    <i class="icon icon-search" v-if="isSimple"></i>
  </div>
</template>

<script setup lang="ts">
const props = defineProps<{
  isSimple: Boolean,
  modelValue: String,
}>();

const emit = defineEmits<{
  (e: 'update:modelValue', value: string): void,
  (e: 'blur', value: string): void,
}>();
</script>

<style scoped>
.search-wrapper {
  display: flex;
  align-items: center;
  flex: 1;
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
  color: var(--textColor);
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
