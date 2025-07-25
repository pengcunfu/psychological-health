package com.ruoyi.ur.controller;

import com.github.pagehelper.PageInfo;
import com.ruoyi.common.annotation.Anonymous;
import com.ruoyi.common.core.domain.AjaxResult;
import com.ruoyi.ur.domain.dto.CourseDetailDto;
import com.ruoyi.ur.domain.dto.CourseDto;
import com.ruoyi.ur.service.ICourseService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;

import static com.ruoyi.common.core.domain.AjaxResult.success;

@RestController
@RequestMapping("/courses")
public class CourseController {
    
    @Autowired
    private ICourseService ICourseService;

    @GetMapping
    @Anonymous
    public AjaxResult getCourses(
            @RequestParam(required = false) String keyword,
            @RequestParam(required = false) String categoryId,
            @RequestParam(defaultValue = "popularity") String sortBy,
            @RequestParam(defaultValue = "1") Integer page,
            @RequestParam(defaultValue = "10") Integer pageSize) {
        
        PageInfo<CourseDto> pageInfo = ICourseService.getCourses(keyword, categoryId, sortBy, page, pageSize);
        return AjaxResult.success(pageInfo);
    }

    @GetMapping("/detail/{id}")
    @Anonymous
    public AjaxResult getCourseDetail(@PathVariable String id) {
        CourseDetailDto detail = ICourseService.getCourseDetailById(id);
        return AjaxResult.success(detail);
    }
}