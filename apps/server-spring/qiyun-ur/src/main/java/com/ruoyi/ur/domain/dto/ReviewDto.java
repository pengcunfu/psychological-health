package com.ruoyi.ur.domain.dto;

import lombok.Data;

@Data
public class ReviewDto {
    private String counselorId;
    private String orderId;
    private String content;
    private Integer rating;
}