/**
 * API统一导出文件
 * 提供所有API的统一入口
 */

// 导入所有API模块
import { authAPI } from './auth'
import { assessmentAPI } from './assessment'
import { counselorAPI } from './counselor'
import { consultantAPI } from './consultant'
import { courseAPI } from './course'
import { bannerAPI } from './banner'

// 统一导出所有API类和实例
export {
    authAPI,
    assessmentAPI,
    counselorAPI,
    consultantAPI,
    courseAPI,
    bannerAPI
}

// 默认导出所有API的集合
export default {
    auth: authAPI,
    assessment: assessmentAPI,
    counselor: counselorAPI,
    consultant: consultantAPI,
    course: courseAPI,
    banner: bannerAPI
}

