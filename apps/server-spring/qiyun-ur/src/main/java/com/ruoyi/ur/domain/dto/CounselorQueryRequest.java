package com.ruoyi.ur.domain.dto;

import lombok.Data;

@Data
public class CounselorQueryRequest {
    private Integer page;
    private Integer pageSize;
    private String keyword;
    private String categoryId;
    private String sortBy;
}
