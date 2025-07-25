package com.ruoyi.ur.domain.dto;

import lombok.Data;

/**
 * 预约请求数据传输对象
 * 用于创建或更新预约时传递预约相关信息
 */
@Data
public class AppointmentRequest {
    /**
     * 咨询师ID
     * 标识被预约的咨询师
     */
    private String counselorId;

    /**
     * 服务项目ID
     * 标识预约的具体服务项目
     */
    private String serviceId;

    /**
     * 用户ID
     * 标识发起预约的用户
     */
    private String userId;

    /**
     * 预约日期
     * 格式：yyyy-MM-dd
     */
    private String date;

    /**
     * 预约时间段
     * 例如："09:00-10:00"、"14:30-15:30"
     */
    private String timeSlot;

    /**
     * 预约备注
     * 用户可以添加额外的预约说明或要求
     */
    private String note;
}