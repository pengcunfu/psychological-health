package com.ruoyi.ur.controller;

import com.ruoyi.common.annotation.Anonymous;
import com.ruoyi.ur.domain.entity.DiseaseTags;
import com.ruoyi.ur.service.IDiseaseTagsService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/diseaseTags")
public class DiseaseTagsController {

    @Autowired
    private IDiseaseTagsService IDiseaseTagsService;

    @GetMapping("/list")
    @Anonymous
    public List<DiseaseTags> getAll() {
        return IDiseaseTagsService.getAll();
    }

}
