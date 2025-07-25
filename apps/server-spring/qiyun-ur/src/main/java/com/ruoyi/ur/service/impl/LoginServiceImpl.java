package com.ruoyi.ur.service.impl;

import com.ruoyi.common.core.domain.AjaxResult;
import com.ruoyi.ur.domain.WxLoginRequest;
import com.ruoyi.ur.service.ILoginService;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.http.ResponseEntity;
import org.springframework.stereotype.Service;
import org.springframework.web.client.RestTemplate;

import java.util.HashMap;
import java.util.Map;

/**
 * 微信登录服务实现类
 */
@Slf4j
@Service
public class LoginServiceImpl implements ILoginService {

    @Value("${wx.miniapp.appid}")
    private String appid;

    @Value("${wx.miniapp.secret}")
    private String secret;

    @Value("${wx.miniapp.code2session-url}")
    private String code2sessionUrl;

    @Autowired
    private RestTemplate restTemplate;

    @Override
    public AjaxResult wxLogin(WxLoginRequest loginRequest) {
        try {
            // 1. 获取openid和session_key
            String url = String.format("%s?appid=%s&secret=%s&js_code=%s&grant_type=authorization_code",
                    code2sessionUrl, appid, secret, loginRequest.getCode());

            ResponseEntity<Map> response = restTemplate.getForEntity(url, Map.class);
            Map<String, Object> result = response.getBody();

            if (result == null || result.containsKey("errcode")) {
                log.error("微信登录失败: {}", result);
                return AjaxResult.error("微信登录失败: " + result.get("errmsg"));
            }

            String openid = (String) result.get("openid");
            String sessionKey = (String) result.get("session_key");

            // 2. 检查用户是否已注册，未注册则自动注册
            // TODO: 实现用户注册逻辑

            // 3. 生成JWT token
            Map<String, Object> claims = new HashMap<>();
            claims.put("openid", openid);
            // TODO: 添加其他需要的用户信息到claims中

            // 4. 返回token和用户信息
            Map<String, Object> data = new HashMap<>();
            data.put("token", generateToken(claims));  // TODO: 实现generateToken方法
            data.put("userInfo", loginRequest.getUserInfo());

            return AjaxResult.success("登录成功", data);

        } catch (Exception e) {
            log.error("微信登录异常", e);
            return AjaxResult.error("登录失败：" + e.getMessage());
        }
    }

    /**
     * 生成JWT Token
     * @param claims Token中要包含的数据
     * @return JWT Token字符串
     */
    private String generateToken(Map<String, Object> claims) {
        // TODO: 实现JWT Token生成逻辑
        return "test_token";
    }
}
