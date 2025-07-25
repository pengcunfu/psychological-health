package com.ruoyi.ur.controller;

import com.ruoyi.common.annotation.Anonymous;
import com.ruoyi.common.core.domain.AjaxResult;
import com.ruoyi.common.utils.uuid.UUID;
import com.ruoyi.ur.service.IMinioService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.core.io.Resource;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.multipart.MultipartFile;

@RestController
@RequestMapping("/file")
public class FileController {
    @Autowired
    private IMinioService minioService;

    @PostMapping(value = "/upload")
    @Anonymous
    public AjaxResult uploadFile(@RequestParam("file") MultipartFile file) {
        try {
            if (file.isEmpty()) {
                return AjaxResult.error("文件为空");
            }
            String objectName = UUID.randomUUID().toString();
            String url = minioService.uploadFile(file, objectName);
            return AjaxResult.success("上传成功", url);

        } catch (RuntimeException e) {

            return AjaxResult.error(e.getMessage());

        } catch (Exception e) {

            return AjaxResult.error("上传失败: " + e.getMessage());

        }
    }

    @GetMapping("/preview/{objectName}")
    @Anonymous
    public AjaxResult getFileUrl(@PathVariable String objectName) {
        try {
            String url = minioService.getPreviewUrl(objectName);
            return AjaxResult.success(url);
        } catch (Exception e) {
            return AjaxResult.error("文件为空");
        }
    }

    @GetMapping("/preview/video/{objectName}")
    @Anonymous
    public ResponseEntity<Resource> previewVideo(
            @PathVariable String objectName,
            @RequestHeader(value = "Range", required = false) String rangeHeader) {
        try {
            return minioService.streamVideo(objectName, rangeHeader);
        } catch (Exception e) {
            return ResponseEntity.status(HttpStatus.NOT_FOUND).build();
        }
    }
}