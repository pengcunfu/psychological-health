import { request } from '@/utils/request'

// 横幅管理API
export const bannerAPI = {
    // 获取横幅列表
    getBanners: (params = {}) => {
        return request({
            url: '/banner',
            method: 'GET',
            data: params
        })
    },
    
    // 获取横幅详情
    getBanner: (id) => {
        return request({
            url: `/banner/${id}`,
            method: 'GET'
        })
    },
    
    // 创建横幅
    createBanner: (data) => {
        return request({
            url: '/banner',
            method: 'POST',
            data
        })
    },
    
    // 更新横幅
    updateBanner: (id, data) => {
        return request({
            url: `/banner/${id}`,
            method: 'PUT',
            data
        })
    },
    
    // 删除横幅
    deleteBanner: (id) => {
        return request({
            url: `/banner/${id}`,
            method: 'DELETE'
        })
    }
}

export default bannerAPI 