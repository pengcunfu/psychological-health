package com.ruoyi.ur.service;

import com.ruoyi.common.core.domain.AjaxResult;
import com.ruoyi.ur.domain.WxLoginRequest;

/**
 * 登录服务接口
 * 提供用户登录相关的服务，包括微信登录、账号密码登录、登出等功能
 *
 * @author ruoyi
 */
public interface ILoginService {
    
    /**
     * 微信小程序登录
     *
     * @param loginRequest 登录请求参数，包含code和用户信息
     * @return 登录结果，包含token和用户信息
     */
    AjaxResult wxLogin(WxLoginRequest loginRequest);
} 