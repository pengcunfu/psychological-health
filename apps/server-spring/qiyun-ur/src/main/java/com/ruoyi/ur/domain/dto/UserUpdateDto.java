package com.ruoyi.ur.domain.dto;

import lombok.Data;

@Data
public class UserUpdateDto {
    private String nickname;
    private String avatar;
    private String email;
    private String gender;
    private Integer age;
    private String bio;
}