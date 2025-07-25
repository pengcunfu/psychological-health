package com.ruoyi.ur.service.impl;

import com.ruoyi.ur.domain.vo.AnnouncementVo;
import com.ruoyi.ur.mapper.AnnouncementMapper;
import com.ruoyi.ur.service.IAnnouncementService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import java.util.List;

@Service
public class AnnouncementServiceImpl implements IAnnouncementService {

    @Autowired
    private AnnouncementMapper announcementMapper;

    @Override
    public AnnouncementVo getById(String id) {
        return announcementMapper.selectById(id);
    }
    @Override
    public List<AnnouncementVo> selectList() {
        return announcementMapper.selectList();
    }
}