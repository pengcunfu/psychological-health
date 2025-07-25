<template>
    <view>
        <up-tabs :list="tabsList" @click="click"></up-tabs>
    </view>

</template>
<script setup>
import { reactive, ref, defineProps } from 'vue';


const { TabsList } = defineProps({
    TabsList: Array
})
const tabsList = ref([
    { name: '关注' },
    { name: '推荐' },
    { name: '电影' },
    { name: '科技' },
    { name: '音乐' },
    { name: '美食' },
    { name: '文化' },
    { name: '财经' },
    { name: '手工' }
])

tabsList.value = TabsList



// 定义方法  
function click(item) {
    console.log('item', item);
}  
</script>