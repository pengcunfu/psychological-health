package com.ruoyi.ur.mapper;

import com.ruoyi.ur.domain.dto.CounselorDetailRequest;
import com.ruoyi.ur.domain.dto.CounselorQueryRequest;
import com.ruoyi.ur.domain.dto.CounselorReviewDto;
import com.ruoyi.ur.domain.vo.CounselorVo;
import org.apache.ibatis.annotations.Mapper;
import org.apache.ibatis.annotations.Param;

import java.util.List;

@Mapper
public interface CounselorMapper {
    List<CounselorVo> selectCounselors(@Param("request") CounselorQueryRequest request);

    int countCounselors(@Param("request") CounselorQueryRequest request);

    CounselorDetailRequest selectCounselorById(String id);

    List<CounselorReviewDto> selectReviewsByCounselorId(String counselorId);
}