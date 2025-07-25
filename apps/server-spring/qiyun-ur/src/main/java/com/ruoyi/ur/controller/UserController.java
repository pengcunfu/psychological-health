package com.ruoyi.ur.controller;

import com.ruoyi.common.annotation.Anonymous;
import com.ruoyi.common.core.domain.AjaxResult;
import com.ruoyi.ur.domain.dto.UserDto;
import com.ruoyi.ur.domain.dto.UserUpdateDto;
import com.ruoyi.ur.service.IUserService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("/user")
public class UserController {

    @Autowired
    private IUserService userService;

    @GetMapping("/{id}")
    @Anonymous
    public AjaxResult getUserById(@PathVariable String id) {
        UserDto user = userService.getUserById(id);
        return AjaxResult.success(user);
    }

    @PutMapping("/{id}")
    public AjaxResult updateUserInfo(@PathVariable String id, @RequestBody UserUpdateDto dto) {
        int result = userService.updateUserInfo(id, dto);
        return result > 0 ? AjaxResult.success() : AjaxResult.error("更新失败");
    }
}