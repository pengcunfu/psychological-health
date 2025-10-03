import api from '@/utils/api'

// 课程管理API
export const courseAPI = {
    // 获取课程列表
    getCourses: (params) => api.get('/course', { params }),

    // 获取课程详情
    getCourse: (id) => api.get(`/course/${id}`),

    // 创建课程
    createCourse: (data) => api.post('/course', data),

    // 更新课程
    updateCourse: (id, data) => api.put(`/course/${id}`, data),

    // 删除课程
    deleteCourse: (id) => api.delete(`/course/${id}`),

    // 上传课程封面
    uploadCover: (id, formData) => api.post(`/course/${id}/cover`, formData, {
        headers: {
            'Content-Type': 'multipart/form-data'
        }
    }),

    // 获取课程评价
    getCourseReviews: (id, params) => api.get(`/course/${id}/reviews`, { params }),

    // 获取课程章节
    getCourseChapters: (id) => api.get(`/course/${id}/chapters`)
}

// 课程大纲管理API
export const courseOutlineAPI = {
    // 获取课程大纲列表
    getCourseOutlines: (params) => api.get('/course-outline', { params }),

    // 获取课程大纲详情
    getCourseOutline: (id) => api.get(`/course-outline/${id}`),

    // 创建课程大纲
    createCourseOutline: (data) => api.post('/course-outline', data),

    // 更新课程大纲
    updateCourseOutline: (id, data) => api.put(`/course-outline/${id}`, data),

    // 删除课程大纲
    deleteCourseOutline: (id) => api.delete(`/course-outline/${id}`),

    // 获取课程列表（用于下拉选择）
    getCourses: (params) => api.get('/course-outline/courses', { params })
}

// 导出单独的课程API函数，以便在其他组件中直接使用
export const getCourses = (params) => courseAPI.getCourses(params)
export const getCourse = (id) => courseAPI.getCourse(id)
export const createCourse = (data) => courseAPI.createCourse(data)
export const updateCourse = (id, data) => courseAPI.updateCourse(id, data)
export const deleteCourse = (id) => courseAPI.deleteCourse(id)

// 课程大纲管理接口（保持向后兼容）
export const getCourseOutlines = (params) => api.get('/course-outline', { params })
export const getCourseOutline = (id) => api.get(`/course-outline/${id}`)
export const createCourseOutline = (data) => api.post('/course-outline', data)
export const updateCourseOutline = (id, data) => api.put(`/course-outline/${id}`, data)
export const deleteCourseOutline = (id) => api.delete(`/course-outline/${id}`)

export default { courseAPI, courseOutlineAPI }
