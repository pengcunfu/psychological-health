package com.ruoyi.ur.service.impl;

import com.ruoyi.ur.domain.dto.UserDto;
import com.ruoyi.ur.domain.dto.UserUpdateDto;
import com.ruoyi.ur.mapper.UserMapper;
import com.ruoyi.ur.service.IUserService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

@Service
public class IUserServiceImpl implements IUserService {

    @Autowired
    private UserMapper userMapper;

    @Override
    public UserDto getUserById(String id) {
        return userMapper.selectUserById(id);
    }

    @Override
    public int updateUserInfo(String id, UserUpdateDto dto) {
        return userMapper.updateUserInfo(id, dto);
    }
}