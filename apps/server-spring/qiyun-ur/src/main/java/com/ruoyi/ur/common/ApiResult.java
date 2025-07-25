package com.ruoyi.ur.common;

import lombok.Data;

@Data
public class ApiResult<T> {
    private int code;
    private String message;
    private T data;

    public static <T> ApiResult<T> success(T data) {
        ApiResult<T> result = new ApiResult<>();
        result.setCode(200);
        result.setMessage("success");
        result.setData(data);
        return result;
    }

    public static ApiResult<?> error(String message) {
        ApiResult<Object> result = new ApiResult<>();
        result.setCode(500);
        result.setMessage("fail");
        result.setData(message);
        return result;
    }
}
