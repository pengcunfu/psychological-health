package com.ruoyi.ur.service;

import com.ruoyi.ur.domain.dto.AppointmentRequest;

/**
 * 预约服务接口
 * 提供预约相关的服务，包括预约的创建、修改、取消、查询等功能
 *
 * @author ruoyi
 */
public interface IAppointmentService {
    
    /**
     * 创建新的预约
     *
     * @param request 预约请求对象，包含预约的详细信息
     * @return 创建成功的预约ID
     */
    String createAppointment(AppointmentRequest request);

    /**
     * 取消预约
     *
     * @param id 预约ID
     * @return 取消成功返回true，否则返回false
     */
    boolean cancelAppointment(String id);

    /**
     * 更新预约信息
     *
     * @param id 预约ID
     * @param date 新的预约日期
     * @param timeSlot 新的预约时间段
     * @param note 新的预约备注
     * @return 更新成功返回true，否则返回false
     */
    boolean updateAppointment(String id, String date, String timeSlot, String note);
}