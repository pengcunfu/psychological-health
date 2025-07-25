import request from '../utils/request';

/**
 * 获取课程列表
 * @param {Object} params - 查询参数 {page, pageSize, keyword, categoryId, sortBy}
 * @returns {Promise} - 课程列表
 */
export function getCourseList(params) {
  return request({
    url: '/courses',
    method: 'GET',
    params
  });
}

/**
 * 获取课程详情
 * @param {String} id - 课程ID
 * @returns {Promise} - 课程详情
 */
export function getCourseDetail(id) {
  return request({
    url: `/courses/detail/${id}`,
    method: 'GET'
  });
}

/**
 * 获取用户已购买的课程
 * @param {String} userId - 用户ID
 * @param {Object} params - 查询参数 {page, pageSize}
 * @returns {Promise} - 已购买课程列表
 */
export function getUserCourses(userId, params = {}) {
  return request({
    url: '/course/my-courses',
    method: 'GET',
    params: { ...params, userId }
  });
}

/**
 * 购买课程
 * @param {Object} data - 购买数据 {courseId, userId}
 * @returns {Promise} - 购买结果
 */
export function purchaseCourse(data) {
  return request({
    url: '/course/purchase',
    method: 'POST',
    data
  });
}

/**
 * 获取课程评价列表
 * @param {Object} params - 查询参数 {targetId, targetType, page, pageSize}
 * @returns {Promise} - 评价列表
 */
export function getCourseReviews(params) {
  return request({
    url: '/review/list',
    method: 'GET',
    params: { ...params, targetType: 'course' }
  });
}

/**
 * 提交课程评价
 * @param {Object} data - 评价数据 {courseId, content, rating, orderId}
 * @returns {Promise} - 提交结果
 */
export function submitCourseReview(data) {
  return request({
    url: '/review/submit',
    method: 'POST',
    data: { ...data, targetType: 'course' }
  });
}

export default {
  getCourseList,
  getCourseDetail,
  getUserCourses,
  purchaseCourse,
  getCourseReviews,
  submitCourseReview
}; 