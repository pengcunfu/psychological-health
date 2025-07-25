package com.ruoyi.ur.controller;

import com.ruoyi.common.core.domain.AjaxResult;
import com.ruoyi.ur.domain.WxLoginRequest;
import com.ruoyi.ur.service.ILoginService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

/**
 * 登录接口控制器
 */
@RestController
@RequestMapping("/wx")
public class LoginController {

    @Autowired
    private ILoginService loginService;

    /**
     * 微信小程序登录
     */
    @PostMapping("/login")
    public AjaxResult login(@RequestBody WxLoginRequest loginRequest) {
        return loginService.wxLogin(loginRequest);
    }
}
