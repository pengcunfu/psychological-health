import request from '../utils/request';

/**
 * 获取咨询师列表
 * @param {Object} params - 查询参数 {page, pageSize, keyword, categoryId, sortBy}
 * @returns {Promise} - 咨询师列表
 */
export function getCounselorList(params) {
  return request({
    url: '/counselor/list',
    method: 'POST',
    data: params
  });
}

/**
 * 获取咨询师详情
 * @param {String} id - 咨询师ID
 * @returns {Promise} - 咨询师详情
 */
export function getCounselorDetail(id) {
  return request({
    url: `/counselor/${id}`,
    method: 'GET'
  });
}

/**
 * 获取咨询师推荐列表
 * @returns {Promise} - 推荐咨询师列表
 */
export function getRecommendedCounselors() {
  return request({
    url: '/counselor/recommended',
    method: 'GET'
  });
}

/**
 * 获取咨询师评价列表
 * @param {Object} params - 查询参数 {targetId, targetType, page, pageSize}
 * @returns {Promise} - 评价列表
 */
export function getCounselorReviews(params) {
  return request({
    url: '/review/list',
    method: 'GET',
    params
  });
}

/**
 * 提交咨询师评价
 * @param {Object} data - 评价数据 {counselorId, content, rating, orderId}
 * @returns {Promise} - 提交结果
 */
export function submitCounselorReview(data) {
  return request({
    url: '/review/submit',
    method: 'POST',
    data
  });
}

/**
 * 获取咨询师可预约时间
 * @param {String} id - 咨询师ID
 * @param {String} date - 日期 YYYY-MM-DD
 * @returns {Promise} - 可预约时间列表
 */
export function getCounselorAvailableSlots(id, date) {
  return request({
    url: `/counselor/available-slots`,
    method: 'GET',
    params: { id, date }
  });
}

/**
 * 申请成为咨询师
 * @param {Object} data - 申请数据
 * @returns {Promise} - 申请结果
 */
export function applyToBeCounselor(data) {
  return request({
    url: '/counselor/apply',
    method: 'POST',
    data
  });
}

export default {
  getCounselorList,
  getCounselorDetail,
  getRecommendedCounselors,
  getCounselorReviews,
  submitCounselorReview,
  getCounselorAvailableSlots,
  applyToBeCounselor
}; 