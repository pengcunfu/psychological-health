package com.ruoyi.ur.controller;

import com.github.pagehelper.PageInfo;
import com.ruoyi.common.annotation.Anonymous;
import com.ruoyi.common.core.domain.AjaxResult;
import com.ruoyi.ur.domain.dto.CounselorQueryRequest;
import com.ruoyi.ur.domain.vo.CounselorVo;
import com.ruoyi.ur.service.ICounselorService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;

import static com.ruoyi.common.core.domain.AjaxResult.success;

/**
 * 咨询师管理控制器
 * 提供咨询师信息的查询、详情等功能
 *
 * @author ruoyi
 * @version 1.0
 * @date 2024-04-21
 */
@RestController
@RequestMapping("/counselor")
public class CounselorController {
    
    @Autowired
    private ICounselorService counselorService;

    /**
     * 分页查询咨询师列表
     *
     * @param request 查询条件请求对象，包含筛选、排序、分页等参数
     * @return 咨询师列表和总数
     * @apiNote 此接口允许匿名访问
     *          返回数据包含：
     *          - total: 符合条件的总记录数
     *          - list: 分页后的咨询师列表数据
     */
    @PostMapping("/list")
    @Anonymous
    public AjaxResult getCounselorList(@RequestBody CounselorQueryRequest request) {
        PageInfo<CounselorVo> list = counselorService.searchCounselors(request);
        int total = counselorService.countCounselors(request);

        return success()
                .put("total", total)
                .put("list", list);
    }

    /**
     * 获取咨询师详细信息
     *
     * @param id 咨询师ID
     * @return 咨询师详细信息
     * @apiNote 此接口允许匿名访问
     *          返回指定咨询师的完整信息，包括基本信息、资质信息、服务信息等
     */
    @GetMapping("/{id}")
    @Anonymous
    public AjaxResult getCounselorDetail(@PathVariable String id) {
        return AjaxResult.success(counselorService.getCounselorDetail(id));
    }
}