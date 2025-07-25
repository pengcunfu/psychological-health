package com.ruoyi.ur.mapper;

import com.ruoyi.ur.domain.dto.CounselorReviewDto;
import com.ruoyi.ur.domain.entity.Review;
import org.apache.ibatis.annotations.Mapper;
import org.apache.ibatis.annotations.Param;

import java.util.List;

@Mapper
public interface ReviewMapper {
    int insert(Review review);

    int update(Review review);

    Review selectByOrderId(String orderId);

    List<CounselorReviewDto> selectReviews(@Param("targetId") String targetId,
                                           @Param("targetType") String targetType);
}