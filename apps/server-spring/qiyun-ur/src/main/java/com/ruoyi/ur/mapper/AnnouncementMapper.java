package com.ruoyi.ur.mapper;

import com.ruoyi.ur.domain.vo.AnnouncementVo;
import org.apache.ibatis.annotations.Mapper;

import java.util.List;

@Mapper
public interface AnnouncementMapper {
    AnnouncementVo selectById(String id);

    List<AnnouncementVo> selectList();
}