/**
 * 文件管理API类
 */
class FileApi {
  /**
   * 上传文件
   * @param {File} file - 文件对象
   * @param {String} type - 文件类型 (avatar, certificate, idcard)
   * @returns {Promise} - 上传结果
   */
  static uploadFile(file, type = 'image') {
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
  static previewFile(fileId) {
    return request({
      url: `/file/preview/${fileId}`,
      method: 'GET'
    });
  }
}

// 默认导出
export default {
  FileApi,
};