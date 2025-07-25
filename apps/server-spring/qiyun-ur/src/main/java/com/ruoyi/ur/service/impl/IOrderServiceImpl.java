package com.ruoyi.ur.service.impl;

import com.ruoyi.ur.domain.dto.OrderDetailDto;
import com.ruoyi.ur.domain.dto.UserAppointmentDto;
import com.ruoyi.ur.mapper.OrderMapper;
import com.ruoyi.ur.service.IOrderService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.HashMap;
import java.util.List;
import java.util.Map;

@Service
public class IOrderServiceImpl implements IOrderService {

    @Autowired
    private OrderMapper orderMapper;

    @Override
    public OrderDetailDto getOrderDetailById(String id) {
        return orderMapper.selectOrderDetailById(id);
    }

    public Map<String, Object> getUserAppointments(String userId, String status, int page, int pageSize) {
        List<UserAppointmentDto> list = orderMapper.selectUserAppointments(
            userId, status, (page - 1) * pageSize, pageSize);
        int total = orderMapper.countUserAppointments(userId, status);
        
        Map<String, Object> result = new HashMap<>();
        result.put("total", total);
        result.put("list", list);
        return result;
    }
}