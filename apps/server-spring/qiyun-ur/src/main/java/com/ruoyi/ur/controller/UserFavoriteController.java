package com.ruoyi.ur.controller;

import com.ruoyi.common.annotation.Anonymous;
import com.ruoyi.common.core.domain.AjaxResult;
import com.ruoyi.ur.domain.entity.UserFavorite;
import com.ruoyi.ur.service.IUserFavoriteService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;

import java.util.Map;

@RestController
@RequestMapping("/favorites")
public class UserFavoriteController {

    @Autowired
    private IUserFavoriteService IUserFavoriteService;

    @PostMapping
    @Anonymous
    public AjaxResult addFavorite(@RequestBody UserFavorite userFavorite) {
        return IUserFavoriteService.addFavorite(userFavorite)
            ? AjaxResult.success() : AjaxResult.error("收藏失败");
    }

    @DeleteMapping("/{id}")
    @Anonymous
    public AjaxResult removeFavorite(@PathVariable String id) {
        return IUserFavoriteService.removeFavorite(id)
            ? AjaxResult.success() : AjaxResult.error("取消收藏失败");
    }



    @GetMapping("/check")
    @Anonymous
    public AjaxResult isItemFavorited(
            @RequestParam String userId,
            @RequestParam String itemId,
            @RequestParam String itemType) {
        boolean isFavorited = IUserFavoriteService.isItemFavorited(userId, itemId, itemType);
        return AjaxResult.success(isFavorited);
    }

    @GetMapping("/counselors")
    public AjaxResult getCounselorFavorites(
        @RequestParam String userId,
        @RequestParam(defaultValue = "counselor") String type,
        @RequestParam(defaultValue = "1") Integer page,
        @RequestParam(defaultValue = "10") Integer pageSize) {
        
        Map<String, Object> result = IUserFavoriteService.getCounselorFavorites(userId,type ,page, pageSize);
        return AjaxResult.success(result);
    }
}