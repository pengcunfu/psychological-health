package com.ruoyi.ur.domain.dto;

import lombok.Data;

import java.util.List;

@Data
public class CounselorDetailRequest {
    private String id;
    private String name;
    private String avatar;
    private String title;
    private Boolean isVerified;
    private List<String> tags;
    private Integer price;
    private Double rating;
    private Integer sessionCount;
    private String introduction;
    private String education;
    private String experience;
    private List<String> certificates;
    private List<String> services;
    private List<String> availability;
    private List<CounselorReviewDto> reviews;
}