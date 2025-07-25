package com.ruoyi.ur.mapper;

import com.ruoyi.ur.domain.dto.UserDto;
import com.ruoyi.ur.domain.dto.UserUpdateDto;
import org.apache.ibatis.annotations.Param;

public interface UserMapper {
    UserDto selectUserById(@Param("id") String id);

    int updateUserInfo(@Param("id") String id, @Param("dto") UserUpdateDto dto);
}