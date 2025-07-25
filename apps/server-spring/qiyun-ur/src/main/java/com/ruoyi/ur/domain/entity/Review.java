package com.ruoyi.ur.domain.entity;

import lombok.Data;
import java.util.Date;

@Data
public class Review {
    private String reviewId;
    private String counselorId;
    private String orderId;
    private String content;
    private Integer rating;
    private Date createTime;
}