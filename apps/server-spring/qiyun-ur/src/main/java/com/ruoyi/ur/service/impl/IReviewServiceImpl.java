package com.ruoyi.ur.service.impl;

import com.github.pagehelper.PageHelper;
import com.github.pagehelper.PageInfo;
import com.ruoyi.ur.domain.dto.CounselorReviewDto;
import com.ruoyi.ur.domain.dto.ReviewDto;
import com.ruoyi.ur.domain.entity.Review;
import com.ruoyi.ur.mapper.ReviewMapper;
import com.ruoyi.ur.service.IReviewService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.Date;
import java.util.List;

@Service
public class IReviewServiceImpl implements IReviewService {

    @Autowired
    private ReviewMapper reviewMapper;

    // 提交评价
    @Override
    public String submitReview(ReviewDto reviewDto) {
        // 检查是否已评价过
        Review existingReview = reviewMapper.selectByOrderId(reviewDto.getOrderId());
        
        Review review = new Review();
        review.setCounselorId(reviewDto.getCounselorId());
        review.setOrderId(reviewDto.getOrderId());
        review.setContent(reviewDto.getContent());
        review.setRating(reviewDto.getRating());
        review.setCreateTime(new Date());

        if(existingReview != null) {
            // 更新评价
            review.setReviewId(existingReview.getReviewId());
            reviewMapper.update(review);
        } else {
            // 新增评价
            review.setReviewId("r" + System.currentTimeMillis());
            reviewMapper.insert(review);
        }
        
        return review.getReviewId();
    }

    // 获取全部评价
    @Override
    public PageInfo<CounselorReviewDto> getReviews(String targetId, String targetType, Integer page, Integer pageSize) {
        PageHelper.startPage(page, pageSize);
        List<CounselorReviewDto> list = reviewMapper.selectReviews(targetId, targetType);
        return new PageInfo<>(list);
    }
}