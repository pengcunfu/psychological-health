package com.ruoyi.ur.service;

import com.github.pagehelper.PageInfo;
import com.ruoyi.ur.domain.dto.CourseDetailDto;
import com.ruoyi.ur.domain.dto.CourseDto;

/**
 * 课程服务接口
 * 提供课程相关的服务，包括课程信息管理、课程内容管理、课程预约等功能
 *
 * @author ruoyi
 */
public interface ICourseService {
    
    /**
     * 获取课程列表
     *
     * @param keyword 搜索关键词
     * @param categoryId 课程分类ID
     * @param sortBy 排序方式
     * @param page 页码
     * @param pageSize 每页数量
     * @return 分页的课程信息列表
     */
    PageInfo<CourseDto> getCourses(String keyword, String categoryId, String sortBy, Integer page, Integer pageSize);

    /**
     * 根据ID获取课程详情
     *
     * @param id 课程ID
     * @return 课程详细信息DTO对象
     */
    CourseDetailDto getCourseDetailById(String id);
}