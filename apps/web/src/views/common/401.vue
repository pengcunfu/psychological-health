<template>
  <div class="unauthorized-container">
    <div class="unauthorized-content">
      <h1>401</h1>
      <h2>Unauthorized</h2>
      <p>Sorry, you are not authorized to access this page.</p>
      <el-button type="primary" @click="goBack">Go Back</el-button>
      <el-button @click="goHome">Back to Home</el-button>
    </div>
  </div>
</template>

<script setup>
import { useRouter } from 'vue-router'

const router = useRouter()

const goBack = () => {
  router.go(-1)
}

const goHome = () => {
  router.push('/')
}
</script>

<style lang="scss" scoped>
.unauthorized-container {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
  background-color: #f8f9fa;
}

.unauthorized-content {
  text-align: center;
  padding: 40px;
  border-radius: 8px;
  background-color: #fff;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
  max-width: 500px;

  h1 {
    font-size: 80px;
    margin: 0;
    color: #f56c6c;
  }

  h2 {
    font-size: 30px;
    margin: 10px 0 20px;
    color: #606266;
  }

  p {
    font-size: 16px;
    color: #909399;
    margin-bottom: 30px;
  }

  .el-button {
    margin: 0 10px;
  }
}
</style>
