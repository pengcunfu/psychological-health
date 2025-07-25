package com.ruoyi.ur.domain.entity;

import io.swagger.annotations.ApiModel;
import io.swagger.annotations.ApiModelProperty;
import lombok.Data;
import java.util.Date;

@Data
@ApiModel(value = "User", description = "用户信息实体")
public class User {
    @ApiModelProperty("用户ID")
    private String id;
    
    @ApiModelProperty("用户名")
    private String username;
    
    @ApiModelProperty("头像URL")
    private String avatar;
    
    @ApiModelProperty("手机号")
    private String phone;
    
    @ApiModelProperty("邮箱")
    private String email;
    
    @ApiModelProperty("创建时间")
    private Date createTime;
    
    @ApiModelProperty("更新时间")
    private Date updateTime;
}