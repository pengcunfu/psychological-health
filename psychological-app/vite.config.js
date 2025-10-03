import {defineConfig} from 'vite'
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
    define: {
        // 修复 uView Plus 在微信小程序中的兼容性问题
        'process.env.VUE_APP_PLATFORM': JSON.stringify(process.env.UNI_PLATFORM)
    },
    build: {
        rollupOptions: {
            external: []
        }
    }
})
