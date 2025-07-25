package com.ruoyi.ur.domain.entity;

import io.swagger.annotations.ApiModel;
import io.swagger.annotations.ApiModelProperty;
import lombok.Data;
import java.util.Date;
import java.util.List;

@Data
@ApiModel(value = "Counselor", description = "咨询师信息实体")
public class Counselor {
    @ApiModelProperty("咨询师ID")
    private String id;
    
    @ApiModelProperty("咨询师姓名")
    private String name;
    
    @ApiModelProperty("头像URL")
    private String avatar;
    
    @ApiModelProperty("职称")
    private String title;
    
    @ApiModelProperty("专业领域标签")
    private List<String> tags;
    
    @ApiModelProperty("咨询价格（每小时）")
    private Double price;
    
    @ApiModelProperty("评分")
    private Double rating;
    
    @ApiModelProperty("咨询次数")
    private Integer consultationCount;
    
    @ApiModelProperty("简介")
    private String introduction;
    
    @ApiModelProperty("创建时间")
    private Date createTime;
    
    @ApiModelProperty("更新时间")
    private Date updateTime;
}