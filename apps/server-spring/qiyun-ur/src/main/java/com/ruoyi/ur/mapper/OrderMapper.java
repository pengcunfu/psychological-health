package com.ruoyi.ur.mapper;

import com.ruoyi.ur.domain.dto.OrderDetailDto;
import com.ruoyi.ur.domain.dto.UserAppointmentDto;
import com.ruoyi.ur.domain.entity.Order;
import org.apache.ibatis.annotations.Mapper;
import org.apache.ibatis.annotations.Param;

import java.util.List;

@Mapper
public interface OrderMapper {
    OrderDetailDto selectOrderDetailById(@Param("id") String id);

    List<UserAppointmentDto> selectUserAppointments(
            @Param("userId") String userId,
            @Param("status") String status,
            @Param("offset") int offset,
            @Param("pageSize") int pageSize);

    int countUserAppointments(
            @Param("userId") String userId,
            @Param("status") String status);
}