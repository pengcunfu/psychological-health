package com.ruoyi.ur.domain.dto;

import lombok.Data;
import java.util.List;

@Data
public class CourseDetailDto {
    private String id;
    private String title;
    private String coverImage;
    private String teacher;
    private String teacherTitle;
    private String teacherAvatar;
    private Double price;
    private Double originalPrice;
    private Integer lessonCount;
    private Integer studentCount;
    private Double rating;
    private List<String> tags;
    private String description;
    private List<CourseOutlineDto> outline;
}
@Data
class CourseLessonDto {
    private String id;
    private String title;
    private String duration;
    private Boolean isFree;
}

@Data
class CourseOutlineDto {
    private String title;
    private List<CourseLessonDto> lessons;
}
