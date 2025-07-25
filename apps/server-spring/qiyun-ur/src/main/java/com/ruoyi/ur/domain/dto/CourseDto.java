package com.ruoyi.ur.domain.dto;

import lombok.Data;
import java.util.List;

@Data
public class CourseDto {
    private String id;
    private String title;
    private String coverImage;
    private String teacher;
    private Double price;
    private Double originalPrice;
    private Integer lessonCount;
    private Integer studentCount;
    private Double rating;
    private List<String> tags;
    private String description;
}