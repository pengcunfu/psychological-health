package com.ruoyi.ur.service.impl;

import com.ruoyi.ur.domain.entity.UserFavorite;
import com.ruoyi.ur.mapper.UserFavoriteMapper;
import com.ruoyi.ur.service.IUserFavoriteService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.Collections;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.stream.Collectors;

@Service
public class IUserFavoriteServiceImpl implements IUserFavoriteService {

    @Autowired
    private UserFavoriteMapper userFavoriteMapper;

    @Override
    public boolean addFavorite(UserFavorite userFavorite) {
        if (isItemFavorited(userFavorite.getUserId(), userFavorite.getItemId(), userFavorite.getItemType())) {
            throw new RuntimeException("该内容已收藏，请勿重复操作");
        }

        userFavorite.setId("f" + System.currentTimeMillis());
        return userFavoriteMapper.insert(userFavorite) > 0;
    }

    @Override
    public boolean removeFavorite(String id) {
        return userFavoriteMapper.deleteById(id) > 0;
    }

    @Override
    public boolean isItemFavorited(String userId, String itemId, String itemType) {
        return userFavoriteMapper.selectByUserAndItem(userId, itemId, itemType) != null;
    }

    @Override
    public Map<String, Object> getCounselorFavorites(String userId, String type, Integer page, Integer pageSize) {
        // 查询收藏记录
        List<UserFavorite> favorites = userFavoriteMapper.selectByUserIdAndType(
                userId, type, (page - 1) * pageSize, pageSize);

        // 查询总数
        long total = userFavoriteMapper.countByUserIdAndType(userId, type);

        // 获取收藏项ID列表
        List<String> itemIds = favorites.stream()
                .map(UserFavorite::getItemId)
                .collect(Collectors.toList());

        List<Map<String, Object>> items;
        if ("counselor".equals(type)) {
            // 查询咨询师详情
            items = userFavoriteMapper.selectCounselorsByIds(itemIds);
        } else if ("course".equals(type)) {
            // 查询课程详情
            items = userFavoriteMapper.selectCoursesByIds(itemIds);
        } else {
            items = Collections.emptyList();
        }

        // 组装返回结果
        Map<String, Object> result = new HashMap<>();
        result.put("total", total);
        result.put("list", items);
        return result;
    }
}