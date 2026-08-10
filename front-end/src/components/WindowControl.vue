<template>
  <div class="window-controls no-drag">
    <!-- 最小化 -->
    <button @click="minimize" :disabled="!isElectron" class="control-btn minimize-btn" :title="isElectron ? '最小化' : '仅在 Electron 中可用'">
      <svg viewBox="0 0 10 10" width="10" height="10">
        <rect x="0" y="4" width="10" height="1" fill="currentColor"/>
      </svg>
    </button>

    <!-- 最大化/还原 -->
    <button @click="maximize" :disabled="!isElectron" class="control-btn maximize-btn" :title="isElectron ? '最大化/还原' : '仅在 Electron 中可用'">
      <svg viewBox="0 0 10 10" width="10" height="10">
        <rect x="1" y="1" width="8" height="8" fill="none" stroke="currentColor" stroke-width="1"/>
      </svg>
    </button>

    <!-- 关闭 -->
    <button @click="close" :disabled="!isElectron" class="control-btn close-btn" :title="isElectron ? '关闭' : '仅在 Electron 中可用'">
      <svg viewBox="0 0 10 10" width="10" height="10">
        <line x1="1" y1="1" x2="9" y2="9" stroke="currentColor" stroke-width="1"/>
        <line x1="9" y1="1" x2="1" y2="9" stroke="currentColor" stroke-width="1"/>
      </svg>
    </button>
 </div>
</template>

<script setup>
// 安全地访问 Electron 暴露的 API（避免在非 Electron 环境或 preload 未生效时报错）
const electronAPI = (typeof window !== 'undefined' && window.electronAPI) ? window.electronAPI : null
const isElectron = !!electronAPI

const minimize = () => {
  if (electronAPI) {
    electronAPI.minimize()
  } else {
  }
}

const maximize = () => {
  if (electronAPI) {
    electronAPI.maximize()
  }
}

const close = () => {
  if (electronAPI) {
    electronAPI.close()
  }
}
</script>

<style scoped>
.window-controls {
  display: flex;
  gap: 8px;
  padding: 8px 12px;
  position: fixed;
  top: 0;
  right: 0;
  z-index: 999;
  -webkit-app-region: no-drag; /* 允许按钮点击，不被拖动 */
}

.control-btn {
  width: 30px;
  height: 30px;
  border: none;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  background: transparent;
  color: #666;
  transition: background 0.2s;
  -webkit-app-region: no-drag; /* 确保按钮本身为可交互区域 */
  pointer-events: auto;
}

.control-btn[disabled] {
  opacity: 0.55;
  cursor: default;
}
.control-btn:hover {
  background: rgba(0, 0, 0, 0.1);
}

.minimize-btn:hover {
  background: #e0e0e0;
}

.maximize-btn:hover {
  background: #e0e0e0;
}

.close-btn:hover {
  background: #e81123;
  color: white;
}

/* 暗色主题适配 */
@media (prefers-color-scheme: dark) {
  .control-btn {
    color: #ccc;
  }
  .control-btn:hover {
    background: rgba(255, 255, 255, 0.1);
  }
  .minimize-btn:hover {
    background: #404040;
  }
  .maximize-btn:hover {
    background: #404040;
  }
}
</style>