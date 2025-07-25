package com.ruoyi.ur.controller;

import com.ruoyi.common.annotation.Anonymous;
import com.ruoyi.common.core.domain.AjaxResult;
import com.ruoyi.ur.domain.dto.OrderDetailDto;
import com.ruoyi.ur.service.IOrderService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;

import java.util.Map;


@RestController
@RequestMapping("/orders")
public class OrderController {

    @Autowired
    private IOrderService orderService;

    @GetMapping("/{id}")
    @Anonymous
    public AjaxResult getOrderDetail(@PathVariable String id) {
        OrderDetailDto detail = orderService.getOrderDetailById(id);
        return AjaxResult.success(detail);
    }

    @GetMapping("/appointments")
      @Anonymous
    public AjaxResult getUserAppointments(
            @RequestParam String userId,
            @RequestParam(defaultValue = "0") String status,
            @RequestParam(defaultValue = "1") int page,
            @RequestParam(defaultValue = "10") int pageSize) {
        
        Map<String, Object> result = orderService.getUserAppointments(userId, status, page, pageSize);
        return AjaxResult.success(result);
    }
}