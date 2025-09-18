<template>
  <div id="app">
    <router-view/>
  </div>
</template>

<script setup>
// App.vue 使用 setup 语法糖，无需额外的逻辑
</script>

<style lang="scss">
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  height: 100%;
}

/* 全局样式重置 */
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

html, body {
  height: 100%;
}

/* 滚动条样式 */
::-webkit-scrollbar {
  width: 8px;

  &-track {
    background: #f1f1f1;
  }

  &-thumb {
    background: #c1c1c1;
    border-radius: 4px;

    &:hover {
      background: #a8a8a8;
    }
  }
}
</style>
