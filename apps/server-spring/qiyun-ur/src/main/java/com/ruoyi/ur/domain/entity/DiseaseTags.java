package com.ruoyi.ur.domain.entity;

import io.swagger.annotations.ApiModel;
import io.swagger.annotations.ApiModelProperty;
import lombok.Data;
import java.util.Date;

@Data
@ApiModel(value = "DiseaseTags", description = "疾病标签实体")
public class DiseaseTags {
    @ApiModelProperty("标签ID")
    private String id;
    
    @ApiModelProperty("标签名称")
    private String name;
    
    @ApiModelProperty("标签描述")
    private String description;
    
    @ApiModelProperty("创建时间")
    private Date createTime;
    
    @ApiModelProperty("更新时间")
    private Date updateTime;
}
