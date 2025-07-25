package com.ruoyi.ur.domain.dto;

import lombok.Data;

@Data
public class UserAppointmentDto {
    private String id;
    private String orderNo;
    private String type;
    private String title;
    private String providerName;
    private String providerTitle;
    private String appointmentTime;
    private String paymenTime;
    private Double price;
    private String status;
    private String createTime;
}