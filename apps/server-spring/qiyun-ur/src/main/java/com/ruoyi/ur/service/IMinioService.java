package com.ruoyi.ur.service;

import org.springframework.core.io.Resource;
import org.springframework.http.ResponseEntity;
import org.springframework.web.multipart.MultipartFile;

/**
 * Minio 对象存储服务接口
 */
public interface IMinioService {
    
    /**
     * 上传文件
     *
     * @param file 文件对象
     * @param objectName 对象名称
     * @return 上传后的对象名称
     * @throws Exception 上传异常
     */
    String uploadFile(MultipartFile file, String objectName) throws Exception;

    /**
     * 获取文件预览URL
     *
     * @param objectName 对象名称
     * @return 预览URL
     * @throws Exception 获取异常
     */
    String getPreviewUrl(String objectName) throws Exception;

    /**
     * 视频流处理
     *
     * @param objectName 对象名称
     * @param rangeHeader 范围请求头
     * @return 视频流响应
     * @throws Exception 处理异常
     */
    ResponseEntity<Resource> streamVideo(String objectName, String rangeHeader) throws Exception;
} 