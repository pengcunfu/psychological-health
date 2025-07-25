package com.ruoyi.ur.mapper;

import com.ruoyi.ur.domain.entity.UserFavorite;
import org.apache.ibatis.annotations.Mapper;
import org.apache.ibatis.annotations.Param;

import java.util.List;
import java.util.Map;

@Mapper
public interface UserFavoriteMapper {
    int insert(UserFavorite userFavorite);

    int deleteById(String id);

    UserFavorite selectByUserAndItem(@Param("userId") String userId,
                                     @Param("itemId") String itemId,
                                     @Param("itemType") String itemType);

    List<UserFavorite> selectByUserIdAndType(
            @Param("userId") String userId,
            @Param("type") String type,
            @Param("offset") int offset,
            @Param("pageSize") int pageSize);

    long countByUserIdAndType(
            @Param("userId") String userId,
            @Param("type") String type);

    List<Map<String, Object>> selectCounselorsByIds(@Param("ids") List<String> ids);

    List<Map<String, Object>> selectCoursesByIds(@Param("ids") List<String> ids);
}