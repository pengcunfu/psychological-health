import { defineConfig } from 'vite'
import uni from '@dcloudio/vite-plugin-uni'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [
    uni(),
  ],
  css: {
    preprocessorOptions: {
      scss: {
        api: 'modern-compiler', // 使用现代编译器
        silenceDeprecations: ['legacy-js-api', 'import'], // 抑制特定的deprecation警告
      }
    }
  },
  optimizeDeps: {
    include: ['uview-plus']
  },
  build: {
    rollupOptions: {
      external: []
    }
  }
})
