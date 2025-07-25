package com.ruoyi.ur.controller;

import com.ruoyi.common.annotation.Anonymous;
import com.ruoyi.common.core.domain.AjaxResult;
import com.ruoyi.ur.domain.dto.AppointmentRequest;
import com.ruoyi.ur.service.IAppointmentService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;

/**
 * 预约管理控制器
 * 提供预约的创建、取消、修改等功能
 *
 * @author ruoyi
 * @version 1.0
 * @date 2024-04-21
 */
@RestController
@RequestMapping("/appointment")
public class AppointmentController {

    @Autowired
    private IAppointmentService IAppointmentService;

    /**
     * 创建预约
     *
     * @param request 预约请求对象，包含预约的详细信息
     * @return 预约订单ID
     * @apiNote 此接口允许匿名访问
     *          成功返回预约订单ID
     *          失败返回错误信息
     */
    @PostMapping("/create")
    @Anonymous
    public AjaxResult createAppointment(@RequestBody AppointmentRequest request) {
        String orderId = IAppointmentService.createAppointment(request);
        return AjaxResult.success(orderId);
    }

    /**
     * 取消预约
     *
     * @param id 预约ID
     * @return 操作结果
     * @apiNote 此接口允许匿名访问
     *          成功返回success
     *          失败返回error及错误信息
     */
    @PutMapping("/cancel/{id}")
    @Anonymous
    public AjaxResult cancelAppointment(@PathVariable String id) {
        boolean success = IAppointmentService.cancelAppointment(id);
        return success ? AjaxResult.success() : AjaxResult.error("取消预约失败");
    }

    /**
     * 更新预约信息
     *
     * @param id       预约ID
     * @param date     预约日期（可选）
     * @param timeSlot 预约时间段（可选）
     * @param note     预约备注（可选）
     * @return 操作结果
     * @apiNote 此接口允许匿名访问
     *          所有参数除id外都是可选的，只更新提供的字段
     *          成功返回success
     *          失败返回error及错误信息
     */
    @PutMapping("/update/{id}")
    @Anonymous
    public AjaxResult updateAppointment(
        @PathVariable String id,
        @RequestParam(required = false) String date,
        @RequestParam(required = false) String timeSlot,
        @RequestParam(required = false) String note) {
        
        boolean success = IAppointmentService.updateAppointment(id, date, timeSlot, note);
        return success ? AjaxResult.success() : AjaxResult.error("修改预约失败");
    }
}