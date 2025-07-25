package com.ruoyi.ur.service;

import com.github.pagehelper.PageInfo;
import com.ruoyi.ur.domain.dto.CounselorDetailRequest;
import com.ruoyi.ur.domain.dto.CounselorQueryRequest;
import com.ruoyi.ur.domain.vo.CounselorVo;

/**
 * 咨询师服务接口
 * 提供咨询师相关的服务，包括咨询师信息管理、排班、预约等功能
 *
 * @author ruoyi
 */
public interface ICounselorService {
    
    /**
     * 搜索咨询师列表
     *
     * @param request 查询条件请求对象，包含搜索关键词、筛选条件等
     * @return 分页的咨询师信息列表
     */
    PageInfo<CounselorVo> searchCounselors(CounselorQueryRequest request);

    /**
     * 统计符合条件的咨询师数量
     *
     * @param request 查询条件请求对象
     * @return 符合条件的咨询师总数
     */
    int countCounselors(CounselorQueryRequest request);

    /**
     * 获取咨询师详细信息
     *
     * @param id 咨询师ID
     * @return 咨询师详细信息DTO对象
     */
    CounselorDetailRequest getCounselorDetail(String id);
}