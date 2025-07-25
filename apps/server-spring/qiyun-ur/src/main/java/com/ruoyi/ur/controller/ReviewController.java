package com.ruoyi.ur.controller;

import com.github.pagehelper.PageInfo;
import com.ruoyi.common.annotation.Anonymous;
import com.ruoyi.common.core.domain.AjaxResult;
import com.ruoyi.ur.domain.dto.CounselorReviewDto;
import com.ruoyi.ur.domain.dto.ReviewDto;
import com.ruoyi.ur.service.IReviewService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("/review")
public class ReviewController {

    @Autowired
    private IReviewService IReviewService;

    @PostMapping("/submit")
    @Anonymous
    public AjaxResult submitReview(@RequestBody ReviewDto reviewDto) {
        return AjaxResult.success(IReviewService.submitReview(reviewDto));
    }

    @GetMapping("/list")
    @Anonymous
    public AjaxResult getReviews(
            @RequestParam String targetId,
            @RequestParam String targetType,
            @RequestParam(defaultValue = "1") Integer page,
            @RequestParam(defaultValue = "10") Integer pageSize) {
        
        PageInfo<CounselorReviewDto> pageInfo = IReviewService.getReviews(targetId, targetType, page, pageSize);
        return AjaxResult.success(pageInfo);
    }
}