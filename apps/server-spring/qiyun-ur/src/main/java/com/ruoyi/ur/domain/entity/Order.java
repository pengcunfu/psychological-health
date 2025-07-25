package com.ruoyi.ur.domain.entity;

import io.swagger.annotations.ApiModel;
import io.swagger.annotations.ApiModelProperty;
import lombok.Data;
import java.util.Date;

@Data
@ApiModel(value = "Order", description = "订单信息实体")
public class Order {
    @ApiModelProperty("订单ID")
    private String id;
    
    @ApiModelProperty("用户ID")
    private String userId;
    
    @ApiModelProperty("商品ID（课程ID或咨询预约ID）")
    private String productId;
    
    @ApiModelProperty("商品类型（1-课程，2-咨询）")
    private Integer type;
    
    @ApiModelProperty("订单金额")
    private Double amount;
    
    @ApiModelProperty("支付状态（0-未支付，1-已支付，2-已退款）")
    private Integer status;
    
    @ApiModelProperty("创建时间")
    private Date createTime;
    
    @ApiModelProperty("更新时间")
    private Date updateTime;
}