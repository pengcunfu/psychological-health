package com.ruoyi.ur.domain.dto;

import lombok.Data;
import java.util.Date;

@Data
public class OrderDetailDto {
    private String id;
    private String orderNo;
    private String type;
    private String title;
    private String providerName;
    private String providerTitle;
    private String providerAvatar;
    private String serviceInfo;
    private String appointmentTime;
    private Double price;
    private Double discount;
    private Double actualPaid;
    private String paymentMethod;
    private Date paymentTime;
    private String status;
    private Date createTime;
    private String note;
}