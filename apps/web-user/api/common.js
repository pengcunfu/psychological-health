import request from '../utils/request';

/**
 * 获取公告列表
 * @returns {Promise} - 公告列表
 */
export function getAnnouncementList() {
  return request({
    url: '/announcement/list',
    method: 'GET'
  });
}

/**
 * 获取单个公告详情
 * @param {String} id - 公告ID
 * @returns {Promise} - 公告详情
 */
export function getAnnouncementDetail(id) {
  return request({
    url: `/announcement/${id}`,
    method: 'GET'
  });
}

/**
 * 获取功能分类列表
 * @returns {Promise} - 功能列表
 */
export function getDiseaseTags() {
  return request({
    url: '/diseaseTags/list',
    method: 'GET'
  });
}

/**
 * 获取协议内容
 * @param {String} type - 协议类型 (user, privacy)
 * @returns {Promise} - 协议内容
 */
export function getAgreement(type) {
  return request({
    url: '/config/agreement',
    method: 'GET',
    params: { type }
  });
}

/**
 * 上传文件
 * @param {File} file - 文件对象
 * @param {String} type - 文件类型 (avatar, certificate, idcard)
 * @returns {Promise} - 上传结果
 */
export function uploadFile(file, type = 'image') {
  const formData = new FormData();
  formData.append('file', file);
  formData.append('type', type);
  
  return request({
    url: '/file/upload',
    method: 'POST',
    headers: {
      'Content-Type': 'multipart/form-data'
    },
    data: formData
  });
}

/**
 * 预览文件
 * @param {String} fileId - 文件ID
 * @returns {Promise} - 文件URL
 */
export function previewFile(fileId) {
  return request({
    url: `/file/preview/${fileId}`,
    method: 'GET'
  });
}

/**
 * 提交反馈信息
 * @param {Object} data - 反馈数据 {userId, content, contactInfo}
 * @returns {Promise} - 提交结果
 */
export function submitFeedback(data) {
  return request({
    url: '/common/feedback',
    method: 'POST',
    data
  });
}

export default {
  getAnnouncementList,
  getAnnouncementDetail,
  getDiseaseTags,
  getAgreement,
  uploadFile,
  previewFile,
  submitFeedback
}; 