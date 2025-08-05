<template>
  <u-tabbar
    :value="currentIndex"
    @change="switchTab"
    :fixed="true"
    :safeAreaInsetBottom="true"
    activeColor="#4A90E2"
    inactiveColor="#999999"
    :border="false"
  >
    <u-tabbar-item
      v-for="(item, index) in tabList"
      :key="index"
      :text="item.text"
    >
      <template #active-icon>
        <SvgIcon 
          :name="item.iconName" 
          :active="true"
          :size="44"
        />
      </template>
      <template #inactive-icon>
        <SvgIcon 
          :name="item.iconName" 
          :active="false"
          :size="44"
        />
      </template>
    </u-tabbar-item>
  </u-tabbar>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import SvgIcon from '../SvgIcon/index.vue'

const currentIndex = ref(0)

const tabList = [
  {
    pagePath: '/pages/index/index',
    iconName: 'home',
    text: '首页'
  },
  {
    pagePath: '/pages/counselor/index',
    iconName: 'counselor',
    text: '咨询'
  },
  {
    pagePath: '/pages/course/index',
    iconName: 'course',
    text: '课程'
  },
  {
    pagePath: '/pages/profile/index',
    iconName: 'profile',
    text: '我的'
  }
]

// 切换标签页
const switchTab = (index) => {
  if (currentIndex.value === index) return
  
  const targetPath = tabList[index].pagePath
  currentIndex.value = index
  
  uni.switchTab({
    url: targetPath,
    success: () => {
      console.log('切换成功:', targetPath)
    },
    fail: (err) => {
      console.error('切换失败:', err)
    }
  })
}

// 获取当前页面路径对应的索引
const getCurrentIndex = () => {
  const pages = getCurrentPages()
  if (pages.length > 0) {
    const currentPage = pages[pages.length - 1]
    const route = '/' + currentPage.route
    
    // 检查是否是tabBar页面（需要去掉可能的参数）
    const basePath = route.split('?')[0]
    
    // 找到对应的索引
    const index = tabList.findIndex(item => item.pagePath === basePath)
    if (index !== -1) {
      currentIndex.value = index
    }
  }
}

onMounted(() => {
  getCurrentIndex()
})

// 监听页面显示
uni.$on('tabBarPageShow', () => {
  getCurrentIndex()
})
</script>

<style lang="scss" scoped>
// 重写uview tabbar的一些样式以确保图标正确显示
:deep(.u-tabbar-item__icon) {
  margin-bottom: 4rpx !important;
}

:deep(.u-tabbar-item__text) {
  font-size: 24rpx !important;
}
</style> 