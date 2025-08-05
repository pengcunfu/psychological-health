<template>
  <div class="not-found-container">
    <div class="not-found-content">
      <h1>404</h1>
      <h2>Page Not Found</h2>
      <p>Sorry, the page you are looking for does not exist.</p>
      <el-button type="primary" @click="goBack">Go Back</el-button>
      <el-button @click="goHome">Back to Home</el-button>
    </div>
  </div>
</template>

<script>
export default {
  name: 'NotFound',
  methods: {
    goBack() {
      this.$router.go(-1)
    },
    goHome() {
      this.$router.push('/')
    }
  }
}
</script>

<style scoped>
.not-found-container {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
  background-color: #f8f9fa;
}

.not-found-content {
  text-align: center;
  padding: 40px;
  border-radius: 8px;
  background-color: #fff;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
  max-width: 500px;
}

h1 {
  font-size: 80px;
  margin: 0;
  color: #409eff;
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
</style>
