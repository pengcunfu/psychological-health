<script>
import { onLaunch, onShow, onHide } from '@dcloudio/uni-app'
import { useUserStore } from './store/user'

export default {
  setup() {
    const userStore = useUserStore()
    
    onLaunch(() => {
      console.log('App Launch')
      // 初始化用户信息
      userStore.initUserInfo()
    })
    
    onShow(() => {
      console.log('App Show')
    })
    
    onHide(() => {
      console.log('App Hide')
    })
  }
}
</script>

<style lang="scss">
/* 引入uView基础样式 */
@import "uview-plus/index.scss";

/* 引入自定义全局样式 */
@import "./static/global.scss";

/* 引入主题样式 */
@import "./static/theme.scss";

page {
  background-color: #f5f7fa;
  font-family: -apple-system, BlinkMacSystemFont, 'Helvetica Neue', Helvetica,
    Segoe UI, Arial, Roboto, 'PingFang SC', 'miui', 'Hiragino Sans GB', 'Microsoft Yahei',
    sans-serif;
  color: #333;
  font-size: 28rpx;
  line-height: 1.6;
}
</style>
