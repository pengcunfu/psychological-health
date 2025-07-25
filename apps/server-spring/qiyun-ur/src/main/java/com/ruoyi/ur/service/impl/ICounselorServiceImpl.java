package com.ruoyi.ur.service.impl;

import com.github.pagehelper.PageHelper;
import com.github.pagehelper.PageInfo;
import com.ruoyi.ur.domain.dto.CounselorDetailRequest;
import com.ruoyi.ur.domain.dto.CounselorQueryRequest;
import com.ruoyi.ur.domain.dto.CounselorReviewDto;
import com.ruoyi.ur.domain.vo.CounselorVo;
import com.ruoyi.ur.mapper.CounselorMapper;
import com.ruoyi.ur.service.ICounselorService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.List;

@Service
public class ICounselorServiceImpl implements ICounselorService {

    @Autowired
    private CounselorMapper counselorMapper;
    @Override
    public PageInfo<CounselorVo> searchCounselors(CounselorQueryRequest request) {
        PageHelper.startPage(request.getPage(), request.getPageSize());
        List<CounselorVo> list = counselorMapper.selectCounselors(request);
        return new PageInfo<>(list);
    }

    @Override
    public int countCounselors(CounselorQueryRequest request) {
        return counselorMapper.countCounselors(request);
    }

    @Override
    public CounselorDetailRequest getCounselorDetail(String id) {
        CounselorDetailRequest detail = counselorMapper.selectCounselorById(id);
        
        List<CounselorReviewDto> reviews = counselorMapper.selectReviewsByCounselorId(id);
        detail.setReviews(reviews);
        
        return detail;
    }
}