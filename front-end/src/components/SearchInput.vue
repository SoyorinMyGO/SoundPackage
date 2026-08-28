<template>
  <div :class="'search-wrapper'">
    <input
        ref="inputRef"
        type="text"
        :value="modelValue"
        @input="emit('update:modelValue', ($event.target as HTMLInputElement).value)"
        @blur="emit('blur', ($event.target as HTMLInputElement).value)"
        class="search-input"
    >
    <i class="icon icon-a-Searchbar_selected" v-if="!isSimple"></i>
    <kbd v-if="isSimple">Ctrl K</kbd>
    <i class="icon icon-search" v-if="isSimple"></i>
  </div>
</template>

<script setup lang="ts">
import {ref} from "vue";

const props = defineProps<{
  isSimple: Boolean,
  modelValue: String,
}>();

const emit = defineEmits<{
  (e: 'update:modelValue', value: string): void,
  (e: 'blur', value: string): void,
}>();

const inputRef = ref<HTMLInputElement | null>(null);

defineExpose({
  focus: () => {
    inputRef.value?.focus();
  },
  select: () => {
    inputRef.value?.select();
  },
  blur: () => {
    if (inputRef.value?.blur) inputRef.value.blur();
  }
})
</script>

<style scoped>
kbd {
  margin: 5px;
  padding: 0 3px 0 3px;
  font-size: 15px;
  color: var(--secondaryColor);
  border: 2px solid var(--secondaryColor);
  border-radius: 6px;
}

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
