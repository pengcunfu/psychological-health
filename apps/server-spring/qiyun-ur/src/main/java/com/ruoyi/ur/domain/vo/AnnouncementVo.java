// 公告实体类
package com.ruoyi.ur.domain.vo;

import lombok.Data;

import java.util.Date;

@Data
public class AnnouncementVo {
    private String id;
    private String content;
    private Date publishTime;
}