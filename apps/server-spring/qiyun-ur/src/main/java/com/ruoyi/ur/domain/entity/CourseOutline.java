// 课程大纲实体类
package com.ruoyi.ur.domain.entity;

import io.swagger.annotations.ApiModel;
import io.swagger.annotations.ApiModelProperty;
import lombok.Data;
import java.util.Date;

@Data
@ApiModel(value = "CourseOutline", description = "课程大纲实体")
public class CourseOutline {
    @ApiModelProperty("大纲ID")
    private String id;
    
    @ApiModelProperty("课程ID")
    private String courseId;
    
    @ApiModelProperty("章节标题")
    private String title;
    
    @ApiModelProperty("章节内容")
    private String content;
    
    @ApiModelProperty("排序序号")
    private Integer orderNum;
    
    @ApiModelProperty("创建时间")
    private Date createTime;
    
    @ApiModelProperty("更新时间")
    private Date updateTime;
}