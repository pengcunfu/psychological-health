package com.ruoyi.ur.controller;

import com.ruoyi.common.annotation.Anonymous;
import com.ruoyi.common.core.controller.BaseController;
import com.ruoyi.common.core.domain.AjaxResult;
import com.ruoyi.ur.service.IAnnouncementService;
import io.swagger.annotations.Api;
import io.swagger.annotations.ApiOperation;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;

/**
 * 公告管理控制器
 * 提供公告的查询等相关接口
 *
 * @author ruoyi
 * @version 1.0
 * @date 2024-04-21
 */
@Api(tags = "公告管理")
@RestController
@RequestMapping("/announcement")
public class AnnouncementsController extends BaseController {

    @Autowired
    private IAnnouncementService announcementService;

    /**
     * 获取指定公告详情
     *
     * @param id 公告ID
     * @return 公告详情信息
     * @apiNote 此接口允许匿名访问
     */
    @ApiOperation("获取公告详情")
    @GetMapping("/{id}")
    @Anonymous
    public AjaxResult getById(@PathVariable String id) {
        return success(announcementService.getById(id));
    }

    /**
     * 获取公告列表
     *
     * @return 公告列表数据
     * @apiNote 此接口允许匿名访问，返回所有有效的公告信息
     */
    @ApiOperation("获取公告列表")
    @GetMapping("/list")
    @Anonymous
    public AjaxResult list() {
        return success(announcementService.selectList());
    }
}