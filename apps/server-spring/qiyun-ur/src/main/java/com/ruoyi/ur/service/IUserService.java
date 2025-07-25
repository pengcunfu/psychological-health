package com.ruoyi.ur.service;

import com.ruoyi.ur.domain.dto.UserDto;
import com.ruoyi.ur.domain.dto.UserUpdateDto;

/**
 * 用户服务接口
 * 提供用户相关的基础服务，包括用户信息的增删改查等操作
 *
 * @author ruoyi
 */
public interface IUserService {
    
    /**
     * 根据ID获取用户信息
     *
     * @param id 用户ID
     * @return 用户信息DTO对象，如果未找到则返回null
     */
    UserDto getUserById(String id);

    /**
     * 更新用户信息
     *
     * @param id 用户ID
     * @param dto 用户信息更新DTO对象
     * @return 更新成功返回1，否则返回0
     */
    int updateUserInfo(String id, UserUpdateDto dto);
}