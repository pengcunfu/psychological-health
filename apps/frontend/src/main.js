import {createSSRApp} from 'vue'
import App from './App.vue'
import pinia from './store'

import {setConfig} from 'uview-plus'
// 导入uViewPlus样式
import 'uview-plus/index.scss'

// 配置uViewPlus
setConfig({
    // 修改$u.config对象的属性
    config: {
        // 修改默认单位为rpx，相当于执行 uni.$u.config.unit = 'rpx'
        unit: 'rpx'
    },
    // 修改$u.props对象的属性
    props: {
        // 可以在这里配置组件的默认属性
        navbar: {
            safeAreaInsetTop: true,
            placeholder: true,
            fixed: true,
            zIndex: 980
        }
    }
})

export function createApp() {
    const app = createSSRApp(App)

    // 使用Pinia状态管理
    app.use(pinia)


    // 在H5环境下确保uViewPlus正确初始化
    if (typeof window !== 'undefined') {
        // 确保uni对象存在
        if (!window.uni) {
            window.uni = {}
        }

    }

    return {
        app
    }
}
