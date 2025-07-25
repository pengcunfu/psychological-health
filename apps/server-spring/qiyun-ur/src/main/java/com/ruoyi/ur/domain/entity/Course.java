package com.ruoyi.ur.domain.entity;

import io.swagger.annotations.ApiModel;
import io.swagger.annotations.ApiModelProperty;
import lombok.Data;
import java.util.Date;
import java.util.List;

@Data
@ApiModel(value = "Course", description = "课程信息实体")
public class Course {
    @ApiModelProperty("课程ID")
    private String id;
    
    @ApiModelProperty("课程标题")
    private String title;
    
    @ApiModelProperty("课程封面图片URL")
    private String coverImage;
    
    @ApiModelProperty("教师姓名")
    private String teacher;
    
    @ApiModelProperty("教师职称")
    private String teacherTitle;
    
    @ApiModelProperty("教师头像URL")
    private String teacherAvatar;
    
    @ApiModelProperty("课程现价")
    private Double price;
    
    @ApiModelProperty("课程原价")
    private Double originalPrice;
    
    @ApiModelProperty("课时数量")
    private Integer lessonCount;
    
    @ApiModelProperty("学生数量")
    private Integer studentCount;
    
    @ApiModelProperty("课程评分")
    private Double rating;
    
    @ApiModelProperty("课程标签列表")
    private List<String> tags;
    
    @ApiModelProperty("课程描述")
    private String description;
    
    @ApiModelProperty("创建时间")
    private Date createTime;
    
    @ApiModelProperty("更新时间")
    private Date updateTime;
}