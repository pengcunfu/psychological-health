package com.ruoyi.ur.service;

import com.ruoyi.ur.domain.vo.AnnouncementVo;

import java.util.List;

/**
 * 公告服务接口
 * 提供系统公告相关的服务，包括公告的发布、更新、查询等功能
 *
 * @author ruoyi
 */
public interface IAnnouncementService {

    /**
     * 根据ID获取公告详情
     *
     * @param id 公告ID
     * @return 公告详情VO对象，如果未找到则返回null
     */
    AnnouncementVo getById(String id);

    /**
     * 获取所有公告列表
     *
     * @return 公告列表，如果没有公告则返回空列表
     */
    List<AnnouncementVo> selectList();
}