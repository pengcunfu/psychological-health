package com.ruoyi.ur.mapper;

import com.ruoyi.ur.domain.dto.CourseDetailDto;
import com.ruoyi.ur.domain.dto.CourseDto;
import org.apache.ibatis.annotations.Mapper;
import org.apache.ibatis.annotations.Param;

import java.util.List;

@Mapper
public interface CourseMapper {
    List<CourseDto> selectCourses(@Param("keyword") String keyword,
                                  @Param("categoryId") String categoryId,
                                  @Param("sortBy") String sortBy);

    CourseDetailDto selectCourseDetailById(@Param("id") String id);
}