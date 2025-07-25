package com.ruoyi.ur.domain;

import lombok.Data;

/**
 * 微信用户信息
 */
@Data
public class WxUserInfo {
    /**
     * 用户昵称
     */
    private String nickName;
    
    /**
     * 用户头像
     */
    private String avatarUrl;
    
    /**
     * 性别 0-未知，1-男性，2-女性
     */
    private Integer gender;
    
    /**
     * 用户所在国家
     */
    private String country;
    
    /**
     * 用户所在省份
     */
    private String province;
    
    /**
     * 用户所在城市
     */
    private String city;
    
    /**
     * 显示 country，province，city 所用的语言
     */
    private String language;
} 