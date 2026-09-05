<template>
<button @click="clickHandle" :class="{ 'button-focused': isFocused }">
  <i :class="[props.icon, { 'font-focused': !isFocused}]"></i>
</button>
</template>

<script setup lang="ts">
import {computed, inject} from "vue";

const props = defineProps({
  icon: {
    type: String,
    default: '',
  },
  buttonValue: {
    type: String,
    default: '',
  }
});

// 注入 RadioGroup 提供的数据
const radioGroup = inject('radioGroup', null);

// 计算当前按钮是否为选择按钮
const isFocused = computed(() => {
  console.log("DEBUG(radioGroup?.selectedValue)", radioGroup?.selectedValue.value);
  console.log("DEBUG(props.buttonValue)", props.buttonValue);
  const value = radioGroup?.selectedValue.value === props.buttonValue;
  console.log(`DEBUG(${props.buttonValue}): ${value}`);
  return value;
})
// 点击事件处理
const clickHandle = () => {
  radioGroup?.selectButton(props.buttonValue);
  console.log("--------------")
  console.log("DEBUG(selectedvalue)", props.buttonValue);
}
</script>

<style scoped>
button {
  display: flex;
  flex-direction: row;
  justify-content: center;
  align-items: center;
  flex: 1;
  border: none;
  background-color: rgba(0, 0, 0, 0);
}

i {
  font-family: "iconfont", serif;
  font-size: 20px;
}

button:active {
  transform: scale(0.9);
}

.button-focused { background-color: var(--primaryColor) !important; }
.font-focused { color: var(--textColor) !important; }
</style>