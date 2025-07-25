package com.ruoyi.ur.service;

import com.github.pagehelper.PageInfo;
import com.ruoyi.ur.domain.dto.CounselorReviewDto;
import com.ruoyi.ur.domain.dto.ReviewDto;

/**
 * 评价服务接口
 * 提供用户评价相关的服务，包括评价的创建、查询、统计等功能
 *
 * @author ruoyi
 */
public interface IReviewService {
    
    /**
     * 提交评价
     *
     * @param reviewDto 评价信息DTO对象
     * @return 创建成功的评价ID
     */
    String submitReview(ReviewDto reviewDto);

    /**
     * 获取评价列表
     *
     * @param targetId 评价目标ID（如咨询师ID、课程ID等）
     * @param targetType 评价目标类型（如"counselor"、"course"等）
     * @param page 页码
     * @param pageSize 每页数量
     * @return 分页的评价信息列表
     */
    PageInfo<CounselorReviewDto> getReviews(String targetId, String targetType, Integer page, Integer pageSize);
}