package com.ruoyi.ur.service;

import com.ruoyi.ur.domain.entity.UserFavorite;

import java.util.Map;

/**
 * 用户收藏服务接口
 * 提供用户收藏相关的服务，包括收藏的添加、删除、查询等功能
 *
 * @author ruoyi
 */
public interface IUserFavoriteService {
    
    /**
     * 添加收藏
     *
     * @param userFavorite 收藏信息实体
     * @return 添加成功返回true，否则返回false
     */
    boolean addFavorite(UserFavorite userFavorite);

    /**
     * 移除收藏
     *
     * @param id 收藏记录ID
     * @return 移除成功返回true，否则返回false
     */
    boolean removeFavorite(String id);

    /**
     * 获取用户的咨询师收藏列表
     *
     * @param userId 用户ID
     * @param type 收藏类型
     * @param page 页码
     * @param pageSize 每页数量
     * @return 包含收藏列表和分页信息的Map
     */
    Map<String, Object> getCounselorFavorites(String userId, String type, Integer page, Integer pageSize);

    /**
     * 检查项目是否已被收藏
     *
     * @param userId 用户ID
     * @param itemId 项目ID
     * @param itemType 项目类型
     * @return 已收藏返回true，否则返回false
     */
    boolean isItemFavorited(String userId, String itemId, String itemType);
}