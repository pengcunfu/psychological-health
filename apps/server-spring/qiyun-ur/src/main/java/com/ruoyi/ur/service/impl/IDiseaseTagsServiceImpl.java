package com.ruoyi.ur.service.impl;

import com.ruoyi.ur.domain.entity.DiseaseTags;
import com.ruoyi.ur.mapper.DiseaseTagsMapper;
import com.ruoyi.ur.service.IDiseaseTagsService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.List;

@Service
public class IDiseaseTagsServiceImpl implements IDiseaseTagsService {

    @Autowired
    private DiseaseTagsMapper diseaseTagsMapper;

    @Override
    public List<DiseaseTags> getAll() {
        return diseaseTagsMapper.selectAll();
    }

}
