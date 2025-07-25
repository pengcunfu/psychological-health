package com.ruoyi.ur.service;

import com.ruoyi.ur.domain.dto.OrderDetailDto;

import java.util.Map;

/**
 * 订单服务接口
 * 提供订单相关的服务，包括订单的创建、支付、查询、取消等功能
 *
 * @author ruoyi
 */
public interface IOrderService {
    
    /**
     * 根据ID获取订单详情
     *
     * @param id 订单ID
     * @return 订单详细信息DTO对象
     */
    OrderDetailDto getOrderDetailById(String id);
    
    /**
     * 获取用户的预约订单列表
     *
     * @param userId 用户ID
     * @param status 订单状态
     * @param page 页码
     * @param pageSize 每页数量
     * @return 包含预约订单列表和分页信息的Map
     */
    Map<String, Object> getUserAppointments(String userId, String status, int page, int pageSize);
}