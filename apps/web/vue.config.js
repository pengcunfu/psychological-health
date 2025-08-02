const { defineConfig } = require('@vue/cli-service')
module.exports = defineConfig({
  transpileDependencies: true,
  // 开发服务器配置
  devServer: {
    port: 8081, // 确保与您使用的端口一致
    proxy: {
      // 代理所有 /api 开头的请求到后端服务器
      '/api': {
        target: 'http://127.0.0.1:5000', // 使用 127.0.0.1 确保连接
        changeOrigin: true,
        pathRewrite: {
          '^/api': '' // 将 /api 前缀移除
        }
      }
    }
  }
})
