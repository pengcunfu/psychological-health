package com.ruoyi.ur.domain.entity;

import lombok.Data;
import java.util.Date;

@Data
public class Announcement {
    private String id;
    private String counselorId;
    private String serviceId;
    private String userId;
    private String date;
    private String note;
    private String timeSlot;
    private Integer status;
    private Date createTime;
}