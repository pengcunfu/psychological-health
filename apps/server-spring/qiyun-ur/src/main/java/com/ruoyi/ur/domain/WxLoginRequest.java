package com.ruoyi.ur.domain;

import lombok.Data;

/**
 * 微信登录请求参数
 */
@Data
public class WxLoginRequest {
    /**
     * 微信登录时获取的 code
     */
    private String code;
    
    /**
     * 用户信息
     */
    private WxUserInfo userInfo;
} 