// 用户收藏实体类
package com.ruoyi.ur.domain.entity;

import lombok.Data;
import java.util.Date;

@Data
public class UserFavorite {
    private String id;
    private String userId;
    private String itemId;
    private String itemType;
    private Date createTime;
}