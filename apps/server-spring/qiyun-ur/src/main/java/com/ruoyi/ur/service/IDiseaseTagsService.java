package com.ruoyi.ur.service;


import com.ruoyi.ur.domain.entity.DiseaseTags;

import java.util.List;

/**
 * 疾病标签服务接口
 * 提供疾病标签相关的服务，包括标签的管理、分类、查询等功能
 *
 * @author ruoyi
 */
public interface IDiseaseTagsService {

    /**
     * 获取所有疾病标签
     *
     * @return 疾病标签列表，如果没有标签则返回空列表
     */
    List<DiseaseTags> getAll();
}
