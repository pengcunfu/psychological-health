package com.ruoyi.ur.domain.vo;

import com.fasterxml.jackson.annotation.JsonInclude;
import lombok.Data;

import java.util.List;

@Data
@JsonInclude(JsonInclude.Include.NON_EMPTY)
public class CounselorVo {
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
}
