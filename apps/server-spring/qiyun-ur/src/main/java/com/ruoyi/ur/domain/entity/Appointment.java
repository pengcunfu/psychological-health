package com.ruoyi.ur.domain.entity;

import io.swagger.annotations.ApiModel;
import io.swagger.annotations.ApiModelProperty;
import lombok.Data;
import java.util.Date;

@Data
@ApiModel(value = "Appointment", description = "咨询预约实体")
public class Appointment {
    @ApiModelProperty("预约ID")
    private String id;
    
    @ApiModelProperty("用户ID")
    private String userId;
    
    @ApiModelProperty("咨询师ID")
    private String counselorId;
    
    @ApiModelProperty("预约时间")
    private Date appointmentTime;
    
    @ApiModelProperty("预约状态（0-待确认，1-已确认，2-已完成，3-已取消）")
    private Integer status;
    
    @ApiModelProperty("创建时间")
    private Date createTime;
    
    @ApiModelProperty("更新时间")
    private Date updateTime;
}