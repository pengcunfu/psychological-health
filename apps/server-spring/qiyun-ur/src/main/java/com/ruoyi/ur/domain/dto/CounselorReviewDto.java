package com.ruoyi.ur.domain.dto;

import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

@Data
@AllArgsConstructor
@NoArgsConstructor
public class CounselorReviewDto {
    private String id;
    private String user;
    private String content;
    private Integer rating;
    private String time;
}
