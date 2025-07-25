package com.ruoyi.ur.service.impl;

import com.github.pagehelper.PageHelper;
import com.github.pagehelper.PageInfo;
import com.ruoyi.ur.domain.dto.CourseDetailDto;
import com.ruoyi.ur.domain.dto.CourseDto;
import com.ruoyi.ur.mapper.CourseMapper;
import com.ruoyi.ur.service.ICourseService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import java.util.List;

@Service
public class ICourseServiceImpl implements ICourseService {

    @Autowired
    private CourseMapper courseMapper;

    @Override
    public PageInfo<CourseDto> getCourses(String keyword, String categoryId, String sortBy, Integer page, Integer pageSize) {
        PageHelper.startPage(page, pageSize);
        List<CourseDto> list = courseMapper.selectCourses(keyword, categoryId, sortBy);
        return new PageInfo<>(list);
    }

    public CourseDetailDto getCourseDetailById(String id) {
        return courseMapper.selectCourseDetailById(id);
    }
}