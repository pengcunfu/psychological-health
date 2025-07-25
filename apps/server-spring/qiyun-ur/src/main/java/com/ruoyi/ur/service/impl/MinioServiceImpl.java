package com.ruoyi.ur.service.impl;

import com.ruoyi.ur.service.IMinioService;
import io.minio.*;
import io.minio.http.Method;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.core.io.InputStreamResource;
import org.springframework.core.io.Resource;
import org.springframework.http.HttpHeaders;
import org.springframework.http.HttpStatus;
import org.springframework.http.MediaType;
import org.springframework.http.ResponseEntity;
import org.springframework.stereotype.Service;
import org.springframework.web.multipart.MultipartFile;

import java.io.InputStream;
import java.util.Arrays;
import java.util.List;

/**
 * Minio 对象存储服务实现类
 */
@Service
public class MinioServiceImpl implements IMinioService {

    @Autowired
    private MinioClient minioClient;
    
    @Value("${minio.bucketName}")
    private String bucketName;

    /**
     * 允许的文件类型
     */
    private static final List<String> ALLOWED_FILE_TYPES = Arrays.asList(
        "image/jpeg", "image/png", "image/gif", 
        "video/mp4", "video/quicktime", "video/x-msvideo",
        "video/x-matroska",
        "application/pdf", "application/msword"
    );

    /**
     * 允许的文件扩展名
     */
    private static final List<String> ALLOWED_EXTENSIONS = Arrays.asList(
        ".jpg", ".jpeg", ".png", ".gif",
        ".mp4", ".mov", ".avi", ".mkv",
        ".pdf", ".doc", ".docx"
    );

    /**
     * 最大文件大小 (1GB)
     */
    private static final long MAX_FILE_SIZE = 1 * 1024 * 1024 * 1024;

    @Override
    public String uploadFile(MultipartFile file, String objectName) throws Exception {
        // 检查存储桶是否存在
        boolean found = minioClient.bucketExists(BucketExistsArgs.builder().bucket(bucketName).build());
        if (!found) {
            minioClient.makeBucket(MakeBucketArgs.builder().bucket(bucketName).build());
        }

        if (file.isEmpty()) {
            throw new RuntimeException("上传文件为空");
        }

        if (file.getSize() > MAX_FILE_SIZE) {
            System.out.println("原始文件名：" + file.getName());
            System.out.println("文件大小：" + file.getSize());
            throw new RuntimeException("文件大小不能超过1GB");
        }

        // 通过扩展名和ContentType双重校验
        String originalFilename = file.getOriginalFilename();
        String extension = originalFilename.substring(originalFilename.lastIndexOf(".")).toLowerCase();
        
        if (!ALLOWED_EXTENSIONS.contains(extension)) {
            throw new RuntimeException("不支持的文件格式: " + extension);
        }

        String contentType = file.getContentType();
        if (!ALLOWED_FILE_TYPES.contains(contentType)) {
            throw new RuntimeException("不支持的文件类型: " + contentType);
        }
        
        try (InputStream inputStream = file.getInputStream()) {
            minioClient.putObject(
                PutObjectArgs.builder()
                    .bucket(bucketName)
                    .object(objectName)
                    .stream(inputStream, file.getSize(), -1)
                    .contentType(file.getContentType())
                    .build());
        } 
        return objectName;
    }

    @Override
    public String getPreviewUrl(String objectName) throws Exception {
        return minioClient.getPresignedObjectUrl(
            GetPresignedObjectUrlArgs.builder()
                .method(Method.GET)
                .bucket(bucketName)
                .object(objectName)
                .build()
        );
    }

    @Override
    public ResponseEntity<Resource> streamVideo(String objectName, String rangeHeader) throws Exception {
        // 获取视频元数据
        ObjectStat stat = minioClient.statObject(bucketName, objectName);
        
        long fileSize = stat.length();
        String contentType = stat.contentType();
        
        // 准备响应头
        HttpHeaders headers = new HttpHeaders();
        headers.setContentType(MediaType.parseMediaType(contentType));
        headers.set("Accept-Ranges", "bytes");
        headers.set("Content-Disposition", "inline");
        
        // 处理范围请求
        long start = 0;
        long end = fileSize - 1;
        
        if (rangeHeader != null && rangeHeader.startsWith("bytes=")) {
            String[] ranges = rangeHeader.substring(6).split("-");
            start = Long.parseLong(ranges[0]);
            end = ranges.length > 1 ? Long.parseLong(ranges[1]) : fileSize - 1;
            headers.set("Content-Range", "bytes " + start + "-" + end + "/" + fileSize);
        }
        
        // 获取视频流
        InputStream stream = minioClient.getObject(
            GetObjectArgs.builder()
                .bucket(bucketName)
                .object(objectName)
                .offset(start)
                .length(end - start + 1)
                .build()
        );
        
        headers.setContentLength(end - start + 1);
        
        return ResponseEntity.status(rangeHeader != null ? HttpStatus.PARTIAL_CONTENT : HttpStatus.OK)
            .headers(headers)
            .body(new InputStreamResource(stream));
    }
} 