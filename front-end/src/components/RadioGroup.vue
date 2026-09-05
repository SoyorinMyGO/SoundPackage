<template>
  <div>
    <slot/>
  </div>
</template>

<script setup lang="ts">
import {provide, ref} from "vue";

// 默认渲染模式为button
const selectedValue = ref("button");

// 选中某个按钮
const selectButton = (value: string) => { selectedValue.value = value; }

// 暴露给父组件使用
defineExpose({selectedValue})

// 提供给子组件的数据和方法
provide('radioGroup',
  {
    selectButton,
    selectedValue
  }
);
</script>

<style scoped>
  div {
    width: 100%;
    height: 100%;
    display: flex;
    flex-direction: row;
    align-items: center;
    justify-content: center;
    background-color: var(--background);
    border: 1px solid var(--secondaryColor);
    border-radius: 8px;
    gap: 2px;
    padding: 2px;
  }
</style>