package com.ruoyi.ur.domain.dto;

import lombok.Data;

@Data
public class UserDto {
    private String id;
    private String nickname;
    private String email;
    private String avatar;
    private String phone;
    private String gender;
    private Integer age;
    private String bio;
}