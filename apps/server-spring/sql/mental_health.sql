/*
 Navicat Premium Data Transfer

 Source Server         : Xder1
 Source Server Type    : MySQL
 Source Server Version : 80040
 Source Host           : localhost:3306
 Source Schema         : mental_health

 Target Server Type    : MySQL
 Target Server Version : 80040
 File Encoding         : 65001

 Date: 03/06/2025 17:50:07
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for gen_table
-- ----------------------------
DROP TABLE IF EXISTS `gen_table`;
CREATE TABLE `gen_table`  (
  `table_id` bigint NOT NULL AUTO_INCREMENT COMMENT '编号',
  `table_name` varchar(200) CHARACTER SET utf8mb3 COLLATE utf8mb3_unicode_ci NULL DEFAULT '' COMMENT '表名称',
  `table_comment` varchar(500) CHARACTER SET utf8mb3 COLLATE utf8mb3_unicode_ci NULL DEFAULT '' COMMENT '表描述',
  `sub_table_name` varchar(64) CHARACTER SET utf8mb3 COLLATE utf8mb3_unicode_ci NULL DEFAULT NULL COMMENT '关联子表的表名',
  `sub_table_fk_name` varchar(64) CHARACTER SET utf8mb3 COLLATE utf8mb3_unicode_ci NULL DEFAULT NULL COMMENT '子表关联的外键名',
  `class_name` varchar(100) CHARACTER SET utf8mb3 COLLATE utf8mb3_unicode_ci NULL DEFAULT '' COMMENT '实体类名称',
  `tpl_category` varchar(200) CHARACTER SET utf8mb3 COLLATE utf8mb3_unicode_ci NULL DEFAULT 'crud' COMMENT '使用的模板（crud单表操作 tree树表操作）',
  `tpl_web_type` varchar(30) CHARACTER SET utf8mb3 COLLATE utf8mb3_unicode_ci NULL DEFAULT '' COMMENT '前端模板类型（element-ui模版 element-plus模版）',
  `package_name` varchar(100) CHARACTER SET utf8mb3 COLLATE utf8mb3_unicode_ci NULL DEFAULT NULL COMMENT '生成包路径',
  `module_name` varchar(30) CHARACTER SET utf8mb3 COLLATE utf8mb3_unicode_ci NULL DEFAULT NULL COMMENT '生成模块名',
  `business_name` varchar(30) CHARACTER SET utf8mb3 COLLATE utf8mb3_unicode_ci NULL DEFAULT NULL COMMENT '生成业务名',
  `function_name` varchar(50) CHARACTER SET utf8mb3 COLLATE utf8mb3_unicode_ci NULL DEFAULT NULL COMMENT '生成功能名',
  `function_author` varchar(50) CHARACTER SET utf8mb3 COLLATE utf8mb3_unicode_ci NULL DEFAULT NULL COMMENT '生成功能作者',
  `gen_type` char(1) CHARACTER SET utf8mb3 COLLATE utf8mb3_unicode_ci NULL DEFAULT '0' COMMENT '生成代码方式（0zip压缩包 1自定义路径）',
  `gen_path` varchar(200) CHARACTER SET utf8mb3 COLLATE utf8mb3_unicode_ci NULL DEFAULT '/' COMMENT '生成路径（不填默认项目路径）',
  `options` varchar(1000) CHARACTER SET utf8mb3 COLLATE utf8mb3_unicode_ci NULL DEFAULT NULL COMMENT '其它生成选项',
  `create_by` varchar(64) CHARACTER SET utf8mb3 COLLATE utf8mb3_unicode_ci NULL DEFAULT '' COMMENT '创建者',
  `create_time` datetime NULL DEFAULT NULL COMMENT '创建时间',
  `update_by` varchar(64) CHARACTER SET utf8mb3 COLLATE utf8mb3_unicode_ci NULL DEFAULT '' COMMENT '更新者',
  `update_time` datetime NULL DEFAULT NULL COMMENT '更新时间',
  `remark` varchar(500) CHARACTER SET utf8mb3 COLLATE utf8mb3_unicode_ci NULL DEFAULT NULL COMMENT '备注',
  PRIMARY KEY (`table_id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 12 CHARACTER SET = utf8mb3 COLLATE = utf8mb3_unicode_ci COMMENT = '代码生成业务表' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of gen_table
-- ----------------------------
INSERT INTO `gen_table` VALUES (1, 'ur_review', '', NULL, NULL, 'UrReview', 'crud', '', 'com.ruoyi.system', 'system', 'review', NULL, 'ruoyi', '0', '/', NULL, 'admin', '2025-05-07 11:19:07', '', NULL, NULL);
INSERT INTO `gen_table` VALUES (2, 'ur_user', '', NULL, NULL, 'UrUser', 'crud', '', 'com.ruoyi.system', 'system', 'user', NULL, 'ruoyi', '0', '/', NULL, 'admin', '2025-05-07 11:19:07', '', NULL, NULL);
INSERT INTO `gen_table` VALUES (3, 'ur_appointment', '', NULL, NULL, 'UrAppointment', 'crud', '', 'com.ruoyi.system', 'system', 'appointment', NULL, 'ruoyi', '0', '/', NULL, 'admin', '2025-05-07 11:19:17', '', NULL, NULL);
INSERT INTO `gen_table` VALUES (4, 'ur_counselor', '', NULL, NULL, 'UrCounselor', 'crud', '', 'com.ruoyi.system', 'system', 'counselor', NULL, 'ruoyi', '0', '/', NULL, 'admin', '2025-05-07 11:19:17', '', NULL, NULL);
INSERT INTO `gen_table` VALUES (5, 'ur_counselor_region', '', NULL, NULL, 'UrCounselorRegion', 'crud', '', 'com.ruoyi.system', 'system', 'region', NULL, 'ruoyi', '0', '/', NULL, 'admin', '2025-05-07 11:19:17', '', NULL, NULL);
INSERT INTO `gen_table` VALUES (6, 'ur_course', '', NULL, NULL, 'UrCourse', 'crud', '', 'com.ruoyi.system', 'system', 'course', NULL, 'ruoyi', '0', '/', NULL, 'admin', '2025-05-07 11:19:17', '', NULL, NULL);
INSERT INTO `gen_table` VALUES (7, 'ur_course_detail', '', NULL, NULL, 'UrCourseDetail', 'crud', '', 'com.ruoyi.system', 'system', 'detail', NULL, 'ruoyi', '0', '/', NULL, 'admin', '2025-05-07 11:19:17', '', NULL, NULL);
INSERT INTO `gen_table` VALUES (8, 'ur_course_purchase_order', '', NULL, NULL, 'UrCoursePurchaseOrder', 'crud', '', 'com.ruoyi.system', 'system', 'order', NULL, 'ruoyi', '0', '/', NULL, 'admin', '2025-05-07 11:19:17', '', NULL, NULL);
INSERT INTO `gen_table` VALUES (9, 'ur_course_read_record', '', NULL, NULL, 'UrCourseReadRecord', 'crud', '', 'com.ruoyi.system', 'system', 'record', NULL, 'ruoyi', '0', '/', NULL, 'admin', '2025-05-07 11:19:17', '', NULL, NULL);
INSERT INTO `gen_table` VALUES (10, 'ur_psychological_appointment_order', '', NULL, NULL, 'UrPsychologicalAppointmentOrder', 'crud', '', 'com.ruoyi.system', 'system', 'order', NULL, 'ruoyi', '0', '/', NULL, 'admin', '2025-05-07 11:19:17', '', NULL, NULL);
INSERT INTO `gen_table` VALUES (11, 'ur_region', '', NULL, NULL, 'UrRegion', 'crud', '', 'com.ruoyi.system', 'system', 'region', NULL, 'ruoyi', '0', '/', NULL, 'admin', '2025-05-07 11:19:17', '', NULL, NULL);
INSERT INTO `gen_table` VALUES (12, 'ur_visitor', '', NULL, NULL, 'UrVisitor', 'crud', '', 'com.ruoyi.system', 'system', 'visitor', NULL, 'ruoyi', '0', '/', NULL, 'admin', '2025-05-07 11:19:17', '', NULL, NULL);

-- ----------------------------
-- Table structure for gen_table_column
-- ----------------------------
DROP TABLE IF EXISTS `gen_table_column`;
CREATE TABLE `gen_table_column`  (
  `column_id` bigint NOT NULL AUTO_INCREMENT COMMENT '编号',
  `table_id` bigint NULL DEFAULT NULL COMMENT '归属表编号',
  `column_name` varchar(200) CHARACTER SET utf8mb3 COLLATE utf8mb3_unicode_ci NULL DEFAULT NULL COMMENT '列名称',
  `column_comment` varchar(500) CHARACTER SET utf8mb3 COLLATE utf8mb3_unicode_ci NULL DEFAULT NULL COMMENT '列描述',
  `column_type` varchar(100) CHARACTER SET utf8mb3 COLLATE utf8mb3_unicode_ci NULL DEFAULT NULL COMMENT '列类型',
  `java_type` varchar(500) CHARACTER SET utf8mb3 COLLATE utf8mb3_unicode_ci NULL DEFAULT NULL COMMENT 'JAVA类型',
  `java_field` varchar(200) CHARACTER SET utf8mb3 COLLATE utf8mb3_unicode_ci NULL DEFAULT NULL COMMENT 'JAVA字段名',
  `is_pk` char(1) CHARACTER SET utf8mb3 COLLATE utf8mb3_unicode_ci NULL DEFAULT NULL COMMENT '是否主键（1是）',
  `is_increment` char(1) CHARACTER SET utf8mb3 COLLATE utf8mb3_unicode_ci NULL DEFAULT NULL COMMENT '是否自增（1是）',
  `is_required` char(1) CHARACTER SET utf8mb3 COLLATE utf8mb3_unicode_ci NULL DEFAULT NULL COMMENT '是否必填（1是）',
  `is_insert` char(1) CHARACTER SET utf8mb3 COLLATE utf8mb3_unicode_ci NULL DEFAULT NULL COMMENT '是否为插入字段（1是）',
  `is_edit` char(1) CHARACTER SET utf8mb3 COLLATE utf8mb3_unicode_ci NULL DEFAULT NULL COMMENT '是否编辑字段（1是）',
  `is_list` char(1) CHARACTER SET utf8mb3 COLLATE utf8mb3_unicode_ci NULL DEFAULT NULL COMMENT '是否列表字段（1是）',
  `is_query` char(1) CHARACTER SET utf8mb3 COLLATE utf8mb3_unicode_ci NULL DEFAULT NULL COMMENT '是否查询字段（1是）',
  `query_type` varchar(200) CHARACTER SET utf8mb3 COLLATE utf8mb3_unicode_ci NULL DEFAULT 'EQ' COMMENT '查询方式（等于、不等于、大于、小于、范围）',
  `html_type` varchar(200) CHARACTER SET utf8mb3 COLLATE utf8mb3_unicode_ci NULL DEFAULT NULL COMMENT '显示类型（文本框、文本域、下拉框、复选框、单选框、日期控件）',
  `dict_type` varchar(200) CHARACTER SET utf8mb3 COLLATE utf8mb3_unicode_ci NULL DEFAULT '' COMMENT '字典类型',
  `sort` int NULL DEFAULT NULL COMMENT '排序',
  `create_by` varchar(64) CHARACTER SET utf8mb3 COLLATE utf8mb3_unicode_ci NULL DEFAULT '' COMMENT '创建者',
  `create_time` datetime NULL DEFAULT NULL COMMENT '创建时间',
  `update_by` varchar(64) CHARACTER SET utf8mb3 COLLATE utf8mb3_unicode_ci NULL DEFAULT '' COMMENT '更新者',
  `update_time` datetime NULL DEFAULT NULL COMMENT '更新时间',
  PRIMARY KEY (`column_id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 115 CHARACTER SET = utf8mb3 COLLATE = utf8mb3_unicode_ci COMMENT = '代码生成业务表字段' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of gen_table_column
-- ----------------------------
INSERT INTO `gen_table_column` VALUES (1, 1, 'review_id', NULL, 'int', 'Long', 'reviewId', '1', '1', '0', '1', NULL, NULL, NULL, 'EQ', 'input', '', 1, 'admin', '2025-05-07 11:19:07', '', NULL);
INSERT INTO `gen_table_column` VALUES (2, 1, 'counselor_id', NULL, 'int', 'Long', 'counselorId', '0', '0', '0', '1', '1', '1', '1', 'EQ', 'input', '', 2, 'admin', '2025-05-07 11:19:07', '', NULL);
INSERT INTO `gen_table_column` VALUES (3, 1, 'user_id', NULL, 'int', 'Long', 'userId', '0', '0', '0', '1', '1', '1', '1', 'EQ', 'input', '', 3, 'admin', '2025-05-07 11:19:07', '', NULL);
INSERT INTO `gen_table_column` VALUES (4, 1, 'review_content', NULL, 'text', 'String', 'reviewContent', '0', '0', '0', '1', '1', '1', '1', 'EQ', 'editor', '', 4, 'admin', '2025-05-07 11:19:07', '', NULL);
INSERT INTO `gen_table_column` VALUES (5, 1, 'review_time', NULL, 'datetime', 'Date', 'reviewTime', '0', '0', '0', '1', '1', '1', '1', 'EQ', 'datetime', '', 5, 'admin', '2025-05-07 11:19:07', '', NULL);
INSERT INTO `gen_table_column` VALUES (6, 2, 'user_id', NULL, 'int', 'Long', 'userId', '1', '1', '0', '1', NULL, NULL, NULL, 'EQ', 'input', '', 1, 'admin', '2025-05-07 11:19:07', '', NULL);
INSERT INTO `gen_table_column` VALUES (7, 2, 'nickname', NULL, 'varchar(50)', 'String', 'nickname', '0', '0', '0', '1', '1', '1', '1', 'LIKE', 'input', '', 2, 'admin', '2025-05-07 11:19:07', '', NULL);
INSERT INTO `gen_table_column` VALUES (8, 2, 'gender', NULL, 'varchar(10)', 'String', 'gender', '0', '0', '0', '1', '1', '1', '1', 'EQ', 'input', '', 3, 'admin', '2025-05-07 11:19:07', '', NULL);
INSERT INTO `gen_table_column` VALUES (9, 2, 'age', NULL, 'int', 'Long', 'age', '0', '0', '0', '1', '1', '1', '1', 'EQ', 'input', '', 4, 'admin', '2025-05-07 11:19:07', '', NULL);
INSERT INTO `gen_table_column` VALUES (10, 2, 'phone_number', NULL, 'varchar(20)', 'String', 'phoneNumber', '0', '0', '0', '1', '1', '1', '1', 'EQ', 'input', '', 5, 'admin', '2025-05-07 11:19:07', '', NULL);
INSERT INTO `gen_table_column` VALUES (11, 2, 'email', NULL, 'varchar(100)', 'String', 'email', '0', '0', '0', '1', '1', '1', '1', 'EQ', 'input', '', 6, 'admin', '2025-05-07 11:19:07', '', NULL);
INSERT INTO `gen_table_column` VALUES (12, 2, 'account', NULL, 'varchar(50)', 'String', 'account', '0', '0', '0', '1', '1', '1', '1', 'EQ', 'input', '', 7, 'admin', '2025-05-07 11:19:07', '', NULL);
INSERT INTO `gen_table_column` VALUES (13, 2, 'password', NULL, 'varchar(100)', 'String', 'password', '0', '0', '0', '1', '1', '1', '1', 'EQ', 'input', '', 8, 'admin', '2025-05-07 11:19:07', '', NULL);
INSERT INTO `gen_table_column` VALUES (14, 2, 'avatar', NULL, 'varchar(255)', 'String', 'avatar', '0', '0', '0', '1', '1', '1', '1', 'EQ', 'input', '', 9, 'admin', '2025-05-07 11:19:07', '', NULL);
INSERT INTO `gen_table_column` VALUES (15, 2, 'introduction', NULL, 'text', 'String', 'introduction', '0', '0', '0', '1', '1', '1', '1', 'EQ', 'textarea', '', 10, 'admin', '2025-05-07 11:19:07', '', NULL);
INSERT INTO `gen_table_column` VALUES (16, 2, 'create_time', NULL, 'datetime', 'Date', 'createTime', '0', '0', '0', '1', NULL, NULL, NULL, 'EQ', 'datetime', '', 11, 'admin', '2025-05-07 11:19:07', '', NULL);
INSERT INTO `gen_table_column` VALUES (17, 2, 'last_login_time', NULL, 'datetime', 'Date', 'lastLoginTime', '0', '0', '0', '1', '1', '1', '1', 'EQ', 'datetime', '', 12, 'admin', '2025-05-07 11:19:07', '', NULL);
INSERT INTO `gen_table_column` VALUES (18, 3, 'appointment_id', NULL, 'int', 'Long', 'appointmentId', '1', '1', '0', '1', NULL, NULL, NULL, 'EQ', 'input', '', 1, 'admin', '2025-05-07 11:19:17', '', NULL);
INSERT INTO `gen_table_column` VALUES (19, 3, 'counselor_id', NULL, 'int', 'Long', 'counselorId', '0', '0', '0', '1', '1', '1', '1', 'EQ', 'input', '', 2, 'admin', '2025-05-07 11:19:17', '', NULL);
INSERT INTO `gen_table_column` VALUES (20, 3, 'user_id', NULL, 'int', 'Long', 'userId', '0', '0', '0', '1', '1', '1', '1', 'EQ', 'input', '', 3, 'admin', '2025-05-07 11:19:17', '', NULL);
INSERT INTO `gen_table_column` VALUES (21, 3, 'start_time', NULL, 'datetime', 'Date', 'startTime', '0', '0', '0', '1', '1', '1', '1', 'EQ', 'datetime', '', 4, 'admin', '2025-05-07 11:19:17', '', NULL);
INSERT INTO `gen_table_column` VALUES (22, 3, 'end_time', NULL, 'datetime', 'Date', 'endTime', '0', '0', '0', '1', '1', '1', '1', 'EQ', 'datetime', '', 5, 'admin', '2025-05-07 11:19:17', '', NULL);
INSERT INTO `gen_table_column` VALUES (23, 4, 'counselor_id', NULL, 'int', 'Long', 'counselorId', '1', '1', '0', '1', NULL, NULL, NULL, 'EQ', 'input', '', 1, 'admin', '2025-05-07 11:19:17', '', NULL);
INSERT INTO `gen_table_column` VALUES (24, 4, 'name', NULL, 'varchar(100)', 'String', 'name', '0', '0', '1', '1', '1', '1', '1', 'LIKE', 'input', '', 2, 'admin', '2025-05-07 11:19:17', '', NULL);
INSERT INTO `gen_table_column` VALUES (25, 4, 'picture_url', NULL, 'varchar(255)', 'String', 'pictureUrl', '0', '0', '0', '1', '1', '1', '1', 'EQ', 'input', '', 3, 'admin', '2025-05-07 11:19:17', '', NULL);
INSERT INTO `gen_table_column` VALUES (26, 4, 'personal_introduction', NULL, 'text', 'String', 'personalIntroduction', '0', '0', '0', '1', '1', '1', '1', 'EQ', 'textarea', '', 4, 'admin', '2025-05-07 11:19:17', '', NULL);
INSERT INTO `gen_table_column` VALUES (27, 4, 'expertise_areas', NULL, 'text', 'String', 'expertiseAreas', '0', '0', '0', '1', '1', '1', '1', 'EQ', 'textarea', '', 5, 'admin', '2025-05-07 11:19:17', '', NULL);
INSERT INTO `gen_table_column` VALUES (28, 4, 'years_of_practice', NULL, 'int', 'Long', 'yearsOfPractice', '0', '0', '0', '1', '1', '1', '1', 'EQ', 'input', '', 6, 'admin', '2025-05-07 11:19:17', '', NULL);
INSERT INTO `gen_table_column` VALUES (29, 4, 'supported_types', NULL, 'text', 'String', 'supportedTypes', '0', '0', '0', '1', '1', '1', '1', 'EQ', 'textarea', '', 7, 'admin', '2025-05-07 11:19:17', '', NULL);
INSERT INTO `gen_table_column` VALUES (30, 4, 'teaching_price', NULL, 'decimal(10,2)', 'BigDecimal', 'teachingPrice', '0', '0', '0', '1', '1', '1', '1', 'EQ', 'input', '', 8, 'admin', '2025-05-07 11:19:17', '', NULL);
INSERT INTO `gen_table_column` VALUES (31, 4, 'counselor_level', NULL, 'varchar(50)', 'String', 'counselorLevel', '0', '0', '0', '1', '1', '1', '1', 'EQ', 'input', '', 9, 'admin', '2025-05-07 11:19:17', '', NULL);
INSERT INTO `gen_table_column` VALUES (32, 4, 'counselor_type', NULL, 'varchar(100)', 'String', 'counselorType', '0', '0', '0', '1', '1', '1', '1', 'EQ', 'select', '', 10, 'admin', '2025-05-07 11:19:17', '', NULL);
INSERT INTO `gen_table_column` VALUES (33, 4, 'tags', NULL, 'text', 'String', 'tags', '0', '0', '0', '1', '1', '1', '1', 'EQ', 'textarea', '', 11, 'admin', '2025-05-07 11:19:17', '', NULL);
INSERT INTO `gen_table_column` VALUES (34, 4, 'rating', NULL, 'decimal(3,2)', 'BigDecimal', 'rating', '0', '0', '0', '1', '1', '1', '1', 'EQ', 'input', '', 12, 'admin', '2025-05-07 11:19:17', '', NULL);
INSERT INTO `gen_table_column` VALUES (35, 4, 'total_practice_hours', NULL, 'int', 'Long', 'totalPracticeHours', '0', '0', '0', '1', '1', '1', '1', 'EQ', 'input', '', 13, 'admin', '2025-05-07 11:19:17', '', NULL);
INSERT INTO `gen_table_column` VALUES (36, 4, 'good_at_problems', NULL, 'text', 'String', 'goodAtProblems', '0', '0', '0', '1', '1', '1', '1', 'EQ', 'textarea', '', 14, 'admin', '2025-05-07 11:19:17', '', NULL);
INSERT INTO `gen_table_column` VALUES (37, 4, 'treatment_methods', NULL, 'text', 'String', 'treatmentMethods', '0', '0', '0', '1', '1', '1', '1', 'EQ', 'textarea', '', 15, 'admin', '2025-05-07 11:19:17', '', NULL);
INSERT INTO `gen_table_column` VALUES (38, 4, 'consultation_duration', NULL, 'int', 'Long', 'consultationDuration', '0', '0', '0', '1', '1', '1', '1', 'EQ', 'input', '', 16, 'admin', '2025-05-07 11:19:17', '', NULL);
INSERT INTO `gen_table_column` VALUES (39, 4, 'professional_qualification', NULL, 'varchar(255)', 'String', 'professionalQualification', '0', '0', '0', '1', '1', '1', '1', 'EQ', 'input', '', 17, 'admin', '2025-05-07 11:19:17', '', NULL);
INSERT INTO `gen_table_column` VALUES (40, 4, 'certification_certificate_url', NULL, 'varchar(255)', 'String', 'certificationCertificateUrl', '0', '0', '0', '1', '1', '1', '1', 'EQ', 'input', '', 18, 'admin', '2025-05-07 11:19:17', '', NULL);
INSERT INTO `gen_table_column` VALUES (41, 4, 'working_hours', NULL, 'text', 'String', 'workingHours', '0', '0', '0', '1', '1', '1', '1', 'EQ', 'textarea', '', 19, 'admin', '2025-05-07 11:19:17', '', NULL);
INSERT INTO `gen_table_column` VALUES (42, 5, 'id', NULL, 'int', 'Long', 'id', '1', '1', '0', '1', NULL, NULL, NULL, 'EQ', 'input', '', 1, 'admin', '2025-05-07 11:19:17', '', NULL);
INSERT INTO `gen_table_column` VALUES (43, 5, 'counselor_id', NULL, 'int', 'Long', 'counselorId', '0', '0', '0', '1', '1', '1', '1', 'EQ', 'input', '', 2, 'admin', '2025-05-07 11:19:17', '', NULL);
INSERT INTO `gen_table_column` VALUES (44, 5, 'region_id', NULL, 'int', 'Long', 'regionId', '0', '0', '0', '1', '1', '1', '1', 'EQ', 'input', '', 3, 'admin', '2025-05-07 11:19:17', '', NULL);
INSERT INTO `gen_table_column` VALUES (45, 6, 'course_id', NULL, 'int', 'Long', 'courseId', '1', '1', '0', '1', NULL, NULL, NULL, 'EQ', 'input', '', 1, 'admin', '2025-05-07 11:19:17', '', NULL);
INSERT INTO `gen_table_column` VALUES (46, 6, 'course_name', NULL, 'varchar(200)', 'String', 'courseName', '0', '0', '1', '1', '1', '1', '1', 'LIKE', 'input', '', 2, 'admin', '2025-05-07 11:19:17', '', NULL);
INSERT INTO `gen_table_column` VALUES (47, 6, 'course_image_url', NULL, 'varchar(255)', 'String', 'courseImageUrl', '0', '0', '0', '1', '1', '1', '1', 'EQ', 'input', '', 3, 'admin', '2025-05-07 11:19:17', '', NULL);
INSERT INTO `gen_table_column` VALUES (48, 6, 'course_tags', NULL, 'text', 'String', 'courseTags', '0', '0', '0', '1', '1', '1', '1', 'EQ', 'textarea', '', 4, 'admin', '2025-05-07 11:19:17', '', NULL);
INSERT INTO `gen_table_column` VALUES (49, 6, 'class_hours', NULL, 'int', 'Long', 'classHours', '0', '0', '0', '1', '1', '1', '1', 'EQ', 'input', '', 5, 'admin', '2025-05-07 11:19:17', '', NULL);
INSERT INTO `gen_table_column` VALUES (50, 6, 'total_duration', NULL, 'int', 'Long', 'totalDuration', '0', '0', '0', '1', '1', '1', '1', 'EQ', 'input', '', 6, 'admin', '2025-05-07 11:19:17', '', NULL);
INSERT INTO `gen_table_column` VALUES (51, 6, 'price', NULL, 'decimal(10,2)', 'BigDecimal', 'price', '0', '0', '0', '1', '1', '1', '1', 'EQ', 'input', '', 7, 'admin', '2025-05-07 11:19:17', '', NULL);
INSERT INTO `gen_table_column` VALUES (52, 6, 'address', NULL, 'varchar(255)', 'String', 'address', '0', '0', '0', '1', '1', '1', '1', 'EQ', 'input', '', 8, 'admin', '2025-05-07 11:19:17', '', NULL);
INSERT INTO `gen_table_column` VALUES (53, 6, 'course_type', NULL, 'varchar(100)', 'String', 'courseType', '0', '0', '0', '1', '1', '1', '1', 'EQ', 'select', '', 9, 'admin', '2025-05-07 11:19:17', '', NULL);
INSERT INTO `gen_table_column` VALUES (54, 6, 'start_time', NULL, 'datetime', 'Date', 'startTime', '0', '0', '0', '1', '1', '1', '1', 'EQ', 'datetime', '', 10, 'admin', '2025-05-07 11:19:17', '', NULL);
INSERT INTO `gen_table_column` VALUES (55, 6, 'detail_id', NULL, 'int', 'Long', 'detailId', '0', '0', '0', '1', '1', '1', '1', 'EQ', 'input', '', 11, 'admin', '2025-05-07 11:19:17', '', NULL);
INSERT INTO `gen_table_column` VALUES (56, 6, 'course_images_urls', NULL, 'text', 'String', 'courseImagesUrls', '0', '0', '0', '1', '1', '1', '1', 'EQ', 'textarea', '', 12, 'admin', '2025-05-07 11:19:17', '', NULL);
INSERT INTO `gen_table_column` VALUES (57, 6, 'cumulative_students', NULL, 'int', 'Long', 'cumulativeStudents', '0', '0', '0', '1', '1', '1', '1', 'EQ', 'input', '', 13, 'admin', '2025-05-07 11:19:17', '', NULL);
INSERT INTO `gen_table_column` VALUES (58, 6, 'course_rating', NULL, 'decimal(3,2)', 'BigDecimal', 'courseRating', '0', '0', '0', '1', '1', '1', '1', 'EQ', 'input', '', 14, 'admin', '2025-05-07 11:19:17', '', NULL);
INSERT INTO `gen_table_column` VALUES (59, 6, 'author_name', NULL, 'varchar(100)', 'String', 'authorName', '0', '0', '0', '1', '1', '1', '1', 'LIKE', 'input', '', 15, 'admin', '2025-05-07 11:19:17', '', NULL);
INSERT INTO `gen_table_column` VALUES (60, 6, 'author_introduction', NULL, 'text', 'String', 'authorIntroduction', '0', '0', '0', '1', '1', '1', '1', 'EQ', 'textarea', '', 16, 'admin', '2025-05-07 11:19:17', '', NULL);
INSERT INTO `gen_table_column` VALUES (61, 6, 'course_introduction', NULL, 'text', 'String', 'courseIntroduction', '0', '0', '0', '1', '1', '1', '1', 'EQ', 'textarea', '', 17, 'admin', '2025-05-07 11:19:17', '', NULL);
INSERT INTO `gen_table_column` VALUES (62, 6, 'course_content', NULL, 'text', 'String', 'courseContent', '0', '0', '0', '1', '1', '1', '1', 'EQ', 'editor', '', 18, 'admin', '2025-05-07 11:19:17', '', NULL);
INSERT INTO `gen_table_column` VALUES (63, 7, 'main_title_id', NULL, 'int', 'Long', 'mainTitleId', '1', '1', '0', '1', NULL, NULL, NULL, 'EQ', 'input', '', 1, 'admin', '2025-05-07 11:19:17', '', NULL);
INSERT INTO `gen_table_column` VALUES (64, 7, 'course_id', NULL, 'int', 'Long', 'courseId', '0', '0', '0', '1', '1', '1', '1', 'EQ', 'input', '', 2, 'admin', '2025-05-07 11:19:17', '', NULL);
INSERT INTO `gen_table_column` VALUES (65, 7, 'main_title', NULL, 'varchar(200)', 'String', 'mainTitle', '0', '0', '0', '1', '1', '1', '1', 'EQ', 'input', '', 3, 'admin', '2025-05-07 11:19:17', '', NULL);
INSERT INTO `gen_table_column` VALUES (66, 7, 'subclass_hours', NULL, 'int', 'Long', 'subclassHours', '0', '0', '0', '1', '1', '1', '1', 'EQ', 'input', '', 4, 'admin', '2025-05-07 11:19:17', '', NULL);
INSERT INTO `gen_table_column` VALUES (67, 7, 'subtotal_duration', NULL, 'int', 'Long', 'subtotalDuration', '0', '0', '0', '1', '1', '1', '1', 'EQ', 'input', '', 5, 'admin', '2025-05-07 11:19:17', '', NULL);
INSERT INTO `gen_table_column` VALUES (68, 7, 'sub_title_id', NULL, 'int', 'Long', 'subTitleId', '0', '0', '0', '1', '1', '1', '1', 'EQ', 'input', '', 6, 'admin', '2025-05-07 11:19:17', '', NULL);
INSERT INTO `gen_table_column` VALUES (69, 7, 'sub_title_image_url', NULL, 'varchar(255)', 'String', 'subTitleImageUrl', '0', '0', '0', '1', '1', '1', '1', 'EQ', 'input', '', 7, 'admin', '2025-05-07 11:19:17', '', NULL);
INSERT INTO `gen_table_column` VALUES (70, 7, 'sub_title_duration', NULL, 'int', 'Long', 'subTitleDuration', '0', '0', '0', '1', '1', '1', '1', 'EQ', 'input', '', 8, 'admin', '2025-05-07 11:19:17', '', NULL);
INSERT INTO `gen_table_column` VALUES (71, 7, 'video_info', NULL, 'text', 'String', 'videoInfo', '0', '0', '0', '1', '1', '1', '1', 'EQ', 'textarea', '', 9, 'admin', '2025-05-07 11:19:17', '', NULL);
INSERT INTO `gen_table_column` VALUES (72, 8, 'order_id', NULL, 'varchar(50)', 'String', 'orderId', '1', '0', '0', '1', NULL, NULL, NULL, 'EQ', 'input', '', 1, 'admin', '2025-05-07 11:19:17', '', NULL);
INSERT INTO `gen_table_column` VALUES (73, 8, 'course_info', NULL, 'int', 'Long', 'courseInfo', '0', '0', '0', '1', '1', '1', '1', 'EQ', 'input', '', 2, 'admin', '2025-05-07 11:19:17', '', NULL);
INSERT INTO `gen_table_column` VALUES (74, 8, 'user_id', NULL, 'int', 'Long', 'userId', '0', '0', '0', '1', '1', '1', '1', 'EQ', 'input', '', 3, 'admin', '2025-05-07 11:19:17', '', NULL);
INSERT INTO `gen_table_column` VALUES (75, 8, 'purchase_time', NULL, 'datetime', 'Date', 'purchaseTime', '0', '0', '0', '1', '1', '1', '1', 'EQ', 'datetime', '', 4, 'admin', '2025-05-07 11:19:17', '', NULL);
INSERT INTO `gen_table_column` VALUES (76, 8, 'order_amount', NULL, 'decimal(10,2)', 'BigDecimal', 'orderAmount', '0', '0', '0', '1', '1', '1', '1', 'EQ', 'input', '', 5, 'admin', '2025-05-07 11:19:17', '', NULL);
INSERT INTO `gen_table_column` VALUES (77, 8, 'payment_status', NULL, 'varchar(20)', 'String', 'paymentStatus', '0', '0', '0', '1', '1', '1', '1', 'EQ', 'radio', '', 6, 'admin', '2025-05-07 11:19:17', '', NULL);
INSERT INTO `gen_table_column` VALUES (78, 9, 'record_id', NULL, 'int', 'Long', 'recordId', '1', '1', '0', '1', NULL, NULL, NULL, 'EQ', 'input', '', 1, 'admin', '2025-05-07 11:19:17', '', NULL);
INSERT INTO `gen_table_column` VALUES (79, 9, 'user_id', NULL, 'int', 'Long', 'userId', '0', '0', '0', '1', '1', '1', '1', 'EQ', 'input', '', 2, 'admin', '2025-05-07 11:19:17', '', NULL);
INSERT INTO `gen_table_column` VALUES (80, 9, 'course_id', NULL, 'int', 'Long', 'courseId', '0', '0', '0', '1', '1', '1', '1', 'EQ', 'input', '', 3, 'admin', '2025-05-07 11:19:17', '', NULL);
INSERT INTO `gen_table_column` VALUES (81, 9, 'start_read_time', NULL, 'datetime', 'Date', 'startReadTime', '0', '0', '0', '1', '1', '1', '1', 'EQ', 'datetime', '', 4, 'admin', '2025-05-07 11:19:17', '', NULL);
INSERT INTO `gen_table_column` VALUES (82, 9, 'end_read_time', NULL, 'datetime', 'Date', 'endReadTime', '0', '0', '0', '1', '1', '1', '1', 'EQ', 'datetime', '', 5, 'admin', '2025-05-07 11:19:17', '', NULL);
INSERT INTO `gen_table_column` VALUES (83, 9, 'read_duration', NULL, 'int', 'Long', 'readDuration', '0', '0', '0', '1', '1', '1', '1', 'EQ', 'input', '', 6, 'admin', '2025-05-07 11:19:17', '', NULL);
INSERT INTO `gen_table_column` VALUES (84, 9, 'last_read_time', NULL, 'datetime', 'Date', 'lastReadTime', '0', '0', '0', '1', '1', '1', '1', 'EQ', 'datetime', '', 7, 'admin', '2025-05-07 11:19:17', '', NULL);
INSERT INTO `gen_table_column` VALUES (85, 9, 'is_finished', NULL, 'enum(\'是\',\'否\')', 'String', 'isFinished', '0', '0', '0', '1', '1', '1', '1', 'EQ', NULL, '', 8, 'admin', '2025-05-07 11:19:17', '', NULL);
INSERT INTO `gen_table_column` VALUES (86, 10, 'order_id', NULL, 'varchar(50)', 'String', 'orderId', '1', '0', '0', '1', NULL, NULL, NULL, 'EQ', 'input', '', 1, 'admin', '2025-05-07 11:19:17', '', NULL);
INSERT INTO `gen_table_column` VALUES (87, 10, 'appointment_name', NULL, 'varchar(200)', 'String', 'appointmentName', '0', '0', '0', '1', '1', '1', '1', 'LIKE', 'input', '', 2, 'admin', '2025-05-07 11:19:17', '', NULL);
INSERT INTO `gen_table_column` VALUES (88, 10, 'author_info', NULL, 'int', 'Long', 'authorInfo', '0', '0', '0', '1', '1', '1', '1', 'EQ', 'input', '', 3, 'admin', '2025-05-07 11:19:17', '', NULL);
INSERT INTO `gen_table_column` VALUES (89, 10, 'user_id', NULL, 'int', 'Long', 'userId', '0', '0', '0', '1', '1', '1', '1', 'EQ', 'input', '', 4, 'admin', '2025-05-07 11:19:17', '', NULL);
INSERT INTO `gen_table_column` VALUES (90, 10, 'order_amount', NULL, 'decimal(10,2)', 'BigDecimal', 'orderAmount', '0', '0', '0', '1', '1', '1', '1', 'EQ', 'input', '', 5, 'admin', '2025-05-07 11:19:17', '', NULL);
INSERT INTO `gen_table_column` VALUES (91, 10, 'payment_status', NULL, 'varchar(20)', 'String', 'paymentStatus', '0', '0', '0', '1', '1', '1', '1', 'EQ', 'radio', '', 6, 'admin', '2025-05-07 11:19:17', '', NULL);
INSERT INTO `gen_table_column` VALUES (92, 11, 'region_id', NULL, 'int', 'Long', 'regionId', '1', '1', '0', '1', NULL, NULL, NULL, 'EQ', 'input', '', 1, 'admin', '2025-05-07 11:19:17', '', NULL);
INSERT INTO `gen_table_column` VALUES (93, 11, 'region_name', NULL, 'varchar(100)', 'String', 'regionName', '0', '0', '0', '1', '1', '1', '1', 'LIKE', 'input', '', 2, 'admin', '2025-05-07 11:19:17', '', NULL);
INSERT INTO `gen_table_column` VALUES (94, 12, 'visitor_id', NULL, 'int', 'Long', 'visitorId', '1', '1', '0', '1', NULL, NULL, NULL, 'EQ', 'input', '', 1, 'admin', '2025-05-07 11:19:17', '', NULL);
INSERT INTO `gen_table_column` VALUES (95, 12, 'counselor_id', NULL, 'int', 'Long', 'counselorId', '0', '0', '0', '1', '1', '1', '1', 'EQ', 'input', '', 2, 'admin', '2025-05-07 11:19:17', '', NULL);
INSERT INTO `gen_table_column` VALUES (96, 12, 'real_name', NULL, 'varchar(50)', 'String', 'realName', '0', '0', '0', '1', '1', '1', '1', 'LIKE', 'input', '', 3, 'admin', '2025-05-07 11:19:17', '', NULL);
INSERT INTO `gen_table_column` VALUES (97, 12, 'birth_date', NULL, 'date', 'Date', 'birthDate', '0', '0', '0', '1', '1', '1', '1', 'EQ', 'datetime', '', 4, 'admin', '2025-05-07 11:19:17', '', NULL);
INSERT INTO `gen_table_column` VALUES (98, 12, 'gender', NULL, 'varchar(10)', 'String', 'gender', '0', '0', '0', '1', '1', '1', '1', 'EQ', 'input', '', 5, 'admin', '2025-05-07 11:19:17', '', NULL);
INSERT INTO `gen_table_column` VALUES (99, 12, 'contact_info', NULL, 'varchar(100)', 'String', 'contactInfo', '0', '0', '0', '1', '1', '1', '1', 'EQ', 'input', '', 6, 'admin', '2025-05-07 11:19:17', '', NULL);
INSERT INTO `gen_table_column` VALUES (100, 12, 'emergency_real_name', NULL, 'varchar(50)', 'String', 'emergencyRealName', '0', '0', '0', '1', '1', '1', '1', 'LIKE', 'input', '', 7, 'admin', '2025-05-07 11:19:17', '', NULL);
INSERT INTO `gen_table_column` VALUES (101, 12, 'emergency_relationship', NULL, 'varchar(50)', 'String', 'emergencyRelationship', '0', '0', '0', '1', '1', '1', '1', 'EQ', 'input', '', 8, 'admin', '2025-05-07 11:19:17', '', NULL);
INSERT INTO `gen_table_column` VALUES (102, 12, 'emergency_contact', NULL, 'varchar(100)', 'String', 'emergencyContact', '0', '0', '0', '1', '1', '1', '1', 'EQ', 'input', '', 9, 'admin', '2025-05-07 11:19:17', '', NULL);
INSERT INTO `gen_table_column` VALUES (103, 12, 'has_psycho_consulted', NULL, 'enum(\'是\',\'否\')', 'String', 'hasPsychoConsulted', '0', '0', '0', '1', '1', '1', '1', 'EQ', NULL, '', 10, 'admin', '2025-05-07 11:19:17', '', NULL);
INSERT INTO `gen_table_column` VALUES (104, 12, 'has_psycho_treated', NULL, 'enum(\'是\',\'否\')', 'String', 'hasPsychoTreated', '0', '0', '0', '1', '1', '1', '1', 'EQ', NULL, '', 11, 'admin', '2025-05-07 11:19:17', '', NULL);
INSERT INTO `gen_table_column` VALUES (105, 12, 'self_harm_behavior', NULL, 'enum(\'有想过\',\'有做过\',\'均没有\')', 'String', 'selfHarmBehavior', '0', '0', '0', '1', '1', '1', '1', 'EQ', NULL, '', 12, 'admin', '2025-05-07 11:19:17', '', NULL);
INSERT INTO `gen_table_column` VALUES (106, 12, 'problem_types', NULL, 'text', 'String', 'problemTypes', '0', '0', '0', '1', '1', '1', '1', 'EQ', 'textarea', '', 13, 'admin', '2025-05-07 11:19:17', '', NULL);
INSERT INTO `gen_table_column` VALUES (107, 12, 'problem_description', NULL, 'text', 'String', 'problemDescription', '0', '0', '0', '1', '1', '1', '1', 'EQ', 'textarea', '', 14, 'admin', '2025-05-07 11:19:17', '', NULL);
INSERT INTO `gen_table_column` VALUES (108, 12, 'emotional_status', NULL, 'varchar(20)', 'String', 'emotionalStatus', '0', '0', '0', '1', '1', '1', '1', 'EQ', 'radio', '', 15, 'admin', '2025-05-07 11:19:17', '', NULL);
INSERT INTO `gen_table_column` VALUES (109, 12, 'children_count', NULL, 'varchar(20)', 'String', 'childrenCount', '0', '0', '0', '1', '1', '1', '1', 'EQ', 'input', '', 16, 'admin', '2025-05-07 11:19:17', '', NULL);
INSERT INTO `gen_table_column` VALUES (110, 12, 'living_city', NULL, 'varchar(50)', 'String', 'livingCity', '0', '0', '0', '1', '1', '1', '1', 'EQ', 'input', '', 17, 'admin', '2025-05-07 11:19:17', '', NULL);
INSERT INTO `gen_table_column` VALUES (111, 12, 'occupation', NULL, 'varchar(100)', 'String', 'occupation', '0', '0', '0', '1', '1', '1', '1', 'EQ', 'input', '', 18, 'admin', '2025-05-07 11:19:17', '', NULL);
INSERT INTO `gen_table_column` VALUES (112, 12, 'income_level', NULL, 'varchar(100)', 'String', 'incomeLevel', '0', '0', '0', '1', '1', '1', '1', 'EQ', 'input', '', 19, 'admin', '2025-05-07 11:19:17', '', NULL);
INSERT INTO `gen_table_column` VALUES (113, 12, 'education_level', NULL, 'varchar(100)', 'String', 'educationLevel', '0', '0', '0', '1', '1', '1', '1', 'EQ', 'input', '', 20, 'admin', '2025-05-07 11:19:17', '', NULL);
INSERT INTO `gen_table_column` VALUES (114, 12, 'message_to_counselor', NULL, 'text', 'String', 'messageToCounselor', '0', '0', '0', '1', '1', '1', '1', 'EQ', 'textarea', '', 21, 'admin', '2025-05-07 11:19:17', '', NULL);
INSERT INTO `gen_table_column` VALUES (115, 12, 'create_time', NULL, 'datetime', 'Date', 'createTime', '0', '0', '0', '1', NULL, NULL, NULL, 'EQ', 'datetime', '', 22, 'admin', '2025-05-07 11:19:17', '', NULL);

-- ----------------------------
-- Table structure for qrtz_blob_triggers
-- ----------------------------
DROP TABLE IF EXISTS `qrtz_blob_triggers`;
CREATE TABLE `qrtz_blob_triggers`  (
  `sched_name` varchar(120) CHARACTER SET utf8mb3 COLLATE utf8mb3_unicode_ci NOT NULL COMMENT '调度名称',
  `trigger_name` varchar(200) CHARACTER SET utf8mb3 COLLATE utf8mb3_unicode_ci NOT NULL COMMENT 'qrtz_triggers表trigger_name的外键',
  `trigger_group` varchar(200) CHARACTER SET utf8mb3 COLLATE utf8mb3_unicode_ci NOT NULL COMMENT 'qrtz_triggers表trigger_group的外键',
  `blob_data` blob NULL COMMENT '存放持久化Trigger对象',
  PRIMARY KEY (`sched_name`, `trigger_name`, `trigger_group`) USING BTREE,
  CONSTRAINT `qrtz_blob_triggers_ibfk_1` FOREIGN KEY (`sched_name`, `trigger_name`, `trigger_group`) REFERENCES `qrtz_triggers` (`sched_name`, `trigger_name`, `trigger_group`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB CHARACTER SET = utf8mb3 COLLATE = utf8mb3_unicode_ci COMMENT = 'Blob类型的触发器表' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of qrtz_blob_triggers
-- ----------------------------

-- ----------------------------
-- Table structure for qrtz_calendars
-- ----------------------------
DROP TABLE IF EXISTS `qrtz_calendars`;
CREATE TABLE `qrtz_calendars`  (
  `sched_name` varchar(120) CHARACTER SET utf8mb3 COLLATE utf8mb3_unicode_ci NOT NULL COMMENT '调度名称',
  `calendar_name` varchar(200) CHARACTER SET utf8mb3 COLLATE utf8mb3_unicode_ci NOT NULL COMMENT '日历名称',
  `calendar` blob NOT NULL COMMENT '存放持久化calendar对象',
  PRIMARY KEY (`sched_name`, `calendar_name`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8mb3 COLLATE = utf8mb3_unicode_ci COMMENT = '日历信息表' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of qrtz_calendars
-- ----------------------------

-- ----------------------------
-- Table structure for qrtz_cron_triggers
-- ----------------------------
DROP TABLE IF EXISTS `qrtz_cron_triggers`;
CREATE TABLE `qrtz_cron_triggers`  (
  `sched_name` varchar(120) CHARACTER SET utf8mb3 COLLATE utf8mb3_unicode_ci NOT NULL COMMENT '调度名称',
  `trigger_name` varchar(200) CHARACTER SET utf8mb3 COLLATE utf8mb3_unicode_ci NOT NULL COMMENT 'qrtz_triggers表trigger_name的外键',
  `trigger_group` varchar(200) CHARACTER SET utf8mb3 COLLATE utf8mb3_unicode_ci NOT NULL COMMENT 'qrtz_triggers表trigger_group的外键',
  `cron_expression` varchar(200) CHARACTER SET utf8mb3 COLLATE utf8mb3_unicode_ci NOT NULL COMMENT 'cron表达式',
  `time_zone_id` varchar(80) CHARACTER SET utf8mb3 COLLATE utf8mb3_unicode_ci NULL DEFAULT NULL COMMENT '时区',
  PRIMARY KEY (`sched_name`, `trigger_name`, `trigger_group`) USING BTREE,
  CONSTRAINT `qrtz_cron_triggers_ibfk_1` FOREIGN KEY (`sched_name`, `trigger_name`, `trigger_group`) REFERENCES `qrtz_triggers` (`sched_name`, `trigger_name`, `trigger_group`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB CHARACTER SET = utf8mb3 COLLATE = utf8mb3_unicode_ci COMMENT = 'Cron类型的触发器表' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of qrtz_cron_triggers
-- ----------------------------

-- ----------------------------
-- Table structure for qrtz_fired_triggers
-- ----------------------------
DROP TABLE IF EXISTS `qrtz_fired_triggers`;
CREATE TABLE `qrtz_fired_triggers`  (
  `sched_name` varchar(120) CHARACTER SET utf8mb3 COLLATE utf8mb3_unicode_ci NOT NULL COMMENT '调度名称',
  `entry_id` varchar(95) CHARACTER SET utf8mb3 COLLATE utf8mb3_unicode_ci NOT NULL COMMENT '调度器实例id',
  `trigger_name` varchar(200) CHARACTER SET utf8mb3 COLLATE utf8mb3_unicode_ci NOT NULL COMMENT 'qrtz_triggers表trigger_name的外键',
  `trigger_group` varchar(200) CHARACTER SET utf8mb3 COLLATE utf8mb3_unicode_ci NOT NULL COMMENT 'qrtz_triggers表trigger_group的外键',
  `instance_name` varchar(200) CHARACTER SET utf8mb3 COLLATE utf8mb3_unicode_ci NOT NULL COMMENT '调度器实例名',
  `fired_time` bigint NOT NULL COMMENT '触发的时间',
  `sched_time` bigint NOT NULL COMMENT '定时器制定的时间',
  `priority` int NOT NULL COMMENT '优先级',
  `state` varchar(16) CHARACTER SET utf8mb3 COLLATE utf8mb3_unicode_ci NOT NULL COMMENT '状态',
  `job_name` varchar(200) CHARACTER SET utf8mb3 COLLATE utf8mb3_unicode_ci NULL DEFAULT NULL COMMENT '任务名称',
  `job_group` varchar(200) CHARACTER SET utf8mb3 COLLATE utf8mb3_unicode_ci NULL DEFAULT NULL COMMENT '任务组名',
  `is_nonconcurrent` varchar(1) CHARACTER SET utf8mb3 COLLATE utf8mb3_unicode_ci NULL DEFAULT NULL COMMENT '是否并发',
  `requests_recovery` varchar(1) CHARACTER SET utf8mb3 COLLATE utf8mb3_unicode_ci NULL DEFAULT NULL COMMENT '是否接受恢复执行',
  PRIMARY KEY (`sched_name`, `entry_id`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8mb3 COLLATE = utf8mb3_unicode_ci COMMENT = '已触发的触发器表' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of qrtz_fired_triggers
-- ----------------------------

-- ----------------------------
-- Table structure for qrtz_job_details
-- ----------------------------
DROP TABLE IF EXISTS `qrtz_job_details`;
CREATE TABLE `qrtz_job_details`  (
  `sched_name` varchar(120) CHARACTER SET utf8mb3 COLLATE utf8mb3_unicode_ci NOT NULL COMMENT '调度名称',
  `job_name` varchar(200) CHARACTER SET utf8mb3 COLLATE utf8mb3_unicode_ci NOT NULL COMMENT '任务名称',
  `job_group` varchar(200) CHARACTER SET utf8mb3 COLLATE utf8mb3_unicode_ci NOT NULL COMMENT '任务组名',
  `description` varchar(250) CHARACTER SET utf8mb3 COLLATE utf8mb3_unicode_ci NULL DEFAULT NULL COMMENT '相关介绍',
  `job_class_name` varchar(250) CHARACTER SET utf8mb3 COLLATE utf8mb3_unicode_ci NOT NULL COMMENT '执行任务类名称',
  `is_durable` varchar(1) CHARACTER SET utf8mb3 COLLATE utf8mb3_unicode_ci NOT NULL COMMENT '是否持久化',
  `is_nonconcurrent` varchar(1) CHARACTER SET utf8mb3 COLLATE utf8mb3_unicode_ci NOT NULL COMMENT '是否并发',
  `is_update_data` varchar(1) CHARACTER SET utf8mb3 COLLATE utf8mb3_unicode_ci NOT NULL COMMENT '是否更新数据',
  `requests_recovery` varchar(1) CHARACTER SET utf8mb3 COLLATE utf8mb3_unicode_ci NOT NULL COMMENT '是否接受恢复执行',
  `job_data` blob NULL COMMENT '存放持久化job对象',
  PRIMARY KEY (`sched_name`, `job_name`, `job_group`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8mb3 COLLATE = utf8mb3_unicode_ci COMMENT = '任务详细信息表' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of qrtz_job_details
-- ----------------------------

-- ----------------------------
-- Table structure for qrtz_locks
-- ----------------------------
DROP TABLE IF EXISTS `qrtz_locks`;
CREATE TABLE `qrtz_locks`  (
  `sched_name` varchar(120) CHARACTER SET utf8mb3 COLLATE utf8mb3_unicode_ci NOT NULL COMMENT '调度名称',
  `lock_name` varchar(40) CHARACTER SET utf8mb3 COLLATE utf8mb3_unicode_ci NOT NULL COMMENT '悲观锁名称',
  PRIMARY KEY (`sched_name`, `lock_name`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8mb3 COLLATE = utf8mb3_unicode_ci COMMENT = '存储的悲观锁信息表' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of qrtz_locks
-- ----------------------------

-- ----------------------------
-- Table structure for qrtz_paused_trigger_grps
-- ----------------------------
DROP TABLE IF EXISTS `qrtz_paused_trigger_grps`;
CREATE TABLE `qrtz_paused_trigger_grps`  (
  `sched_name` varchar(120) CHARACTER SET utf8mb3 COLLATE utf8mb3_unicode_ci NOT NULL COMMENT '调度名称',
  `trigger_group` varchar(200) CHARACTER SET utf8mb3 COLLATE utf8mb3_unicode_ci NOT NULL COMMENT 'qrtz_triggers表trigger_group的外键',
  PRIMARY KEY (`sched_name`, `trigger_group`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8mb3 COLLATE = utf8mb3_unicode_ci COMMENT = '暂停的触发器表' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of qrtz_paused_trigger_grps
-- ----------------------------

-- ----------------------------
-- Table structure for qrtz_scheduler_state
-- ----------------------------
DROP TABLE IF EXISTS `qrtz_scheduler_state`;
CREATE TABLE `qrtz_scheduler_state`  (
  `sched_name` varchar(120) CHARACTER SET utf8mb3 COLLATE utf8mb3_unicode_ci NOT NULL COMMENT '调度名称',
  `instance_name` varchar(200) CHARACTER SET utf8mb3 COLLATE utf8mb3_unicode_ci NOT NULL COMMENT '实例名称',
  `last_checkin_time` bigint NOT NULL COMMENT '上次检查时间',
  `checkin_interval` bigint NOT NULL COMMENT '检查间隔时间',
  PRIMARY KEY (`sched_name`, `instance_name`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8mb3 COLLATE = utf8mb3_unicode_ci COMMENT = '调度器状态表' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of qrtz_scheduler_state
-- ----------------------------

-- ----------------------------
-- Table structure for qrtz_simple_triggers
-- ----------------------------
DROP TABLE IF EXISTS `qrtz_simple_triggers`;
CREATE TABLE `qrtz_simple_triggers`  (
  `sched_name` varchar(120) CHARACTER SET utf8mb3 COLLATE utf8mb3_unicode_ci NOT NULL COMMENT '调度名称',
  `trigger_name` varchar(200) CHARACTER SET utf8mb3 COLLATE utf8mb3_unicode_ci NOT NULL COMMENT 'qrtz_triggers表trigger_name的外键',
  `trigger_group` varchar(200) CHARACTER SET utf8mb3 COLLATE utf8mb3_unicode_ci NOT NULL COMMENT 'qrtz_triggers表trigger_group的外键',
  `repeat_count` bigint NOT NULL COMMENT '重复的次数统计',
  `repeat_interval` bigint NOT NULL COMMENT '重复的间隔时间',
  `times_triggered` bigint NOT NULL COMMENT '已经触发的次数',
  PRIMARY KEY (`sched_name`, `trigger_name`, `trigger_group`) USING BTREE,
  CONSTRAINT `qrtz_simple_triggers_ibfk_1` FOREIGN KEY (`sched_name`, `trigger_name`, `trigger_group`) REFERENCES `qrtz_triggers` (`sched_name`, `trigger_name`, `trigger_group`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB CHARACTER SET = utf8mb3 COLLATE = utf8mb3_unicode_ci COMMENT = '简单触发器的信息表' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of qrtz_simple_triggers
-- ----------------------------

-- ----------------------------
-- Table structure for qrtz_simprop_triggers
-- ----------------------------
DROP TABLE IF EXISTS `qrtz_simprop_triggers`;
CREATE TABLE `qrtz_simprop_triggers`  (
  `sched_name` varchar(120) CHARACTER SET utf8mb3 COLLATE utf8mb3_unicode_ci NOT NULL COMMENT '调度名称',
  `trigger_name` varchar(200) CHARACTER SET utf8mb3 COLLATE utf8mb3_unicode_ci NOT NULL COMMENT 'qrtz_triggers表trigger_name的外键',
  `trigger_group` varchar(200) CHARACTER SET utf8mb3 COLLATE utf8mb3_unicode_ci NOT NULL COMMENT 'qrtz_triggers表trigger_group的外键',
  `str_prop_1` varchar(512) CHARACTER SET utf8mb3 COLLATE utf8mb3_unicode_ci NULL DEFAULT NULL COMMENT 'String类型的trigger的第一个参数',
  `str_prop_2` varchar(512) CHARACTER SET utf8mb3 COLLATE utf8mb3_unicode_ci NULL DEFAULT NULL COMMENT 'String类型的trigger的第二个参数',
  `str_prop_3` varchar(512) CHARACTER SET utf8mb3 COLLATE utf8mb3_unicode_ci NULL DEFAULT NULL COMMENT 'String类型的trigger的第三个参数',
  `int_prop_1` int NULL DEFAULT NULL COMMENT 'int类型的trigger的第一个参数',
  `int_prop_2` int NULL DEFAULT NULL COMMENT 'int类型的trigger的第二个参数',
  `long_prop_1` bigint NULL DEFAULT NULL COMMENT 'long类型的trigger的第一个参数',
  `long_prop_2` bigint NULL DEFAULT NULL COMMENT 'long类型的trigger的第二个参数',
  `dec_prop_1` decimal(13, 4) NULL DEFAULT NULL COMMENT 'decimal类型的trigger的第一个参数',
  `dec_prop_2` decimal(13, 4) NULL DEFAULT NULL COMMENT 'decimal类型的trigger的第二个参数',
  `bool_prop_1` varchar(1) CHARACTER SET utf8mb3 COLLATE utf8mb3_unicode_ci NULL DEFAULT NULL COMMENT 'Boolean类型的trigger的第一个参数',
  `bool_prop_2` varchar(1) CHARACTER SET utf8mb3 COLLATE utf8mb3_unicode_ci NULL DEFAULT NULL COMMENT 'Boolean类型的trigger的第二个参数',
  PRIMARY KEY (`sched_name`, `trigger_name`, `trigger_group`) USING BTREE,
  CONSTRAINT `qrtz_simprop_triggers_ibfk_1` FOREIGN KEY (`sched_name`, `trigger_name`, `trigger_group`) REFERENCES `qrtz_triggers` (`sched_name`, `trigger_name`, `trigger_group`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB CHARACTER SET = utf8mb3 COLLATE = utf8mb3_unicode_ci COMMENT = '同步机制的行锁表' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of qrtz_simprop_triggers
-- ----------------------------

-- ----------------------------
-- Table structure for qrtz_triggers
-- ----------------------------
DROP TABLE IF EXISTS `qrtz_triggers`;
CREATE TABLE `qrtz_triggers`  (
  `sched_name` varchar(120) CHARACTER SET utf8mb3 COLLATE utf8mb3_unicode_ci NOT NULL COMMENT '调度名称',
  `trigger_name` varchar(200) CHARACTER SET utf8mb3 COLLATE utf8mb3_unicode_ci NOT NULL COMMENT '触发器的名字',
  `trigger_group` varchar(200) CHARACTER SET utf8mb3 COLLATE utf8mb3_unicode_ci NOT NULL COMMENT '触发器所属组的名字',
  `job_name` varchar(200) CHARACTER SET utf8mb3 COLLATE utf8mb3_unicode_ci NOT NULL COMMENT 'qrtz_job_details表job_name的外键',
  `job_group` varchar(200) CHARACTER SET utf8mb3 COLLATE utf8mb3_unicode_ci NOT NULL COMMENT 'qrtz_job_details表job_group的外键',
  `description` varchar(250) CHARACTER SET utf8mb3 COLLATE utf8mb3_unicode_ci NULL DEFAULT NULL COMMENT '相关介绍',
  `next_fire_time` bigint NULL DEFAULT NULL COMMENT '上一次触发时间（毫秒）',
  `prev_fire_time` bigint NULL DEFAULT NULL COMMENT '下一次触发时间（默认为-1表示不触发）',
  `priority` int NULL DEFAULT NULL COMMENT '优先级',
  `trigger_state` varchar(16) CHARACTER SET utf8mb3 COLLATE utf8mb3_unicode_ci NOT NULL COMMENT '触发器状态',
  `trigger_type` varchar(8) CHARACTER SET utf8mb3 COLLATE utf8mb3_unicode_ci NOT NULL COMMENT '触发器的类型',
  `start_time` bigint NOT NULL COMMENT '开始时间',
  `end_time` bigint NULL DEFAULT NULL COMMENT '结束时间',
  `calendar_name` varchar(200) CHARACTER SET utf8mb3 COLLATE utf8mb3_unicode_ci NULL DEFAULT NULL COMMENT '日程表名称',
  `misfire_instr` smallint NULL DEFAULT NULL COMMENT '补偿执行的策略',
  `job_data` blob NULL COMMENT '存放持久化job对象',
  PRIMARY KEY (`sched_name`, `trigger_name`, `trigger_group`) USING BTREE,
  INDEX `sched_name`(`sched_name` ASC, `job_name` ASC, `job_group` ASC) USING BTREE,
  CONSTRAINT `qrtz_triggers_ibfk_1` FOREIGN KEY (`sched_name`, `job_name`, `job_group`) REFERENCES `qrtz_job_details` (`sched_name`, `job_name`, `job_group`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB CHARACTER SET = utf8mb3 COLLATE = utf8mb3_unicode_ci COMMENT = '触发器详细信息表' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of qrtz_triggers
-- ----------------------------

-- ----------------------------
-- Table structure for sys_config
-- ----------------------------
DROP TABLE IF EXISTS `sys_config`;
CREATE TABLE `sys_config`  (
  `config_id` int NOT NULL AUTO_INCREMENT COMMENT '参数主键',
  `config_name` varchar(100) CHARACTER SET utf8mb3 COLLATE utf8mb3_unicode_ci NULL DEFAULT '' COMMENT '参数名称',
  `config_key` varchar(100) CHARACTER SET utf8mb3 COLLATE utf8mb3_unicode_ci NULL DEFAULT '' COMMENT '参数键名',
  `config_value` varchar(500) CHARACTER SET utf8mb3 COLLATE utf8mb3_unicode_ci NULL DEFAULT '' COMMENT '参数键值',
  `config_type` char(1) CHARACTER SET utf8mb3 COLLATE utf8mb3_unicode_ci NULL DEFAULT 'N' COMMENT '系统内置（Y是 N否）',
  `create_by` varchar(64) CHARACTER SET utf8mb3 COLLATE utf8mb3_unicode_ci NULL DEFAULT '' COMMENT '创建者',
  `create_time` datetime NULL DEFAULT NULL COMMENT '创建时间',
  `update_by` varchar(64) CHARACTER SET utf8mb3 COLLATE utf8mb3_unicode_ci NULL DEFAULT '' COMMENT '更新者',
  `update_time` datetime NULL DEFAULT NULL COMMENT '更新时间',
  `remark` varchar(500) CHARACTER SET utf8mb3 COLLATE utf8mb3_unicode_ci NULL DEFAULT NULL COMMENT '备注',
  PRIMARY KEY (`config_id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 6 CHARACTER SET = utf8mb3 COLLATE = utf8mb3_unicode_ci COMMENT = '参数配置表' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of sys_config
-- ----------------------------
INSERT INTO `sys_config` VALUES (1, '主框架页-默认皮肤样式名称', 'sys.index.skinName', 'skin-blue', 'Y', 'admin', '2025-04-27 08:31:47', '', NULL, '蓝色 skin-blue、绿色 skin-green、紫色 skin-purple、红色 skin-red、黄色 skin-yellow');
INSERT INTO `sys_config` VALUES (2, '用户管理-账号初始密码', 'sys.user.initPassword', '123456', 'Y', 'admin', '2025-04-27 08:31:47', '', NULL, '初始化密码 123456');
INSERT INTO `sys_config` VALUES (3, '主框架页-侧边栏主题', 'sys.index.sideTheme', 'theme-dark', 'Y', 'admin', '2025-04-27 08:31:47', '', NULL, '深色主题theme-dark，浅色主题theme-light');
INSERT INTO `sys_config` VALUES (4, '账号自助-验证码开关', 'sys.account.captchaEnabled', 'true', 'Y', 'admin', '2025-04-27 08:31:47', '', NULL, '是否开启验证码功能（true开启，false关闭）');
INSERT INTO `sys_config` VALUES (5, '账号自助-是否开启用户注册功能', 'sys.account.registerUser', 'false', 'Y', 'admin', '2025-04-27 08:31:47', '', NULL, '是否开启注册用户功能（true开启，false关闭）');
INSERT INTO `sys_config` VALUES (6, '用户登录-黑名单列表', 'sys.login.blackIPList', '', 'Y', 'admin', '2025-04-27 08:31:47', '', NULL, '设置登录IP黑名单限制，多个匹配项以;分隔，支持匹配（*通配、网段）');

-- ----------------------------
-- Table structure for sys_dept
-- ----------------------------
DROP TABLE IF EXISTS `sys_dept`;
CREATE TABLE `sys_dept`  (
  `dept_id` bigint NOT NULL AUTO_INCREMENT COMMENT '部门id',
  `parent_id` bigint NULL DEFAULT 0 COMMENT '父部门id',
  `ancestors` varchar(50) CHARACTER SET utf8mb3 COLLATE utf8mb3_unicode_ci NULL DEFAULT '' COMMENT '祖级列表',
  `dept_name` varchar(30) CHARACTER SET utf8mb3 COLLATE utf8mb3_unicode_ci NULL DEFAULT '' COMMENT '部门名称',
  `order_num` int NULL DEFAULT 0 COMMENT '显示顺序',
  `leader` varchar(20) CHARACTER SET utf8mb3 COLLATE utf8mb3_unicode_ci NULL DEFAULT NULL COMMENT '负责人',
  `phone` varchar(11) CHARACTER SET utf8mb3 COLLATE utf8mb3_unicode_ci NULL DEFAULT NULL COMMENT '联系电话',
  `email` varchar(50) CHARACTER SET utf8mb3 COLLATE utf8mb3_unicode_ci NULL DEFAULT NULL COMMENT '邮箱',
  `status` char(1) CHARACTER SET utf8mb3 COLLATE utf8mb3_unicode_ci NULL DEFAULT '0' COMMENT '部门状态（0正常 1停用）',
  `del_flag` char(1) CHARACTER SET utf8mb3 COLLATE utf8mb3_unicode_ci NULL DEFAULT '0' COMMENT '删除标志（0代表存在 2代表删除）',
  `create_by` varchar(64) CHARACTER SET utf8mb3 COLLATE utf8mb3_unicode_ci NULL DEFAULT '' COMMENT '创建者',
  `create_time` datetime NULL DEFAULT NULL COMMENT '创建时间',
  `update_by` varchar(64) CHARACTER SET utf8mb3 COLLATE utf8mb3_unicode_ci NULL DEFAULT '' COMMENT '更新者',
  `update_time` datetime NULL DEFAULT NULL COMMENT '更新时间',
  PRIMARY KEY (`dept_id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 109 CHARACTER SET = utf8mb3 COLLATE = utf8mb3_unicode_ci COMMENT = '部门表' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of sys_dept
-- ----------------------------
INSERT INTO `sys_dept` VALUES (100, 0, '0', '若依科技', 0, '若依', '15888888888', 'ry@qq.com', '0', '0', 'admin', '2025-04-27 08:31:44', '', NULL);
INSERT INTO `sys_dept` VALUES (101, 100, '0,100', '深圳总公司', 1, '若依', '15888888888', 'ry@qq.com', '0', '0', 'admin', '2025-04-27 08:31:44', '', NULL);
INSERT INTO `sys_dept` VALUES (102, 100, '0,100', '长沙分公司', 2, '若依', '15888888888', 'ry@qq.com', '0', '0', 'admin', '2025-04-27 08:31:44', '', NULL);
INSERT INTO `sys_dept` VALUES (103, 101, '0,100,101', '研发部门', 1, '若依', '15888888888', 'ry@qq.com', '0', '0', 'admin', '2025-04-27 08:31:44', '', NULL);
INSERT INTO `sys_dept` VALUES (104, 101, '0,100,101', '市场部门', 2, '若依', '15888888888', 'ry@qq.com', '0', '0', 'admin', '2025-04-27 08:31:45', '', NULL);
INSERT INTO `sys_dept` VALUES (105, 101, '0,100,101', '测试部门', 3, '若依', '15888888888', 'ry@qq.com', '0', '0', 'admin', '2025-04-27 08:31:45', '', NULL);
INSERT INTO `sys_dept` VALUES (106, 101, '0,100,101', '财务部门', 4, '若依', '15888888888', 'ry@qq.com', '0', '0', 'admin', '2025-04-27 08:31:45', '', NULL);
INSERT INTO `sys_dept` VALUES (107, 101, '0,100,101', '运维部门', 5, '若依', '15888888888', 'ry@qq.com', '0', '0', 'admin', '2025-04-27 08:31:45', '', NULL);
INSERT INTO `sys_dept` VALUES (108, 102, '0,100,102', '市场部门', 1, '若依', '15888888888', 'ry@qq.com', '0', '0', 'admin', '2025-04-27 08:31:45', '', NULL);
INSERT INTO `sys_dept` VALUES (109, 102, '0,100,102', '财务部门', 2, '若依', '15888888888', 'ry@qq.com', '0', '0', 'admin', '2025-04-27 08:31:45', '', NULL);

-- ----------------------------
-- Table structure for sys_dict_data
-- ----------------------------
DROP TABLE IF EXISTS `sys_dict_data`;
CREATE TABLE `sys_dict_data`  (
  `dict_code` bigint NOT NULL AUTO_INCREMENT COMMENT '字典编码',
  `dict_sort` int NULL DEFAULT 0 COMMENT '字典排序',
  `dict_label` varchar(100) CHARACTER SET utf8mb3 COLLATE utf8mb3_unicode_ci NULL DEFAULT '' COMMENT '字典标签',
  `dict_value` varchar(100) CHARACTER SET utf8mb3 COLLATE utf8mb3_unicode_ci NULL DEFAULT '' COMMENT '字典键值',
  `dict_type` varchar(100) CHARACTER SET utf8mb3 COLLATE utf8mb3_unicode_ci NULL DEFAULT '' COMMENT '字典类型',
  `css_class` varchar(100) CHARACTER SET utf8mb3 COLLATE utf8mb3_unicode_ci NULL DEFAULT NULL COMMENT '样式属性（其他样式扩展）',
  `list_class` varchar(100) CHARACTER SET utf8mb3 COLLATE utf8mb3_unicode_ci NULL DEFAULT NULL COMMENT '表格回显样式',
  `is_default` char(1) CHARACTER SET utf8mb3 COLLATE utf8mb3_unicode_ci NULL DEFAULT 'N' COMMENT '是否默认（Y是 N否）',
  `status` char(1) CHARACTER SET utf8mb3 COLLATE utf8mb3_unicode_ci NULL DEFAULT '0' COMMENT '状态（0正常 1停用）',
  `create_by` varchar(64) CHARACTER SET utf8mb3 COLLATE utf8mb3_unicode_ci NULL DEFAULT '' COMMENT '创建者',
  `create_time` datetime NULL DEFAULT NULL COMMENT '创建时间',
  `update_by` varchar(64) CHARACTER SET utf8mb3 COLLATE utf8mb3_unicode_ci NULL DEFAULT '' COMMENT '更新者',
  `update_time` datetime NULL DEFAULT NULL COMMENT '更新时间',
  `remark` varchar(500) CHARACTER SET utf8mb3 COLLATE utf8mb3_unicode_ci NULL DEFAULT NULL COMMENT '备注',
  PRIMARY KEY (`dict_code`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 29 CHARACTER SET = utf8mb3 COLLATE = utf8mb3_unicode_ci COMMENT = '字典数据表' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of sys_dict_data
-- ----------------------------
INSERT INTO `sys_dict_data` VALUES (1, 1, '男', '0', 'sys_user_sex', '', '', 'Y', '0', 'admin', '2025-04-27 08:31:46', '', NULL, '性别男');
INSERT INTO `sys_dict_data` VALUES (2, 2, '女', '1', 'sys_user_sex', '', '', 'N', '0', 'admin', '2025-04-27 08:31:46', '', NULL, '性别女');
INSERT INTO `sys_dict_data` VALUES (3, 3, '未知', '2', 'sys_user_sex', '', '', 'N', '0', 'admin', '2025-04-27 08:31:46', '', NULL, '性别未知');
INSERT INTO `sys_dict_data` VALUES (4, 1, '显示', '0', 'sys_show_hide', '', 'primary', 'Y', '0', 'admin', '2025-04-27 08:31:46', '', NULL, '显示菜单');
INSERT INTO `sys_dict_data` VALUES (5, 2, '隐藏', '1', 'sys_show_hide', '', 'danger', 'N', '0', 'admin', '2025-04-27 08:31:46', '', NULL, '隐藏菜单');
INSERT INTO `sys_dict_data` VALUES (6, 1, '正常', '0', 'sys_normal_disable', '', 'primary', 'Y', '0', 'admin', '2025-04-27 08:31:46', '', NULL, '正常状态');
INSERT INTO `sys_dict_data` VALUES (7, 2, '停用', '1', 'sys_normal_disable', '', 'danger', 'N', '0', 'admin', '2025-04-27 08:31:46', '', NULL, '停用状态');
INSERT INTO `sys_dict_data` VALUES (8, 1, '正常', '0', 'sys_job_status', '', 'primary', 'Y', '0', 'admin', '2025-04-27 08:31:46', '', NULL, '正常状态');
INSERT INTO `sys_dict_data` VALUES (9, 2, '暂停', '1', 'sys_job_status', '', 'danger', 'N', '0', 'admin', '2025-04-27 08:31:46', '', NULL, '停用状态');
INSERT INTO `sys_dict_data` VALUES (10, 1, '默认', 'DEFAULT', 'sys_job_group', '', '', 'Y', '0', 'admin', '2025-04-27 08:31:46', '', NULL, '默认分组');
INSERT INTO `sys_dict_data` VALUES (11, 2, '系统', 'SYSTEM', 'sys_job_group', '', '', 'N', '0', 'admin', '2025-04-27 08:31:46', '', NULL, '系统分组');
INSERT INTO `sys_dict_data` VALUES (12, 1, '是', 'Y', 'sys_yes_no', '', 'primary', 'Y', '0', 'admin', '2025-04-27 08:31:46', '', NULL, '系统默认是');
INSERT INTO `sys_dict_data` VALUES (13, 2, '否', 'N', 'sys_yes_no', '', 'danger', 'N', '0', 'admin', '2025-04-27 08:31:46', '', NULL, '系统默认否');
INSERT INTO `sys_dict_data` VALUES (14, 1, '通知', '1', 'sys_notice_type', '', 'warning', 'Y', '0', 'admin', '2025-04-27 08:31:46', '', NULL, '通知');
INSERT INTO `sys_dict_data` VALUES (15, 2, '公告', '2', 'sys_notice_type', '', 'success', 'N', '0', 'admin', '2025-04-27 08:31:46', '', NULL, '公告');
INSERT INTO `sys_dict_data` VALUES (16, 1, '正常', '0', 'sys_notice_status', '', 'primary', 'Y', '0', 'admin', '2025-04-27 08:31:46', '', NULL, '正常状态');
INSERT INTO `sys_dict_data` VALUES (17, 2, '关闭', '1', 'sys_notice_status', '', 'danger', 'N', '0', 'admin', '2025-04-27 08:31:46', '', NULL, '关闭状态');
INSERT INTO `sys_dict_data` VALUES (18, 99, '其他', '0', 'sys_oper_type', '', 'info', 'N', '0', 'admin', '2025-04-27 08:31:46', '', NULL, '其他操作');
INSERT INTO `sys_dict_data` VALUES (19, 1, '新增', '1', 'sys_oper_type', '', 'info', 'N', '0', 'admin', '2025-04-27 08:31:46', '', NULL, '新增操作');
INSERT INTO `sys_dict_data` VALUES (20, 2, '修改', '2', 'sys_oper_type', '', 'info', 'N', '0', 'admin', '2025-04-27 08:31:46', '', NULL, '修改操作');
INSERT INTO `sys_dict_data` VALUES (21, 3, '删除', '3', 'sys_oper_type', '', 'danger', 'N', '0', 'admin', '2025-04-27 08:31:46', '', NULL, '删除操作');
INSERT INTO `sys_dict_data` VALUES (22, 4, '授权', '4', 'sys_oper_type', '', 'primary', 'N', '0', 'admin', '2025-04-27 08:31:46', '', NULL, '授权操作');
INSERT INTO `sys_dict_data` VALUES (23, 5, '导出', '5', 'sys_oper_type', '', 'warning', 'N', '0', 'admin', '2025-04-27 08:31:46', '', NULL, '导出操作');
INSERT INTO `sys_dict_data` VALUES (24, 6, '导入', '6', 'sys_oper_type', '', 'warning', 'N', '0', 'admin', '2025-04-27 08:31:46', '', NULL, '导入操作');
INSERT INTO `sys_dict_data` VALUES (25, 7, '强退', '7', 'sys_oper_type', '', 'danger', 'N', '0', 'admin', '2025-04-27 08:31:47', '', NULL, '强退操作');
INSERT INTO `sys_dict_data` VALUES (26, 8, '生成代码', '8', 'sys_oper_type', '', 'warning', 'N', '0', 'admin', '2025-04-27 08:31:47', '', NULL, '生成操作');
INSERT INTO `sys_dict_data` VALUES (27, 9, '清空数据', '9', 'sys_oper_type', '', 'danger', 'N', '0', 'admin', '2025-04-27 08:31:47', '', NULL, '清空操作');
INSERT INTO `sys_dict_data` VALUES (28, 1, '成功', '0', 'sys_common_status', '', 'primary', 'N', '0', 'admin', '2025-04-27 08:31:47', '', NULL, '正常状态');
INSERT INTO `sys_dict_data` VALUES (29, 2, '失败', '1', 'sys_common_status', '', 'danger', 'N', '0', 'admin', '2025-04-27 08:31:47', '', NULL, '停用状态');

-- ----------------------------
-- Table structure for sys_dict_type
-- ----------------------------
DROP TABLE IF EXISTS `sys_dict_type`;
CREATE TABLE `sys_dict_type`  (
  `dict_id` bigint NOT NULL AUTO_INCREMENT COMMENT '字典主键',
  `dict_name` varchar(100) CHARACTER SET utf8mb3 COLLATE utf8mb3_unicode_ci NULL DEFAULT '' COMMENT '字典名称',
  `dict_type` varchar(100) CHARACTER SET utf8mb3 COLLATE utf8mb3_unicode_ci NULL DEFAULT '' COMMENT '字典类型',
  `status` char(1) CHARACTER SET utf8mb3 COLLATE utf8mb3_unicode_ci NULL DEFAULT '0' COMMENT '状态（0正常 1停用）',
  `create_by` varchar(64) CHARACTER SET utf8mb3 COLLATE utf8mb3_unicode_ci NULL DEFAULT '' COMMENT '创建者',
  `create_time` datetime NULL DEFAULT NULL COMMENT '创建时间',
  `update_by` varchar(64) CHARACTER SET utf8mb3 COLLATE utf8mb3_unicode_ci NULL DEFAULT '' COMMENT '更新者',
  `update_time` datetime NULL DEFAULT NULL COMMENT '更新时间',
  `remark` varchar(500) CHARACTER SET utf8mb3 COLLATE utf8mb3_unicode_ci NULL DEFAULT NULL COMMENT '备注',
  PRIMARY KEY (`dict_id`) USING BTREE,
  UNIQUE INDEX `dict_type`(`dict_type` ASC) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 10 CHARACTER SET = utf8mb3 COLLATE = utf8mb3_unicode_ci COMMENT = '字典类型表' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of sys_dict_type
-- ----------------------------
INSERT INTO `sys_dict_type` VALUES (1, '用户性别', 'sys_user_sex', '0', 'admin', '2025-04-27 08:31:45', '', NULL, '用户性别列表');
INSERT INTO `sys_dict_type` VALUES (2, '菜单状态', 'sys_show_hide', '0', 'admin', '2025-04-27 08:31:45', '', NULL, '菜单状态列表');
INSERT INTO `sys_dict_type` VALUES (3, '系统开关', 'sys_normal_disable', '0', 'admin', '2025-04-27 08:31:45', '', NULL, '系统开关列表');
INSERT INTO `sys_dict_type` VALUES (4, '任务状态', 'sys_job_status', '0', 'admin', '2025-04-27 08:31:45', '', NULL, '任务状态列表');
INSERT INTO `sys_dict_type` VALUES (5, '任务分组', 'sys_job_group', '0', 'admin', '2025-04-27 08:31:45', '', NULL, '任务分组列表');
INSERT INTO `sys_dict_type` VALUES (6, '系统是否', 'sys_yes_no', '0', 'admin', '2025-04-27 08:31:46', '', NULL, '系统是否列表');
INSERT INTO `sys_dict_type` VALUES (7, '通知类型', 'sys_notice_type', '0', 'admin', '2025-04-27 08:31:46', '', NULL, '通知类型列表');
INSERT INTO `sys_dict_type` VALUES (8, '通知状态', 'sys_notice_status', '0', 'admin', '2025-04-27 08:31:46', '', NULL, '通知状态列表');
INSERT INTO `sys_dict_type` VALUES (9, '操作类型', 'sys_oper_type', '0', 'admin', '2025-04-27 08:31:46', '', NULL, '操作类型列表');
INSERT INTO `sys_dict_type` VALUES (10, '系统状态', 'sys_common_status', '0', 'admin', '2025-04-27 08:31:46', '', NULL, '登录状态列表');

-- ----------------------------
-- Table structure for sys_job
-- ----------------------------
DROP TABLE IF EXISTS `sys_job`;
CREATE TABLE `sys_job`  (
  `job_id` bigint NOT NULL AUTO_INCREMENT COMMENT '任务ID',
  `job_name` varchar(64) CHARACTER SET utf8mb3 COLLATE utf8mb3_unicode_ci NOT NULL DEFAULT '' COMMENT '任务名称',
  `job_group` varchar(64) CHARACTER SET utf8mb3 COLLATE utf8mb3_unicode_ci NOT NULL DEFAULT 'DEFAULT' COMMENT '任务组名',
  `invoke_target` varchar(500) CHARACTER SET utf8mb3 COLLATE utf8mb3_unicode_ci NOT NULL COMMENT '调用目标字符串',
  `cron_expression` varchar(255) CHARACTER SET utf8mb3 COLLATE utf8mb3_unicode_ci NULL DEFAULT '' COMMENT 'cron执行表达式',
  `misfire_policy` varchar(20) CHARACTER SET utf8mb3 COLLATE utf8mb3_unicode_ci NULL DEFAULT '3' COMMENT '计划执行错误策略（1立即执行 2执行一次 3放弃执行）',
  `concurrent` char(1) CHARACTER SET utf8mb3 COLLATE utf8mb3_unicode_ci NULL DEFAULT '1' COMMENT '是否并发执行（0允许 1禁止）',
  `status` char(1) CHARACTER SET utf8mb3 COLLATE utf8mb3_unicode_ci NULL DEFAULT '0' COMMENT '状态（0正常 1暂停）',
  `create_by` varchar(64) CHARACTER SET utf8mb3 COLLATE utf8mb3_unicode_ci NULL DEFAULT '' COMMENT '创建者',
  `create_time` datetime NULL DEFAULT NULL COMMENT '创建时间',
  `update_by` varchar(64) CHARACTER SET utf8mb3 COLLATE utf8mb3_unicode_ci NULL DEFAULT '' COMMENT '更新者',
  `update_time` datetime NULL DEFAULT NULL COMMENT '更新时间',
  `remark` varchar(500) CHARACTER SET utf8mb3 COLLATE utf8mb3_unicode_ci NULL DEFAULT '' COMMENT '备注信息',
  PRIMARY KEY (`job_id`, `job_name`, `job_group`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 3 CHARACTER SET = utf8mb3 COLLATE = utf8mb3_unicode_ci COMMENT = '定时任务调度表' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of sys_job
-- ----------------------------
INSERT INTO `sys_job` VALUES (1, '系统默认（无参）', 'DEFAULT', 'ryTask.ryNoParams', '0/10 * * * * ?', '3', '1', '1', 'admin', '2025-04-27 08:31:47', '', NULL, '');
INSERT INTO `sys_job` VALUES (2, '系统默认（有参）', 'DEFAULT', 'ryTask.ryParams(\'ry\')', '0/15 * * * * ?', '3', '1', '1', 'admin', '2025-04-27 08:31:47', '', NULL, '');
INSERT INTO `sys_job` VALUES (3, '系统默认（多参）', 'DEFAULT', 'ryTask.ryMultipleParams(\'ry\', true, 2000L, 316.50D, 100)', '0/20 * * * * ?', '3', '1', '1', 'admin', '2025-04-27 08:31:47', '', NULL, '');

-- ----------------------------
-- Table structure for sys_job_log
-- ----------------------------
DROP TABLE IF EXISTS `sys_job_log`;
CREATE TABLE `sys_job_log`  (
  `job_log_id` bigint NOT NULL AUTO_INCREMENT COMMENT '任务日志ID',
  `job_name` varchar(64) CHARACTER SET utf8mb3 COLLATE utf8mb3_unicode_ci NOT NULL COMMENT '任务名称',
  `job_group` varchar(64) CHARACTER SET utf8mb3 COLLATE utf8mb3_unicode_ci NOT NULL COMMENT '任务组名',
  `invoke_target` varchar(500) CHARACTER SET utf8mb3 COLLATE utf8mb3_unicode_ci NOT NULL COMMENT '调用目标字符串',
  `job_message` varchar(500) CHARACTER SET utf8mb3 COLLATE utf8mb3_unicode_ci NULL DEFAULT NULL COMMENT '日志信息',
  `status` char(1) CHARACTER SET utf8mb3 COLLATE utf8mb3_unicode_ci NULL DEFAULT '0' COMMENT '执行状态（0正常 1失败）',
  `exception_info` varchar(2000) CHARACTER SET utf8mb3 COLLATE utf8mb3_unicode_ci NULL DEFAULT '' COMMENT '异常信息',
  `create_time` datetime NULL DEFAULT NULL COMMENT '创建时间',
  PRIMARY KEY (`job_log_id`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8mb3 COLLATE = utf8mb3_unicode_ci COMMENT = '定时任务调度日志表' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of sys_job_log
-- ----------------------------

-- ----------------------------
-- Table structure for sys_logininfor
-- ----------------------------
DROP TABLE IF EXISTS `sys_logininfor`;
CREATE TABLE `sys_logininfor`  (
  `info_id` bigint NOT NULL AUTO_INCREMENT COMMENT '访问ID',
  `user_name` varchar(50) CHARACTER SET utf8mb3 COLLATE utf8mb3_unicode_ci NULL DEFAULT '' COMMENT '用户账号',
  `ipaddr` varchar(128) CHARACTER SET utf8mb3 COLLATE utf8mb3_unicode_ci NULL DEFAULT '' COMMENT '登录IP地址',
  `login_location` varchar(255) CHARACTER SET utf8mb3 COLLATE utf8mb3_unicode_ci NULL DEFAULT '' COMMENT '登录地点',
  `browser` varchar(50) CHARACTER SET utf8mb3 COLLATE utf8mb3_unicode_ci NULL DEFAULT '' COMMENT '浏览器类型',
  `os` varchar(50) CHARACTER SET utf8mb3 COLLATE utf8mb3_unicode_ci NULL DEFAULT '' COMMENT '操作系统',
  `status` char(1) CHARACTER SET utf8mb3 COLLATE utf8mb3_unicode_ci NULL DEFAULT '0' COMMENT '登录状态（0成功 1失败）',
  `msg` varchar(255) CHARACTER SET utf8mb3 COLLATE utf8mb3_unicode_ci NULL DEFAULT '' COMMENT '提示消息',
  `login_time` datetime NULL DEFAULT NULL COMMENT '访问时间',
  PRIMARY KEY (`info_id`) USING BTREE,
  INDEX `idx_sys_logininfor_s`(`status` ASC) USING BTREE,
  INDEX `idx_sys_logininfor_lt`(`login_time` ASC) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 108 CHARACTER SET = utf8mb3 COLLATE = utf8mb3_unicode_ci COMMENT = '系统访问记录' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of sys_logininfor
-- ----------------------------
INSERT INTO `sys_logininfor` VALUES (100, 'admin', '127.0.0.1', '内网IP', 'Chrome 13', 'Windows 10', '0', '登录成功', '2025-05-06 09:28:59');
INSERT INTO `sys_logininfor` VALUES (101, 'admin', '127.0.0.1', '内网IP', 'Chrome 13', 'Windows 10', '0', '登录成功', '2025-05-07 10:53:21');
INSERT INTO `sys_logininfor` VALUES (102, 'admin', '127.0.0.1', '内网IP', 'Chrome 13', 'Windows 10', '0', '退出成功', '2025-05-07 11:46:25');
INSERT INTO `sys_logininfor` VALUES (103, 'admin', '127.0.0.1', '内网IP', 'Chrome 13', 'Windows 10', '0', '登录成功', '2025-05-07 11:46:49');
INSERT INTO `sys_logininfor` VALUES (104, 'admin', '127.0.0.1', '内网IP', 'Chrome 13', 'Windows 10', '0', '登录成功', '2025-05-07 14:36:38');
INSERT INTO `sys_logininfor` VALUES (105, 'admin', '127.0.0.1', '内网IP', 'Chrome 13', 'Windows 10', '0', '退出成功', '2025-05-07 14:41:50');
INSERT INTO `sys_logininfor` VALUES (106, 'admin', '127.0.0.1', '内网IP', 'Chrome 13', 'Windows 10', '0', '登录成功', '2025-05-07 14:42:03');
INSERT INTO `sys_logininfor` VALUES (107, 'admin', '127.0.0.1', '内网IP', 'Chrome 13', 'Windows 10', '0', '登录成功', '2025-05-07 15:51:09');
INSERT INTO `sys_logininfor` VALUES (108, 'admin', '127.0.0.1', '内网IP', 'Chrome 13', 'Windows 10', '0', '登录成功', '2025-05-07 16:36:53');

-- ----------------------------
-- Table structure for sys_menu
-- ----------------------------
DROP TABLE IF EXISTS `sys_menu`;
CREATE TABLE `sys_menu`  (
  `menu_id` bigint NOT NULL AUTO_INCREMENT COMMENT '菜单ID',
  `menu_name` varchar(50) CHARACTER SET utf8mb3 COLLATE utf8mb3_unicode_ci NOT NULL COMMENT '菜单名称',
  `parent_id` bigint NULL DEFAULT 0 COMMENT '父菜单ID',
  `order_num` int NULL DEFAULT 0 COMMENT '显示顺序',
  `path` varchar(200) CHARACTER SET utf8mb3 COLLATE utf8mb3_unicode_ci NULL DEFAULT '' COMMENT '路由地址',
  `component` varchar(255) CHARACTER SET utf8mb3 COLLATE utf8mb3_unicode_ci NULL DEFAULT NULL COMMENT '组件路径',
  `query` varchar(255) CHARACTER SET utf8mb3 COLLATE utf8mb3_unicode_ci NULL DEFAULT NULL COMMENT '路由参数',
  `route_name` varchar(50) CHARACTER SET utf8mb3 COLLATE utf8mb3_unicode_ci NULL DEFAULT '' COMMENT '路由名称',
  `is_frame` int NULL DEFAULT 1 COMMENT '是否为外链（0是 1否）',
  `is_cache` int NULL DEFAULT 0 COMMENT '是否缓存（0缓存 1不缓存）',
  `menu_type` char(1) CHARACTER SET utf8mb3 COLLATE utf8mb3_unicode_ci NULL DEFAULT '' COMMENT '菜单类型（M目录 C菜单 F按钮）',
  `visible` char(1) CHARACTER SET utf8mb3 COLLATE utf8mb3_unicode_ci NULL DEFAULT '0' COMMENT '菜单状态（0显示 1隐藏）',
  `status` char(1) CHARACTER SET utf8mb3 COLLATE utf8mb3_unicode_ci NULL DEFAULT '0' COMMENT '菜单状态（0正常 1停用）',
  `perms` varchar(100) CHARACTER SET utf8mb3 COLLATE utf8mb3_unicode_ci NULL DEFAULT NULL COMMENT '权限标识',
  `icon` varchar(100) CHARACTER SET utf8mb3 COLLATE utf8mb3_unicode_ci NULL DEFAULT '#' COMMENT '菜单图标',
  `create_by` varchar(64) CHARACTER SET utf8mb3 COLLATE utf8mb3_unicode_ci NULL DEFAULT '' COMMENT '创建者',
  `create_time` datetime NULL DEFAULT NULL COMMENT '创建时间',
  `update_by` varchar(64) CHARACTER SET utf8mb3 COLLATE utf8mb3_unicode_ci NULL DEFAULT '' COMMENT '更新者',
  `update_time` datetime NULL DEFAULT NULL COMMENT '更新时间',
  `remark` varchar(500) CHARACTER SET utf8mb3 COLLATE utf8mb3_unicode_ci NULL DEFAULT '' COMMENT '备注',
  PRIMARY KEY (`menu_id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 2000 CHARACTER SET = utf8mb3 COLLATE = utf8mb3_unicode_ci COMMENT = '菜单权限表' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of sys_menu
-- ----------------------------
INSERT INTO `sys_menu` VALUES (1, '系统管理', 0, 1, 'system', NULL, '', '', 1, 0, 'M', '0', '0', '', 'system', 'admin', '2025-04-27 08:31:45', '', NULL, '系统管理目录');
INSERT INTO `sys_menu` VALUES (2, '系统监控', 0, 2, 'monitor', NULL, '', '', 1, 0, 'M', '0', '0', '', 'monitor', 'admin', '2025-04-27 08:31:45', '', NULL, '系统监控目录');
INSERT INTO `sys_menu` VALUES (3, '系统工具', 0, 3, 'tool', NULL, '', '', 1, 0, 'M', '0', '0', '', 'tool', 'admin', '2025-04-27 08:31:45', '', NULL, '系统工具目录');
INSERT INTO `sys_menu` VALUES (4, '若依官网', 0, 4, 'http://ruoyi.vip', NULL, '', '', 0, 0, 'M', '0', '0', '', 'guide', 'admin', '2025-04-27 08:31:45', '', NULL, '若依官网地址');
INSERT INTO `sys_menu` VALUES (100, '用户管理', 1, 1, 'user', 'system/user/index', '', '', 1, 0, 'C', '0', '0', 'system:user:list', 'user', 'admin', '2025-04-27 08:31:45', '', NULL, '用户管理菜单');
INSERT INTO `sys_menu` VALUES (101, '角色管理', 1, 2, 'role', 'system/role/index', '', '', 1, 0, 'C', '0', '0', 'system:role:list', 'peoples', 'admin', '2025-04-27 08:31:45', '', NULL, '角色管理菜单');
INSERT INTO `sys_menu` VALUES (102, '菜单管理', 1, 3, 'menu', 'system/menu/index', '', '', 1, 0, 'C', '0', '0', 'system:menu:list', 'tree-table', 'admin', '2025-04-27 08:31:45', '', NULL, '菜单管理菜单');
INSERT INTO `sys_menu` VALUES (103, '部门管理', 1, 4, 'dept', 'system/dept/index', '', '', 1, 0, 'C', '0', '0', 'system:dept:list', 'tree', 'admin', '2025-04-27 08:31:45', '', NULL, '部门管理菜单');
INSERT INTO `sys_menu` VALUES (104, '岗位管理', 1, 5, 'post', 'system/post/index', '', '', 1, 0, 'C', '0', '0', 'system:post:list', 'post', 'admin', '2025-04-27 08:31:45', '', NULL, '岗位管理菜单');
INSERT INTO `sys_menu` VALUES (105, '字典管理', 1, 6, 'dict', 'system/dict/index', '', '', 1, 0, 'C', '0', '0', 'system:dict:list', 'dict', 'admin', '2025-04-27 08:31:45', '', NULL, '字典管理菜单');
INSERT INTO `sys_menu` VALUES (106, '参数设置', 1, 7, 'config', 'system/config/index', '', '', 1, 0, 'C', '0', '0', 'system:config:list', 'edit', 'admin', '2025-04-27 08:31:45', '', NULL, '参数设置菜单');
INSERT INTO `sys_menu` VALUES (107, '通知公告', 1, 8, 'notice', 'system/notice/index', '', '', 1, 0, 'C', '0', '0', 'system:notice:list', 'message', 'admin', '2025-04-27 08:31:45', '', NULL, '通知公告菜单');
INSERT INTO `sys_menu` VALUES (108, '日志管理', 1, 9, 'log', '', '', '', 1, 0, 'M', '0', '0', '', 'log', 'admin', '2025-04-27 08:31:45', '', NULL, '日志管理菜单');
INSERT INTO `sys_menu` VALUES (109, '在线用户', 2, 1, 'online', 'monitor/online/index', '', '', 1, 0, 'C', '0', '0', 'monitor:online:list', 'online', 'admin', '2025-04-27 08:31:45', '', NULL, '在线用户菜单');
INSERT INTO `sys_menu` VALUES (110, '定时任务', 2, 2, 'job', 'monitor/job/index', '', '', 1, 0, 'C', '0', '0', 'monitor:job:list', 'job', 'admin', '2025-04-27 08:31:45', '', NULL, '定时任务菜单');
INSERT INTO `sys_menu` VALUES (111, '数据监控', 2, 3, 'druid', 'monitor/druid/index', '', '', 1, 0, 'C', '0', '0', 'monitor:druid:list', 'druid', 'admin', '2025-04-27 08:31:45', '', NULL, '数据监控菜单');
INSERT INTO `sys_menu` VALUES (112, '服务监控', 2, 4, 'server', 'monitor/server/index', '', '', 1, 0, 'C', '0', '0', 'monitor:server:list', 'server', 'admin', '2025-04-27 08:31:45', '', NULL, '服务监控菜单');
INSERT INTO `sys_menu` VALUES (113, '缓存监控', 2, 5, 'cache', 'monitor/cache/index', '', '', 1, 0, 'C', '0', '0', 'monitor:cache:list', 'redis', 'admin', '2025-04-27 08:31:45', '', NULL, '缓存监控菜单');
INSERT INTO `sys_menu` VALUES (114, '缓存列表', 2, 6, 'cacheList', 'monitor/cache/list', '', '', 1, 0, 'C', '0', '0', 'monitor:cache:list', 'redis-list', 'admin', '2025-04-27 08:31:45', '', NULL, '缓存列表菜单');
INSERT INTO `sys_menu` VALUES (115, '表单构建', 3, 1, 'build', 'tool/build/index', '', '', 1, 0, 'C', '0', '0', 'tool:build:list', 'build', 'admin', '2025-04-27 08:31:45', '', NULL, '表单构建菜单');
INSERT INTO `sys_menu` VALUES (116, '代码生成', 3, 2, 'gen', 'tool/gen/index', '', '', 1, 0, 'C', '0', '0', 'tool:gen:list', 'code', 'admin', '2025-04-27 08:31:45', '', NULL, '代码生成菜单');
INSERT INTO `sys_menu` VALUES (117, '系统接口', 3, 3, 'swagger', 'tool/swagger/index', '', '', 1, 0, 'C', '0', '0', 'tool:swagger:list', 'swagger', 'admin', '2025-04-27 08:31:45', '', NULL, '系统接口菜单');
INSERT INTO `sys_menu` VALUES (500, '操作日志', 108, 1, 'operlog', 'monitor/operlog/index', '', '', 1, 0, 'C', '0', '0', 'monitor:operlog:list', 'form', 'admin', '2025-04-27 08:31:45', '', NULL, '操作日志菜单');
INSERT INTO `sys_menu` VALUES (501, '登录日志', 108, 2, 'logininfor', 'monitor/logininfor/index', '', '', 1, 0, 'C', '0', '0', 'monitor:logininfor:list', 'logininfor', 'admin', '2025-04-27 08:31:45', '', NULL, '登录日志菜单');
INSERT INTO `sys_menu` VALUES (1000, '用户查询', 100, 1, '', '', '', '', 1, 0, 'F', '0', '0', 'system:user:query', '#', 'admin', '2025-04-27 08:31:45', '', NULL, '');
INSERT INTO `sys_menu` VALUES (1001, '用户新增', 100, 2, '', '', '', '', 1, 0, 'F', '0', '0', 'system:user:add', '#', 'admin', '2025-04-27 08:31:45', '', NULL, '');
INSERT INTO `sys_menu` VALUES (1002, '用户修改', 100, 3, '', '', '', '', 1, 0, 'F', '0', '0', 'system:user:edit', '#', 'admin', '2025-04-27 08:31:45', '', NULL, '');
INSERT INTO `sys_menu` VALUES (1003, '用户删除', 100, 4, '', '', '', '', 1, 0, 'F', '0', '0', 'system:user:remove', '#', 'admin', '2025-04-27 08:31:45', '', NULL, '');
INSERT INTO `sys_menu` VALUES (1004, '用户导出', 100, 5, '', '', '', '', 1, 0, 'F', '0', '0', 'system:user:export', '#', 'admin', '2025-04-27 08:31:45', '', NULL, '');
INSERT INTO `sys_menu` VALUES (1005, '用户导入', 100, 6, '', '', '', '', 1, 0, 'F', '0', '0', 'system:user:import', '#', 'admin', '2025-04-27 08:31:45', '', NULL, '');
INSERT INTO `sys_menu` VALUES (1006, '重置密码', 100, 7, '', '', '', '', 1, 0, 'F', '0', '0', 'system:user:resetPwd', '#', 'admin', '2025-04-27 08:31:45', '', NULL, '');
INSERT INTO `sys_menu` VALUES (1007, '角色查询', 101, 1, '', '', '', '', 1, 0, 'F', '0', '0', 'system:role:query', '#', 'admin', '2025-04-27 08:31:45', '', NULL, '');
INSERT INTO `sys_menu` VALUES (1008, '角色新增', 101, 2, '', '', '', '', 1, 0, 'F', '0', '0', 'system:role:add', '#', 'admin', '2025-04-27 08:31:45', '', NULL, '');
INSERT INTO `sys_menu` VALUES (1009, '角色修改', 101, 3, '', '', '', '', 1, 0, 'F', '0', '0', 'system:role:edit', '#', 'admin', '2025-04-27 08:31:45', '', NULL, '');
INSERT INTO `sys_menu` VALUES (1010, '角色删除', 101, 4, '', '', '', '', 1, 0, 'F', '0', '0', 'system:role:remove', '#', 'admin', '2025-04-27 08:31:45', '', NULL, '');
INSERT INTO `sys_menu` VALUES (1011, '角色导出', 101, 5, '', '', '', '', 1, 0, 'F', '0', '0', 'system:role:export', '#', 'admin', '2025-04-27 08:31:45', '', NULL, '');
INSERT INTO `sys_menu` VALUES (1012, '菜单查询', 102, 1, '', '', '', '', 1, 0, 'F', '0', '0', 'system:menu:query', '#', 'admin', '2025-04-27 08:31:45', '', NULL, '');
INSERT INTO `sys_menu` VALUES (1013, '菜单新增', 102, 2, '', '', '', '', 1, 0, 'F', '0', '0', 'system:menu:add', '#', 'admin', '2025-04-27 08:31:45', '', NULL, '');
INSERT INTO `sys_menu` VALUES (1014, '菜单修改', 102, 3, '', '', '', '', 1, 0, 'F', '0', '0', 'system:menu:edit', '#', 'admin', '2025-04-27 08:31:45', '', NULL, '');
INSERT INTO `sys_menu` VALUES (1015, '菜单删除', 102, 4, '', '', '', '', 1, 0, 'F', '0', '0', 'system:menu:remove', '#', 'admin', '2025-04-27 08:31:45', '', NULL, '');
INSERT INTO `sys_menu` VALUES (1016, '部门查询', 103, 1, '', '', '', '', 1, 0, 'F', '0', '0', 'system:dept:query', '#', 'admin', '2025-04-27 08:31:45', '', NULL, '');
INSERT INTO `sys_menu` VALUES (1017, '部门新增', 103, 2, '', '', '', '', 1, 0, 'F', '0', '0', 'system:dept:add', '#', 'admin', '2025-04-27 08:31:45', '', NULL, '');
INSERT INTO `sys_menu` VALUES (1018, '部门修改', 103, 3, '', '', '', '', 1, 0, 'F', '0', '0', 'system:dept:edit', '#', 'admin', '2025-04-27 08:31:45', '', NULL, '');
INSERT INTO `sys_menu` VALUES (1019, '部门删除', 103, 4, '', '', '', '', 1, 0, 'F', '0', '0', 'system:dept:remove', '#', 'admin', '2025-04-27 08:31:45', '', NULL, '');
INSERT INTO `sys_menu` VALUES (1020, '岗位查询', 104, 1, '', '', '', '', 1, 0, 'F', '0', '0', 'system:post:query', '#', 'admin', '2025-04-27 08:31:45', '', NULL, '');
INSERT INTO `sys_menu` VALUES (1021, '岗位新增', 104, 2, '', '', '', '', 1, 0, 'F', '0', '0', 'system:post:add', '#', 'admin', '2025-04-27 08:31:45', '', NULL, '');
INSERT INTO `sys_menu` VALUES (1022, '岗位修改', 104, 3, '', '', '', '', 1, 0, 'F', '0', '0', 'system:post:edit', '#', 'admin', '2025-04-27 08:31:45', '', NULL, '');
INSERT INTO `sys_menu` VALUES (1023, '岗位删除', 104, 4, '', '', '', '', 1, 0, 'F', '0', '0', 'system:post:remove', '#', 'admin', '2025-04-27 08:31:45', '', NULL, '');
INSERT INTO `sys_menu` VALUES (1024, '岗位导出', 104, 5, '', '', '', '', 1, 0, 'F', '0', '0', 'system:post:export', '#', 'admin', '2025-04-27 08:31:45', '', NULL, '');
INSERT INTO `sys_menu` VALUES (1025, '字典查询', 105, 1, '#', '', '', '', 1, 0, 'F', '0', '0', 'system:dict:query', '#', 'admin', '2025-04-27 08:31:45', '', NULL, '');
INSERT INTO `sys_menu` VALUES (1026, '字典新增', 105, 2, '#', '', '', '', 1, 0, 'F', '0', '0', 'system:dict:add', '#', 'admin', '2025-04-27 08:31:45', '', NULL, '');
INSERT INTO `sys_menu` VALUES (1027, '字典修改', 105, 3, '#', '', '', '', 1, 0, 'F', '0', '0', 'system:dict:edit', '#', 'admin', '2025-04-27 08:31:45', '', NULL, '');
INSERT INTO `sys_menu` VALUES (1028, '字典删除', 105, 4, '#', '', '', '', 1, 0, 'F', '0', '0', 'system:dict:remove', '#', 'admin', '2025-04-27 08:31:45', '', NULL, '');
INSERT INTO `sys_menu` VALUES (1029, '字典导出', 105, 5, '#', '', '', '', 1, 0, 'F', '0', '0', 'system:dict:export', '#', 'admin', '2025-04-27 08:31:45', '', NULL, '');
INSERT INTO `sys_menu` VALUES (1030, '参数查询', 106, 1, '#', '', '', '', 1, 0, 'F', '0', '0', 'system:config:query', '#', 'admin', '2025-04-27 08:31:45', '', NULL, '');
INSERT INTO `sys_menu` VALUES (1031, '参数新增', 106, 2, '#', '', '', '', 1, 0, 'F', '0', '0', 'system:config:add', '#', 'admin', '2025-04-27 08:31:45', '', NULL, '');
INSERT INTO `sys_menu` VALUES (1032, '参数修改', 106, 3, '#', '', '', '', 1, 0, 'F', '0', '0', 'system:config:edit', '#', 'admin', '2025-04-27 08:31:45', '', NULL, '');
INSERT INTO `sys_menu` VALUES (1033, '参数删除', 106, 4, '#', '', '', '', 1, 0, 'F', '0', '0', 'system:config:remove', '#', 'admin', '2025-04-27 08:31:45', '', NULL, '');
INSERT INTO `sys_menu` VALUES (1034, '参数导出', 106, 5, '#', '', '', '', 1, 0, 'F', '0', '0', 'system:config:export', '#', 'admin', '2025-04-27 08:31:45', '', NULL, '');
INSERT INTO `sys_menu` VALUES (1035, '公告查询', 107, 1, '#', '', '', '', 1, 0, 'F', '0', '0', 'system:notice:query', '#', 'admin', '2025-04-27 08:31:45', '', NULL, '');
INSERT INTO `sys_menu` VALUES (1036, '公告新增', 107, 2, '#', '', '', '', 1, 0, 'F', '0', '0', 'system:notice:add', '#', 'admin', '2025-04-27 08:31:45', '', NULL, '');
INSERT INTO `sys_menu` VALUES (1037, '公告修改', 107, 3, '#', '', '', '', 1, 0, 'F', '0', '0', 'system:notice:edit', '#', 'admin', '2025-04-27 08:31:45', '', NULL, '');
INSERT INTO `sys_menu` VALUES (1038, '公告删除', 107, 4, '#', '', '', '', 1, 0, 'F', '0', '0', 'system:notice:remove', '#', 'admin', '2025-04-27 08:31:45', '', NULL, '');
INSERT INTO `sys_menu` VALUES (1039, '操作查询', 500, 1, '#', '', '', '', 1, 0, 'F', '0', '0', 'monitor:operlog:query', '#', 'admin', '2025-04-27 08:31:45', '', NULL, '');
INSERT INTO `sys_menu` VALUES (1040, '操作删除', 500, 2, '#', '', '', '', 1, 0, 'F', '0', '0', 'monitor:operlog:remove', '#', 'admin', '2025-04-27 08:31:45', '', NULL, '');
INSERT INTO `sys_menu` VALUES (1041, '日志导出', 500, 3, '#', '', '', '', 1, 0, 'F', '0', '0', 'monitor:operlog:export', '#', 'admin', '2025-04-27 08:31:45', '', NULL, '');
INSERT INTO `sys_menu` VALUES (1042, '登录查询', 501, 1, '#', '', '', '', 1, 0, 'F', '0', '0', 'monitor:logininfor:query', '#', 'admin', '2025-04-27 08:31:45', '', NULL, '');
INSERT INTO `sys_menu` VALUES (1043, '登录删除', 501, 2, '#', '', '', '', 1, 0, 'F', '0', '0', 'monitor:logininfor:remove', '#', 'admin', '2025-04-27 08:31:45', '', NULL, '');
INSERT INTO `sys_menu` VALUES (1044, '日志导出', 501, 3, '#', '', '', '', 1, 0, 'F', '0', '0', 'monitor:logininfor:export', '#', 'admin', '2025-04-27 08:31:45', '', NULL, '');
INSERT INTO `sys_menu` VALUES (1045, '账户解锁', 501, 4, '#', '', '', '', 1, 0, 'F', '0', '0', 'monitor:logininfor:unlock', '#', 'admin', '2025-04-27 08:31:45', '', NULL, '');
INSERT INTO `sys_menu` VALUES (1046, '在线查询', 109, 1, '#', '', '', '', 1, 0, 'F', '0', '0', 'monitor:online:query', '#', 'admin', '2025-04-27 08:31:45', '', NULL, '');
INSERT INTO `sys_menu` VALUES (1047, '批量强退', 109, 2, '#', '', '', '', 1, 0, 'F', '0', '0', 'monitor:online:batchLogout', '#', 'admin', '2025-04-27 08:31:45', '', NULL, '');
INSERT INTO `sys_menu` VALUES (1048, '单条强退', 109, 3, '#', '', '', '', 1, 0, 'F', '0', '0', 'monitor:online:forceLogout', '#', 'admin', '2025-04-27 08:31:45', '', NULL, '');
INSERT INTO `sys_menu` VALUES (1049, '任务查询', 110, 1, '#', '', '', '', 1, 0, 'F', '0', '0', 'monitor:job:query', '#', 'admin', '2025-04-27 08:31:45', '', NULL, '');
INSERT INTO `sys_menu` VALUES (1050, '任务新增', 110, 2, '#', '', '', '', 1, 0, 'F', '0', '0', 'monitor:job:add', '#', 'admin', '2025-04-27 08:31:45', '', NULL, '');
INSERT INTO `sys_menu` VALUES (1051, '任务修改', 110, 3, '#', '', '', '', 1, 0, 'F', '0', '0', 'monitor:job:edit', '#', 'admin', '2025-04-27 08:31:45', '', NULL, '');
INSERT INTO `sys_menu` VALUES (1052, '任务删除', 110, 4, '#', '', '', '', 1, 0, 'F', '0', '0', 'monitor:job:remove', '#', 'admin', '2025-04-27 08:31:45', '', NULL, '');
INSERT INTO `sys_menu` VALUES (1053, '状态修改', 110, 5, '#', '', '', '', 1, 0, 'F', '0', '0', 'monitor:job:changeStatus', '#', 'admin', '2025-04-27 08:31:45', '', NULL, '');
INSERT INTO `sys_menu` VALUES (1054, '任务导出', 110, 6, '#', '', '', '', 1, 0, 'F', '0', '0', 'monitor:job:export', '#', 'admin', '2025-04-27 08:31:45', '', NULL, '');
INSERT INTO `sys_menu` VALUES (1055, '生成查询', 116, 1, '#', '', '', '', 1, 0, 'F', '0', '0', 'tool:gen:query', '#', 'admin', '2025-04-27 08:31:45', '', NULL, '');
INSERT INTO `sys_menu` VALUES (1056, '生成修改', 116, 2, '#', '', '', '', 1, 0, 'F', '0', '0', 'tool:gen:edit', '#', 'admin', '2025-04-27 08:31:45', '', NULL, '');
INSERT INTO `sys_menu` VALUES (1057, '生成删除', 116, 3, '#', '', '', '', 1, 0, 'F', '0', '0', 'tool:gen:remove', '#', 'admin', '2025-04-27 08:31:45', '', NULL, '');
INSERT INTO `sys_menu` VALUES (1058, '导入代码', 116, 4, '#', '', '', '', 1, 0, 'F', '0', '0', 'tool:gen:import', '#', 'admin', '2025-04-27 08:31:45', '', NULL, '');
INSERT INTO `sys_menu` VALUES (1059, '预览代码', 116, 5, '#', '', '', '', 1, 0, 'F', '0', '0', 'tool:gen:preview', '#', 'admin', '2025-04-27 08:31:45', '', NULL, '');
INSERT INTO `sys_menu` VALUES (1060, '生成代码', 116, 6, '#', '', '', '', 1, 0, 'F', '0', '0', 'tool:gen:code', '#', 'admin', '2025-04-27 08:31:45', '', NULL, '');
INSERT INTO `sys_menu` VALUES (2000, '咨询师管理', 0, 5, 'counselors', NULL, NULL, '', 1, 0, 'M', '0', '0', NULL, 'user', 'admin', '2025-05-07 15:06:38', '', NULL, '');

-- ----------------------------
-- Table structure for sys_notice
-- ----------------------------
DROP TABLE IF EXISTS `sys_notice`;
CREATE TABLE `sys_notice`  (
  `notice_id` int NOT NULL AUTO_INCREMENT COMMENT '公告ID',
  `notice_title` varchar(50) CHARACTER SET utf8mb3 COLLATE utf8mb3_unicode_ci NOT NULL COMMENT '公告标题',
  `notice_type` char(1) CHARACTER SET utf8mb3 COLLATE utf8mb3_unicode_ci NOT NULL COMMENT '公告类型（1通知 2公告）',
  `notice_content` longblob NULL COMMENT '公告内容',
  `status` char(1) CHARACTER SET utf8mb3 COLLATE utf8mb3_unicode_ci NULL DEFAULT '0' COMMENT '公告状态（0正常 1关闭）',
  `create_by` varchar(64) CHARACTER SET utf8mb3 COLLATE utf8mb3_unicode_ci NULL DEFAULT '' COMMENT '创建者',
  `create_time` datetime NULL DEFAULT NULL COMMENT '创建时间',
  `update_by` varchar(64) CHARACTER SET utf8mb3 COLLATE utf8mb3_unicode_ci NULL DEFAULT '' COMMENT '更新者',
  `update_time` datetime NULL DEFAULT NULL COMMENT '更新时间',
  `remark` varchar(255) CHARACTER SET utf8mb3 COLLATE utf8mb3_unicode_ci NULL DEFAULT NULL COMMENT '备注',
  PRIMARY KEY (`notice_id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 2 CHARACTER SET = utf8mb3 COLLATE = utf8mb3_unicode_ci COMMENT = '通知公告表' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of sys_notice
-- ----------------------------
INSERT INTO `sys_notice` VALUES (1, '温馨提醒：2018-07-01 若依新版本发布啦', '2', 0xE696B0E78988E69CACE58685E5AEB9, '0', 'admin', '2025-04-27 08:31:47', '', NULL, '管理员');
INSERT INTO `sys_notice` VALUES (2, '维护通知：2018-07-01 若依系统凌晨维护', '1', 0xE7BBB4E68AA4E58685E5AEB9, '0', 'admin', '2025-04-27 08:31:47', '', NULL, '管理员');

-- ----------------------------
-- Table structure for sys_oper_log
-- ----------------------------
DROP TABLE IF EXISTS `sys_oper_log`;
CREATE TABLE `sys_oper_log`  (
  `oper_id` bigint NOT NULL AUTO_INCREMENT COMMENT '日志主键',
  `title` varchar(50) CHARACTER SET utf8mb3 COLLATE utf8mb3_unicode_ci NULL DEFAULT '' COMMENT '模块标题',
  `business_type` int NULL DEFAULT 0 COMMENT '业务类型（0其它 1新增 2修改 3删除）',
  `method` varchar(200) CHARACTER SET utf8mb3 COLLATE utf8mb3_unicode_ci NULL DEFAULT '' COMMENT '方法名称',
  `request_method` varchar(10) CHARACTER SET utf8mb3 COLLATE utf8mb3_unicode_ci NULL DEFAULT '' COMMENT '请求方式',
  `operator_type` int NULL DEFAULT 0 COMMENT '操作类别（0其它 1后台用户 2手机端用户）',
  `oper_name` varchar(50) CHARACTER SET utf8mb3 COLLATE utf8mb3_unicode_ci NULL DEFAULT '' COMMENT '操作人员',
  `dept_name` varchar(50) CHARACTER SET utf8mb3 COLLATE utf8mb3_unicode_ci NULL DEFAULT '' COMMENT '部门名称',
  `oper_url` varchar(255) CHARACTER SET utf8mb3 COLLATE utf8mb3_unicode_ci NULL DEFAULT '' COMMENT '请求URL',
  `oper_ip` varchar(128) CHARACTER SET utf8mb3 COLLATE utf8mb3_unicode_ci NULL DEFAULT '' COMMENT '主机地址',
  `oper_location` varchar(255) CHARACTER SET utf8mb3 COLLATE utf8mb3_unicode_ci NULL DEFAULT '' COMMENT '操作地点',
  `oper_param` varchar(2000) CHARACTER SET utf8mb3 COLLATE utf8mb3_unicode_ci NULL DEFAULT '' COMMENT '请求参数',
  `json_result` varchar(2000) CHARACTER SET utf8mb3 COLLATE utf8mb3_unicode_ci NULL DEFAULT '' COMMENT '返回参数',
  `status` int NULL DEFAULT 0 COMMENT '操作状态（0正常 1异常）',
  `error_msg` varchar(2000) CHARACTER SET utf8mb3 COLLATE utf8mb3_unicode_ci NULL DEFAULT '' COMMENT '错误消息',
  `oper_time` datetime NULL DEFAULT NULL COMMENT '操作时间',
  `cost_time` bigint NULL DEFAULT 0 COMMENT '消耗时间',
  PRIMARY KEY (`oper_id`) USING BTREE,
  INDEX `idx_sys_oper_log_bt`(`business_type` ASC) USING BTREE,
  INDEX `idx_sys_oper_log_s`(`status` ASC) USING BTREE,
  INDEX `idx_sys_oper_log_ot`(`oper_time` ASC) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 112 CHARACTER SET = utf8mb3 COLLATE = utf8mb3_unicode_ci COMMENT = '操作日志记录' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of sys_oper_log
-- ----------------------------
INSERT INTO `sys_oper_log` VALUES (100, '创建表', 0, 'com.ruoyi.generator.controller.GenController.createTableSave()', 'POST', 1, 'admin', '研发部门', '/tool/gen/createTable', '127.0.0.1', '内网IP', '{\"sql\":\"CREATE TABLE ur_user (\\n    user_id INT AUTO_INCREMENT PRIMARY KEY,\\n    nickname VARCHAR(50),\\n    gender VARCHAR(10),\\n    age INT,\\n    phone_number VARCHAR(20) UNIQUE,\\n    email VARCHAR(100) UNIQUE,\\n    account VARCHAR(50) UNIQUE,\\n    password VARCHAR(100),\\n    avatar VARCHAR(255),\\n    introduction TEXT,\\n    create_time DATETIME,\\n    last_login_time DATETIME\\n);\\n\\n-- 咨询师表\\nCREATE TABLE ur_counselor (\\n    counselor_id INT AUTO_INCREMENT PRIMARY KEY,\\n    name VARCHAR(100) NOT NULL,\\n    picture_url VARCHAR(255),\\n    personal_introduction TEXT,\\n    expertise_areas TEXT,\\n    years_of_practice INT,\\n    supported_types TEXT,\\n    teaching_price DECIMAL(10, 2),\\n    counselor_level VARCHAR(50),\\n    counselor_type VARCHAR(100),\\n    tags TEXT,\\n    rating DECIMAL(3, 2),\\n    total_practice_hours INT,\\n    good_at_problems TEXT,\\n    treatment_methods TEXT,\\n    consultation_duration INT,\\n    professional_qualification VARCHAR(255),\\n    certification_certificate_url VARCHAR(255),\\n    working_hours TEXT\\n);\\n\\n-- 预约时间表\\nCREATE TABLE ur_appointment (\\n    appointment_id INT AUTO_INCREMENT PRIMARY KEY,\\n    counselor_id INT,\\n    user_id INT,\\n    start_time DATETIME,\\n    end_time DATETIME,\\n    FOREIGN KEY (counselor_id) REFERENCES ur_counselor(counselor_id),\\n    FOREIGN KEY (user_id) REFERENCES ur_user(user_id)\\n);\\n\\n-- 评价表\\nCREATE TABLE ur_review (\\n    review_id INT AUTO_INCREMENT PRIMARY KEY,\\n    counselor_id INT,\\n    user_id INT,\\n    review_content TEXT,\\n    review_time DATETIME,\\n    FOREIGN KEY (counselor_id) REFERENCES ur_counselor(counselor_id),\\n    FOREIGN KEY (user_id) REFERENCES ur_user(user_id)\\n);\\n\\n-- 地区表\\nCREATE TABLE ur_region (\\n    region_id INT AUTO_INCREMENT PRIMARY KEY,\\n    region_name VARCHAR(100)\\n);\\n\\n-- 咨询师-地区关联表\\nCREATE TABLE ur_counselor_region (\\n    id INT AUTO_INCREMENT PRIMARY KEY,\\n    counselor_id INT,\\n    region_id INT,\\n    FOREIGN KEY (counselor_id) REFERENCES ur_counselor(counselor_id),\\n    FOREIG', '{\"msg\":\"创建表结构异常\",\"code\":500}', 0, NULL, '2025-05-07 11:02:29', 8);
INSERT INTO `sys_oper_log` VALUES (101, '创建表', 0, 'com.ruoyi.generator.controller.GenController.createTableSave()', 'POST', 1, 'admin', '研发部门', '/tool/gen/createTable', '127.0.0.1', '内网IP', '{\"sql\":\"CREATE TABLE ur_user (\\n    user_id INT AUTO_INCREMENT PRIMARY KEY,\\n    nickname VARCHAR(50),\\n    gender VARCHAR(10),\\n    age INT,\\n    phone_number VARCHAR(20) UNIQUE,\\n    email VARCHAR(100) UNIQUE,\\n    account VARCHAR(50) UNIQUE,\\n    password VARCHAR(100),\\n    avatar VARCHAR(255),\\n    introduction TEXT,\\n    create_time DATETIME,\\n    last_login_time DATETIME\\n);\\n\\nCREATE TABLE ur_counselor (\\n    counselor_id INT AUTO_INCREMENT PRIMARY KEY,\\n    name VARCHAR(100) NOT NULL,\\n    picture_url VARCHAR(255),\\n    personal_introduction TEXT,\\n    expertise_areas TEXT,\\n    years_of_practice INT,\\n    supported_types TEXT,\\n    teaching_price DECIMAL(10, 2),\\n    counselor_level VARCHAR(50),\\n    counselor_type VARCHAR(100),\\n    tags TEXT,\\n    rating DECIMAL(3, 2),\\n    total_practice_hours INT,\\n    good_at_problems TEXT,\\n    treatment_methods TEXT,\\n    consultation_duration INT,\\n    professional_qualification VARCHAR(255),\\n    certification_certificate_url VARCHAR(255),\\n    working_hours TEXT\\n);\\n\\nCREATE TABLE ur_appointment (\\n    appointment_id INT AUTO_INCREMENT PRIMARY KEY,\\n    counselor_id INT,\\n    user_id INT,\\n    start_time DATETIME,\\n    end_time DATETIME,\\n    FOREIGN KEY (counselor_id) REFERENCES ur_counselor(counselor_id),\\n    FOREIGN KEY (user_id) REFERENCES ur_user(user_id)\\n);\\n\\nCREATE TABLE ur_review (\\n    review_id INT AUTO_INCREMENT PRIMARY KEY,\\n    counselor_id INT,\\n    user_id INT,\\n    review_content TEXT,\\n    review_time DATETIME,\\n    FOREIGN KEY (counselor_id) REFERENCES ur_counselor(counselor_id),\\n    FOREIGN KEY (user_id) REFERENCES ur_user(user_id)\\n);\\n\\nCREATE TABLE ur_region (\\n    region_id INT AUTO_INCREMENT PRIMARY KEY,\\n    region_name VARCHAR(100)\\n);\\n\\nCREATE TABLE ur_counselor_region (\\n    id INT AUTO_INCREMENT PRIMARY KEY,\\n    counselor_id INT,\\n    region_id INT,\\n    FOREIGN KEY (counselor_id) REFERENCES ur_counselor(counselor_id),\\n    FOREIGN KEY (region_id) REFERENCES ur_region(region_id)', '{\"msg\":\"创建表结构异常\",\"code\":500}', 0, NULL, '2025-05-07 11:03:11', 4);
INSERT INTO `sys_oper_log` VALUES (102, '创建表', 0, 'com.ruoyi.generator.controller.GenController.createTableSave()', 'POST', 1, 'admin', '研发部门', '/tool/gen/createTable', '127.0.0.1', '内网IP', '{\"sql\":\"CREATE TABLE ur_user (\\n    user_id INT AUTO_INCREMENT PRIMARY KEY,\\n    nickname VARCHAR(50),\\n    gender VARCHAR(10),\\n    age INT,\\n    phone_number VARCHAR(20) UNIQUE,\\n    email VARCHAR(100) UNIQUE,\\n    account VARCHAR(50) UNIQUE,\\n    password VARCHAR(100),\\n    avatar VARCHAR(255),\\n    introduction TEXT,\\n    create_time DATETIME,\\n    last_login_time DATETIME\\n);\"}', '{\"msg\":\"创建表结构异常\",\"code\":500}', 0, NULL, '2025-05-07 11:03:21', 2);
INSERT INTO `sys_oper_log` VALUES (103, '创建表', 0, 'com.ruoyi.generator.controller.GenController.createTableSave()', 'POST', 1, 'admin', '研发部门', '/tool/gen/createTable', '127.0.0.1', '内网IP', '{\"sql\":\"CREATE TABLE ur_user (\\n    user_id INT AUTO_INCREMENT PRIMARY KEY,\\n    nickname VARCHAR(50),\\n    gender VARCHAR(10),\\n    age INT,\\n    phone_number VARCHAR(20) UNIQUE,\\n    email VARCHAR(100) UNIQUE,\\n    account VARCHAR(50) UNIQUE,\\n    password VARCHAR(100),\\n    avatar VARCHAR(255),\\n    introduction TEXT,\\n    create_time DATETIME,\\n    last_login_time DATETIME\\n);\"}', '{\"msg\":\"创建表结构异常\",\"code\":500}', 0, NULL, '2025-05-07 11:14:42', 2);
INSERT INTO `sys_oper_log` VALUES (104, '创建表', 0, 'com.ruoyi.generator.controller.GenController.createTableSave()', 'POST', 1, 'admin', '研发部门', '/tool/gen/createTable', '127.0.0.1', '内网IP', '{\"sql\":\"CREATE TABLE ur_user (\\n    user_id INT AUTO_INCREMENT PRIMARY KEY,\\n    nickname VARCHAR(50),\\n    gender VARCHAR(10),\\n    age INT,\\n    phone_number VARCHAR(20) UNIQUE,\\n    email VARCHAR(100) UNIQUE,\\n    account VARCHAR(50) UNIQUE,\\n    password VARCHAR(100),\\n    avatar VARCHAR(255),CREATE TABLE ur_user (\\n    user_id BIGINT(20) NOT NULL AUTO_INCREMENT COMMENT \'用户ID\',\\n    nickname VARCHAR(30) NOT NULL COMMENT \'用户昵称\',\\n    gender CHAR(1) DEFAULT \'0\' COMMENT \'性别（0男 1女 2未知）\',\\n    age INT(3) DEFAULT NULL COMMENT \'年龄\',\\n    phone_number VARCHAR(11) NOT NULL COMMENT \'手机号码\',\\n    email VARCHAR(50) DEFAULT \'\' COMMENT \'用户邮箱\',\\n    account VARCHAR(30) NOT NULL COMMENT \'登录账号\',\\n    password VARCHAR(100) DEFAULT \'\' COMMENT \'密码\',\\n    avatar VARCHAR(100) DEFAULT \'\' COMMENT \'头像路径\',\\n    introduction VARCHAR(500) DEFAULT NULL COMMENT \'个人简介\',\\n    status CHAR(1) DEFAULT \'0\' COMMENT \'帐号状态（0正常 1停用）\',\\n    del_flag CHAR(1) DEFAULT \'0\' COMMENT \'删除标志（0代表存在 2代表删除）\',\\n    login_ip VARCHAR(50) DEFAULT \'\' COMMENT \'最后登录IP\',\\n    login_date DATETIME DEFAULT NULL COMMENT \'最后登录时间\',\\n    create_by VARCHAR(64) DEFAULT \'\' COMMENT \'创建者\',\\n    create_time DATETIME COMMENT \'创建时间\',\\n    update_by VARCHAR(64) DEFAULT \'\' COMMENT \'更新者\',\\n    update_time DATETIME COMMENT \'更新时间\',\\n    remark VARCHAR(500) DEFAULT NULL COMMENT \'备注\',\\n    PRIMARY KEY (user_id),\\n    UNIQUE KEY (phone_number),\\n    UNIQUE KEY (email),\\n    UNIQUE KEY (account)\\n) ENGINE=InnoDB AUTO_INCREMENT=100 DEFAULT CHARSET=utf8mb4 COMMENT=\'用户信息表\';\\n    introduction TEXT,\\n    create_time DATETIME,\\n    last_login_time DATETIME\\n);\"}', '{\"msg\":\"创建表结构异常\",\"code\":500}', 0, NULL, '2025-05-07 11:15:47', 2);
INSERT INTO `sys_oper_log` VALUES (105, '创建表', 0, 'com.ruoyi.generator.controller.GenController.createTableSave()', 'POST', 1, 'admin', '研发部门', '/tool/gen/createTable', '127.0.0.1', '内网IP', '{\"sql\":\"CREATE TABLE ur_user (\\n    user_id INT AUTO_INCREMENT PRIMARY KEY,\\n    nickname VARCHAR(50),\\n    gender VARCHAR(10),\\n    age INT,\\n    phone_number VARCHAR(20) UNIQUE,\\n    email VARCHAR(100) UNIQUE,\\n    account VARCHAR(50) UNIQUE,\\n    password VARCHAR(100),\\n    avatar VARCHAR(255),CREATE TABLE ur_user (\\n    user_id BIGINT(20) NOT NULL AUTO_INCREMENT COMMENT \'用户ID\',\\n    nickname VARCHAR(30) NOT NULL COMMENT \'用户昵称\',\\n    gender CHAR(1) DEFAULT \'0\' COMMENT \'性别（0男 1女 2未知）\',\\n    age INT(3) DEFAULT NULL COMMENT \'年龄\',\\n    phone_number VARCHAR(11) NOT NULL COMMENT \'手机号码\',\\n    email VARCHAR(50) DEFAULT \'\' COMMENT \'用户邮箱\',\\n    account VARCHAR(30) NOT NULL COMMENT \'登录账号\',\\n    password VARCHAR(100) DEFAULT \'\' COMMENT \'密码\',\\n    avatar VARCHAR(100) DEFAULT \'\' COMMENT \'头像路径\',\\n    introduction VARCHAR(500) DEFAULT NULL COMMENT \'个人简介\',\\n    status CHAR(1) DEFAULT \'0\' COMMENT \'帐号状态（0正常 1停用）\',\\n    del_flag CHAR(1) DEFAULT \'0\' COMMENT \'删除标志（0代表存在 2代表删除）\',\\n    login_ip VARCHAR(50) DEFAULT \'\' COMMENT \'最后登录IP\',\\n    login_date DATETIME DEFAULT NULL COMMENT \'最后登录时间\',\\n    create_by VARCHAR(64) DEFAULT \'\' COMMENT \'创建者\',\\n    create_time DATETIME COMMENT \'创建时间\',\\n    update_by VARCHAR(64) DEFAULT \'\' COMMENT \'更新者\',\\n    update_time DATETIME COMMENT \'更新时间\',\\n    remark VARCHAR(500) DEFAULT NULL COMMENT \'备注\',\\n    PRIMARY KEY (user_id),\\n    UNIQUE KEY (phone_number),\\n    UNIQUE KEY (email),\\n    UNIQUE KEY (account)\\n) ENGINE=InnoDB AUTO_INCREMENT=100 DEFAULT CHARSET=utf8mb4 COMMENT=\'用户信息表\';\\n    introduction TEXT,\\n    create_time DATETIME,\\n    last_login_time DATETIME\\n);\"}', '{\"msg\":\"创建表结构异常\",\"code\":500}', 0, NULL, '2025-05-07 11:16:01', 2);
INSERT INTO `sys_oper_log` VALUES (106, '创建表', 0, 'com.ruoyi.generator.controller.GenController.createTableSave()', 'POST', 1, 'admin', '研发部门', '/tool/gen/createTable', '127.0.0.1', '内网IP', '{\"sql\":\"CREATE TABLE ur_user (\\n    user_id INT AUTO_INCREMENT PRIMARY KEY,\\n    nickname VARCHAR(50),\\n    gender VARCHAR(10),\\n    age INT,\\n    phone_number VARCHAR(20) UNIQUE,\\n    email VARCHAR(100) UNIQUE,\\n    account VARCHAR(50) UNIQUE,\\n    password VARCHAR(100),\\n    avatar VARCHAR(255),\\n    introduction TEXT,\\n    create_time DATETIME,\\n    last_login_time DATETIME\\n);\"}', '{\"msg\":\"创建表结构异常\",\"code\":500}', 0, NULL, '2025-05-07 11:17:31', 1);
INSERT INTO `sys_oper_log` VALUES (107, '代码生成', 6, 'com.ruoyi.generator.controller.GenController.importTableSave()', 'POST', 1, 'admin', '研发部门', '/tool/gen/importTable', '127.0.0.1', '内网IP', '{\"tables\":\"ur_user,ur_review\"}', '{\"msg\":\"操作成功\",\"code\":200}', 0, NULL, '2025-05-07 11:19:07', 87);
INSERT INTO `sys_oper_log` VALUES (108, '代码生成', 6, 'com.ruoyi.generator.controller.GenController.importTableSave()', 'POST', 1, 'admin', '研发部门', '/tool/gen/importTable', '127.0.0.1', '内网IP', '{\"tables\":\"ur_visitor,ur_course_purchase_order,ur_psychological_appointment_order,ur_course,ur_course_detail,ur_course_read_record,ur_appointment,ur_counselor,ur_counselor_region,ur_region\"}', '{\"msg\":\"操作成功\",\"code\":200}', 0, NULL, '2025-05-07 11:19:17', 268);
INSERT INTO `sys_oper_log` VALUES (109, '代码生成', 8, 'com.ruoyi.generator.controller.GenController.batchGenCode()', 'GET', 1, 'admin', '研发部门', '/tool/gen/batchGenCode', '127.0.0.1', '内网IP', '{\"tables\":\"ur_appointment\"}', NULL, 0, NULL, '2025-05-07 11:19:43', 178);
INSERT INTO `sys_oper_log` VALUES (110, '代码生成', 8, 'com.ruoyi.generator.controller.GenController.batchGenCode()', 'GET', 1, 'admin', '研发部门', '/tool/gen/batchGenCode', '127.0.0.1', '内网IP', '{\"tables\":\"ur_appointment\"}', NULL, 0, NULL, '2025-05-07 11:20:42', 38);
INSERT INTO `sys_oper_log` VALUES (111, '代码生成', 8, 'com.ruoyi.generator.controller.GenController.batchGenCode()', 'GET', 1, 'admin', '研发部门', '/tool/gen/batchGenCode', '127.0.0.1', '内网IP', '{\"tables\":\"ur_appointment\"}', NULL, 0, NULL, '2025-05-07 15:00:15', 216);
INSERT INTO `sys_oper_log` VALUES (112, '菜单管理', 1, 'com.ruoyi.web.controller.system.SysMenuController.add()', 'POST', 1, 'admin', '研发部门', '/system/menu', '127.0.0.1', '内网IP', '{\"children\":[],\"createBy\":\"admin\",\"icon\":\"user\",\"isCache\":\"0\",\"isFrame\":\"1\",\"menuName\":\"咨询师管理\",\"menuType\":\"M\",\"orderNum\":5,\"params\":{},\"parentId\":0,\"path\":\"counselors\",\"status\":\"0\",\"visible\":\"0\"}', '{\"msg\":\"操作成功\",\"code\":200}', 0, NULL, '2025-05-07 15:06:38', 18);

-- ----------------------------
-- Table structure for sys_post
-- ----------------------------
DROP TABLE IF EXISTS `sys_post`;
CREATE TABLE `sys_post`  (
  `post_id` bigint NOT NULL AUTO_INCREMENT COMMENT '岗位ID',
  `post_code` varchar(64) CHARACTER SET utf8mb3 COLLATE utf8mb3_unicode_ci NOT NULL COMMENT '岗位编码',
  `post_name` varchar(50) CHARACTER SET utf8mb3 COLLATE utf8mb3_unicode_ci NOT NULL COMMENT '岗位名称',
  `post_sort` int NOT NULL COMMENT '显示顺序',
  `status` char(1) CHARACTER SET utf8mb3 COLLATE utf8mb3_unicode_ci NOT NULL COMMENT '状态（0正常 1停用）',
  `create_by` varchar(64) CHARACTER SET utf8mb3 COLLATE utf8mb3_unicode_ci NULL DEFAULT '' COMMENT '创建者',
  `create_time` datetime NULL DEFAULT NULL COMMENT '创建时间',
  `update_by` varchar(64) CHARACTER SET utf8mb3 COLLATE utf8mb3_unicode_ci NULL DEFAULT '' COMMENT '更新者',
  `update_time` datetime NULL DEFAULT NULL COMMENT '更新时间',
  `remark` varchar(500) CHARACTER SET utf8mb3 COLLATE utf8mb3_unicode_ci NULL DEFAULT NULL COMMENT '备注',
  PRIMARY KEY (`post_id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 4 CHARACTER SET = utf8mb3 COLLATE = utf8mb3_unicode_ci COMMENT = '岗位信息表' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of sys_post
-- ----------------------------
INSERT INTO `sys_post` VALUES (1, 'ceo', '董事长', 1, '0', 'admin', '2025-04-27 08:31:45', '', NULL, '');
INSERT INTO `sys_post` VALUES (2, 'se', '项目经理', 2, '0', 'admin', '2025-04-27 08:31:45', '', NULL, '');
INSERT INTO `sys_post` VALUES (3, 'hr', '人力资源', 3, '0', 'admin', '2025-04-27 08:31:45', '', NULL, '');
INSERT INTO `sys_post` VALUES (4, 'user', '普通员工', 4, '0', 'admin', '2025-04-27 08:31:45', '', NULL, '');

-- ----------------------------
-- Table structure for sys_role
-- ----------------------------
DROP TABLE IF EXISTS `sys_role`;
CREATE TABLE `sys_role`  (
  `role_id` bigint NOT NULL AUTO_INCREMENT COMMENT '角色ID',
  `role_name` varchar(30) CHARACTER SET utf8mb3 COLLATE utf8mb3_unicode_ci NOT NULL COMMENT '角色名称',
  `role_key` varchar(100) CHARACTER SET utf8mb3 COLLATE utf8mb3_unicode_ci NOT NULL COMMENT '角色权限字符串',
  `role_sort` int NOT NULL COMMENT '显示顺序',
  `data_scope` char(1) CHARACTER SET utf8mb3 COLLATE utf8mb3_unicode_ci NULL DEFAULT '1' COMMENT '数据范围（1：全部数据权限 2：自定数据权限 3：本部门数据权限 4：本部门及以下数据权限）',
  `menu_check_strictly` tinyint(1) NULL DEFAULT 1 COMMENT '菜单树选择项是否关联显示',
  `dept_check_strictly` tinyint(1) NULL DEFAULT 1 COMMENT '部门树选择项是否关联显示',
  `status` char(1) CHARACTER SET utf8mb3 COLLATE utf8mb3_unicode_ci NOT NULL COMMENT '角色状态（0正常 1停用）',
  `del_flag` char(1) CHARACTER SET utf8mb3 COLLATE utf8mb3_unicode_ci NULL DEFAULT '0' COMMENT '删除标志（0代表存在 2代表删除）',
  `create_by` varchar(64) CHARACTER SET utf8mb3 COLLATE utf8mb3_unicode_ci NULL DEFAULT '' COMMENT '创建者',
  `create_time` datetime NULL DEFAULT NULL COMMENT '创建时间',
  `update_by` varchar(64) CHARACTER SET utf8mb3 COLLATE utf8mb3_unicode_ci NULL DEFAULT '' COMMENT '更新者',
  `update_time` datetime NULL DEFAULT NULL COMMENT '更新时间',
  `remark` varchar(500) CHARACTER SET utf8mb3 COLLATE utf8mb3_unicode_ci NULL DEFAULT NULL COMMENT '备注',
  PRIMARY KEY (`role_id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 2 CHARACTER SET = utf8mb3 COLLATE = utf8mb3_unicode_ci COMMENT = '角色信息表' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of sys_role
-- ----------------------------
INSERT INTO `sys_role` VALUES (1, '超级管理员', 'admin', 1, '1', 1, 1, '0', '0', 'admin', '2025-04-27 08:31:45', '', NULL, '超级管理员');
INSERT INTO `sys_role` VALUES (2, '普通角色', 'common', 2, '2', 1, 1, '0', '0', 'admin', '2025-04-27 08:31:45', '', NULL, '普通角色');

-- ----------------------------
-- Table structure for sys_role_dept
-- ----------------------------
DROP TABLE IF EXISTS `sys_role_dept`;
CREATE TABLE `sys_role_dept`  (
  `role_id` bigint NOT NULL COMMENT '角色ID',
  `dept_id` bigint NOT NULL COMMENT '部门ID',
  PRIMARY KEY (`role_id`, `dept_id`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8mb3 COLLATE = utf8mb3_unicode_ci COMMENT = '角色和部门关联表' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of sys_role_dept
-- ----------------------------
INSERT INTO `sys_role_dept` VALUES (2, 100);
INSERT INTO `sys_role_dept` VALUES (2, 101);
INSERT INTO `sys_role_dept` VALUES (2, 105);

-- ----------------------------
-- Table structure for sys_role_menu
-- ----------------------------
DROP TABLE IF EXISTS `sys_role_menu`;
CREATE TABLE `sys_role_menu`  (
  `role_id` bigint NOT NULL COMMENT '角色ID',
  `menu_id` bigint NOT NULL COMMENT '菜单ID',
  PRIMARY KEY (`role_id`, `menu_id`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8mb3 COLLATE = utf8mb3_unicode_ci COMMENT = '角色和菜单关联表' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of sys_role_menu
-- ----------------------------
INSERT INTO `sys_role_menu` VALUES (2, 1);
INSERT INTO `sys_role_menu` VALUES (2, 2);
INSERT INTO `sys_role_menu` VALUES (2, 3);
INSERT INTO `sys_role_menu` VALUES (2, 4);
INSERT INTO `sys_role_menu` VALUES (2, 100);
INSERT INTO `sys_role_menu` VALUES (2, 101);
INSERT INTO `sys_role_menu` VALUES (2, 102);
INSERT INTO `sys_role_menu` VALUES (2, 103);
INSERT INTO `sys_role_menu` VALUES (2, 104);
INSERT INTO `sys_role_menu` VALUES (2, 105);
INSERT INTO `sys_role_menu` VALUES (2, 106);
INSERT INTO `sys_role_menu` VALUES (2, 107);
INSERT INTO `sys_role_menu` VALUES (2, 108);
INSERT INTO `sys_role_menu` VALUES (2, 109);
INSERT INTO `sys_role_menu` VALUES (2, 110);
INSERT INTO `sys_role_menu` VALUES (2, 111);
INSERT INTO `sys_role_menu` VALUES (2, 112);
INSERT INTO `sys_role_menu` VALUES (2, 113);
INSERT INTO `sys_role_menu` VALUES (2, 114);
INSERT INTO `sys_role_menu` VALUES (2, 115);
INSERT INTO `sys_role_menu` VALUES (2, 116);
INSERT INTO `sys_role_menu` VALUES (2, 117);
INSERT INTO `sys_role_menu` VALUES (2, 500);
INSERT INTO `sys_role_menu` VALUES (2, 501);
INSERT INTO `sys_role_menu` VALUES (2, 1000);
INSERT INTO `sys_role_menu` VALUES (2, 1001);
INSERT INTO `sys_role_menu` VALUES (2, 1002);
INSERT INTO `sys_role_menu` VALUES (2, 1003);
INSERT INTO `sys_role_menu` VALUES (2, 1004);
INSERT INTO `sys_role_menu` VALUES (2, 1005);
INSERT INTO `sys_role_menu` VALUES (2, 1006);
INSERT INTO `sys_role_menu` VALUES (2, 1007);
INSERT INTO `sys_role_menu` VALUES (2, 1008);
INSERT INTO `sys_role_menu` VALUES (2, 1009);
INSERT INTO `sys_role_menu` VALUES (2, 1010);
INSERT INTO `sys_role_menu` VALUES (2, 1011);
INSERT INTO `sys_role_menu` VALUES (2, 1012);
INSERT INTO `sys_role_menu` VALUES (2, 1013);
INSERT INTO `sys_role_menu` VALUES (2, 1014);
INSERT INTO `sys_role_menu` VALUES (2, 1015);
INSERT INTO `sys_role_menu` VALUES (2, 1016);
INSERT INTO `sys_role_menu` VALUES (2, 1017);
INSERT INTO `sys_role_menu` VALUES (2, 1018);
INSERT INTO `sys_role_menu` VALUES (2, 1019);
INSERT INTO `sys_role_menu` VALUES (2, 1020);
INSERT INTO `sys_role_menu` VALUES (2, 1021);
INSERT INTO `sys_role_menu` VALUES (2, 1022);
INSERT INTO `sys_role_menu` VALUES (2, 1023);
INSERT INTO `sys_role_menu` VALUES (2, 1024);
INSERT INTO `sys_role_menu` VALUES (2, 1025);
INSERT INTO `sys_role_menu` VALUES (2, 1026);
INSERT INTO `sys_role_menu` VALUES (2, 1027);
INSERT INTO `sys_role_menu` VALUES (2, 1028);
INSERT INTO `sys_role_menu` VALUES (2, 1029);
INSERT INTO `sys_role_menu` VALUES (2, 1030);
INSERT INTO `sys_role_menu` VALUES (2, 1031);
INSERT INTO `sys_role_menu` VALUES (2, 1032);
INSERT INTO `sys_role_menu` VALUES (2, 1033);
INSERT INTO `sys_role_menu` VALUES (2, 1034);
INSERT INTO `sys_role_menu` VALUES (2, 1035);
INSERT INTO `sys_role_menu` VALUES (2, 1036);
INSERT INTO `sys_role_menu` VALUES (2, 1037);
INSERT INTO `sys_role_menu` VALUES (2, 1038);
INSERT INTO `sys_role_menu` VALUES (2, 1039);
INSERT INTO `sys_role_menu` VALUES (2, 1040);
INSERT INTO `sys_role_menu` VALUES (2, 1041);
INSERT INTO `sys_role_menu` VALUES (2, 1042);
INSERT INTO `sys_role_menu` VALUES (2, 1043);
INSERT INTO `sys_role_menu` VALUES (2, 1044);
INSERT INTO `sys_role_menu` VALUES (2, 1045);
INSERT INTO `sys_role_menu` VALUES (2, 1046);
INSERT INTO `sys_role_menu` VALUES (2, 1047);
INSERT INTO `sys_role_menu` VALUES (2, 1048);
INSERT INTO `sys_role_menu` VALUES (2, 1049);
INSERT INTO `sys_role_menu` VALUES (2, 1050);
INSERT INTO `sys_role_menu` VALUES (2, 1051);
INSERT INTO `sys_role_menu` VALUES (2, 1052);
INSERT INTO `sys_role_menu` VALUES (2, 1053);
INSERT INTO `sys_role_menu` VALUES (2, 1054);
INSERT INTO `sys_role_menu` VALUES (2, 1055);
INSERT INTO `sys_role_menu` VALUES (2, 1056);
INSERT INTO `sys_role_menu` VALUES (2, 1057);
INSERT INTO `sys_role_menu` VALUES (2, 1058);
INSERT INTO `sys_role_menu` VALUES (2, 1059);
INSERT INTO `sys_role_menu` VALUES (2, 1060);

-- ----------------------------
-- Table structure for sys_user
-- ----------------------------
DROP TABLE IF EXISTS `sys_user`;
CREATE TABLE `sys_user`  (
  `user_id` bigint NOT NULL AUTO_INCREMENT COMMENT '用户ID',
  `dept_id` bigint NULL DEFAULT NULL COMMENT '部门ID',
  `user_name` varchar(30) CHARACTER SET utf8mb3 COLLATE utf8mb3_unicode_ci NOT NULL COMMENT '用户账号',
  `nick_name` varchar(30) CHARACTER SET utf8mb3 COLLATE utf8mb3_unicode_ci NOT NULL COMMENT '用户昵称',
  `user_type` varchar(2) CHARACTER SET utf8mb3 COLLATE utf8mb3_unicode_ci NULL DEFAULT '00' COMMENT '用户类型（00系统用户）',
  `email` varchar(50) CHARACTER SET utf8mb3 COLLATE utf8mb3_unicode_ci NULL DEFAULT '' COMMENT '用户邮箱',
  `phonenumber` varchar(11) CHARACTER SET utf8mb3 COLLATE utf8mb3_unicode_ci NULL DEFAULT '' COMMENT '手机号码',
  `sex` char(1) CHARACTER SET utf8mb3 COLLATE utf8mb3_unicode_ci NULL DEFAULT '0' COMMENT '用户性别（0男 1女 2未知）',
  `avatar` varchar(100) CHARACTER SET utf8mb3 COLLATE utf8mb3_unicode_ci NULL DEFAULT '' COMMENT '头像地址',
  `password` varchar(100) CHARACTER SET utf8mb3 COLLATE utf8mb3_unicode_ci NULL DEFAULT '' COMMENT '密码',
  `status` char(1) CHARACTER SET utf8mb3 COLLATE utf8mb3_unicode_ci NULL DEFAULT '0' COMMENT '账号状态（0正常 1停用）',
  `del_flag` char(1) CHARACTER SET utf8mb3 COLLATE utf8mb3_unicode_ci NULL DEFAULT '0' COMMENT '删除标志（0代表存在 2代表删除）',
  `login_ip` varchar(128) CHARACTER SET utf8mb3 COLLATE utf8mb3_unicode_ci NULL DEFAULT '' COMMENT '最后登录IP',
  `login_date` datetime NULL DEFAULT NULL COMMENT '最后登录时间',
  `create_by` varchar(64) CHARACTER SET utf8mb3 COLLATE utf8mb3_unicode_ci NULL DEFAULT '' COMMENT '创建者',
  `create_time` datetime NULL DEFAULT NULL COMMENT '创建时间',
  `update_by` varchar(64) CHARACTER SET utf8mb3 COLLATE utf8mb3_unicode_ci NULL DEFAULT '' COMMENT '更新者',
  `update_time` datetime NULL DEFAULT NULL COMMENT '更新时间',
  `remark` varchar(500) CHARACTER SET utf8mb3 COLLATE utf8mb3_unicode_ci NULL DEFAULT NULL COMMENT '备注',
  PRIMARY KEY (`user_id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 2 CHARACTER SET = utf8mb3 COLLATE = utf8mb3_unicode_ci COMMENT = '用户信息表' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of sys_user
-- ----------------------------
INSERT INTO `sys_user` VALUES (1, 103, 'admin', '若依', '00', 'ry@163.com', '15888888888', '1', '', '$2a$10$7JB720yubVSZvUI0rEqK/.VqGOZTH.ulu33dHOiBE8ByOhJIrdAu2', '0', '0', '127.0.0.1', '2025-05-07 16:36:53', 'admin', '2025-04-27 08:31:45', '', '2025-05-07 16:36:53', '管理员');
INSERT INTO `sys_user` VALUES (2, 105, 'ry', '若依', '00', 'ry@qq.com', '15666666666', '1', '', '$2a$10$7JB720yubVSZvUI0rEqK/.VqGOZTH.ulu33dHOiBE8ByOhJIrdAu2', '0', '0', '127.0.0.1', '2025-04-27 08:31:45', 'admin', '2025-04-27 08:31:45', '', NULL, '测试员');

-- ----------------------------
-- Table structure for sys_user_post
-- ----------------------------
DROP TABLE IF EXISTS `sys_user_post`;
CREATE TABLE `sys_user_post`  (
  `user_id` bigint NOT NULL COMMENT '用户ID',
  `post_id` bigint NOT NULL COMMENT '岗位ID',
  PRIMARY KEY (`user_id`, `post_id`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8mb3 COLLATE = utf8mb3_unicode_ci COMMENT = '用户与岗位关联表' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of sys_user_post
-- ----------------------------
INSERT INTO `sys_user_post` VALUES (1, 1);
INSERT INTO `sys_user_post` VALUES (2, 2);

-- ----------------------------
-- Table structure for sys_user_role
-- ----------------------------
DROP TABLE IF EXISTS `sys_user_role`;
CREATE TABLE `sys_user_role`  (
  `user_id` bigint NOT NULL COMMENT '用户ID',
  `role_id` bigint NOT NULL COMMENT '角色ID',
  PRIMARY KEY (`user_id`, `role_id`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8mb3 COLLATE = utf8mb3_unicode_ci COMMENT = '用户和角色关联表' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of sys_user_role
-- ----------------------------
INSERT INTO `sys_user_role` VALUES (1, 1);
INSERT INTO `sys_user_role` VALUES (2, 2);

-- ----------------------------
-- Table structure for ur_announcement
-- ----------------------------
DROP TABLE IF EXISTS `ur_announcement`;
CREATE TABLE `ur_announcement`  (
  `id` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '公告ID',
  `content` text CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '公告内容',
  `publish_time` datetime NOT NULL COMMENT '发布时间',
  `status` tinyint NULL DEFAULT 1 COMMENT '状态(0-禁用,1-启用)',
  `create_time` datetime NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `update_time` datetime NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci COMMENT = '系统公告表' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of ur_announcement
-- ----------------------------
INSERT INTO `ur_announcement` VALUES ('a001', '新版小程序上线，体验全新功能', '2023-05-20 10:00:00', 1, '2025-05-08 22:20:17', '2025-05-08 22:20:17');
INSERT INTO `ur_announcement` VALUES ('a002', '系统维护通知：5月25日0点至6点', '2023-05-22 15:30:00', 1, '2025-05-08 22:20:17', '2025-05-08 22:20:17');
INSERT INTO `ur_announcement` VALUES ('a003', '端午节假期客服安排调整', '2023-06-10 09:00:00', 1, '2025-05-08 22:20:17', '2025-05-08 22:20:17');
INSERT INTO `ur_announcement` VALUES ('a004', '用户协议更新公告', '2023-06-15 14:00:00', 0, '2025-05-08 22:20:17', '2025-05-08 22:20:17');
INSERT INTO `ur_announcement` VALUES ('a005', '暑期优惠活动即将开始', '2023-06-20 11:20:00', 1, '2025-05-08 22:20:17', '2025-05-08 22:20:17');

-- ----------------------------
-- Table structure for ur_appointments
-- ----------------------------
DROP TABLE IF EXISTS `ur_appointments`;
CREATE TABLE `ur_appointments`  (
  `id` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '预约ID',
  `counselor_id` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '咨询师ID',
  `service_id` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '服务ID',
  `user_id` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '用户ID',
  `date` date NOT NULL COMMENT '预约日期',
  `time_slot` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '时间段',
  `note` text CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL COMMENT '咨询备注',
  `status` tinyint NULL DEFAULT 0 COMMENT '预约状态(0-待确认,1-已确认,2-已取消)',
  `create_time` datetime NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `service_id`(`service_id` ASC) USING BTREE,
  INDEX `counselor_id`(`counselor_id` ASC) USING BTREE,
  CONSTRAINT `ur_appointments_ibfk_1` FOREIGN KEY (`service_id`) REFERENCES `ur_service` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `ur_appointments_ibfk_2` FOREIGN KEY (`counselor_id`) REFERENCES `ur_counselor` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci COMMENT = '心理咨询预约表' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of ur_appointments
-- ----------------------------
INSERT INTO `ur_appointments` VALUES ('y001', 'c001', 's001', 'u1001', '2023-06-01', '09:00-10:00', '第一次咨询，希望能得到专业帮助1', 1, '2023-05-28 10:00:00');
INSERT INTO `ur_appointments` VALUES ('y002', 'c002', 's002', 'u1002', '2023-06-02', '14:00-15:30', '婚姻关系咨询', 1, '2023-05-29 11:30:00');
INSERT INTO `ur_appointments` VALUES ('y003', 'c003', 's003', 'u1003', '2023-06-03', '10:30-11:00', '紧急心理疏导', 0, '2023-05-30 09:15:00');
INSERT INTO `ur_appointments` VALUES ('y004', 'c001', 's004', 'u1004', '2023-06-04', '15:00-17:00', '青少年心理健康团体辅导', 1, '2023-05-30 14:20:00');
INSERT INTO `ur_appointments` VALUES ('y005', 'c002', 's005', 'u1005', '2023-06-05', '13:00-14:00', '职业心理测评', 2, '2023-05-31 16:45:00');
INSERT INTO `ur_appointments` VALUES ('y1746792169293', 'c001', 's002', 'u1001', '2023-06-02', '10:00-12:00', '第一次咨询，希望能得到专业帮助2', 2, '2025-05-09 20:02:49');
INSERT INTO `ur_appointments` VALUES ('y1746889913376', 'c001', 's002', 'u1001', '2023-12-15', '14:00-15:00', '修改后的咨询备注', 0, '2025-05-10 23:11:53');

-- ----------------------------
-- Table structure for ur_counselor
-- ----------------------------
DROP TABLE IF EXISTS `ur_counselor`;
CREATE TABLE `ur_counselor`  (
  `id` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '咨询师ID',
  `name` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '姓名',
  `avatar` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL COMMENT '头像URL',
  `title` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL COMMENT '职称',
  `is_verified` tinyint NULL DEFAULT NULL COMMENT '是否认证',
  `tags` json NULL COMMENT '擅长标签',
  `price` decimal(10, 2) NOT NULL COMMENT '咨询价格(元/小时)',
  `rating` decimal(3, 1) NULL DEFAULT 0.0 COMMENT '评分(0-5)',
  `session_count` int NULL DEFAULT 0 COMMENT '咨询次数',
  `introduction` text CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL COMMENT '个人简介',
  `education` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL COMMENT '教育背景',
  `experience` text CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL COMMENT '工作经历',
  `certificates` json NULL COMMENT '资格证书',
  `services` json NULL COMMENT '服务类型',
  `availability` json NULL COMMENT '可预约时间段',
  `create_time` datetime NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `update_time` datetime NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  `region_id` int NULL DEFAULT NULL COMMENT '地区',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci COMMENT = '心理咨询师表' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of ur_counselor
-- ----------------------------
INSERT INTO `ur_counselor` VALUES ('c001', '张医生', 'https://example.com/counselor1.jpg', '心理咨询师', 1, '[\"抑郁症\", \"焦虑障碍\", \"青少年心理\"]', 300.00, 4.8, 256, '15年临床经验，专注于抑郁症和焦虑障碍治疗...', '北京大学心理学博士', '曾任某三甲医院心理科主任医师，有丰富的临床经验...', '[\"国家二级心理咨询师\", \"认知行为治疗师资格证\"]', '[\"个人咨询\", \"家庭咨询\", \"青少年咨询\"]', '[\"周一至周五: 9:00-18:00\", \"周六: 10:00-16:00\"]', '2025-05-08 13:58:39', '2025-05-08 18:54:57', 1);
INSERT INTO `ur_counselor` VALUES ('c002', '李教授', 'https://example.com/counselor2.jpg', '临床心理专家', 1, '[\"婚姻咨询\", \"家庭治疗\", \"亲子关系\"]', 450.00, 4.9, 312, '20年心理咨询经验，擅长解决婚姻家庭问题...', '清华大学心理学硕士', '现任某高校心理系教授，婚姻家庭咨询专家...', '[\"国家一级心理咨询师\", \"婚姻家庭治疗师\"]', '[\"婚姻咨询\", \"家庭治疗\", \"团体辅导\"]', '[\"周二、周四: 10:00-17:00\", \"周六: 9:00-15:00\"]', '2025-05-08 13:58:39', '2025-05-09 00:13:13', 1);
INSERT INTO `ur_counselor` VALUES ('c003', '王老师', 'https://example.com/counselor3.jpg', '青少年心理专家', 0, '[\"青少年心理\", \"学习障碍\", \"网络成瘾\"]', 380.00, 4.7, 189, '专注于青少年心理健康教育10年...', '华东师范大学心理学博士', '青少年心理辅导中心主任...', '[\"国家二级心理咨询师\", \"青少年心理指导师\"]', '[\"青少年咨询\", \"家长指导\", \"学校心理辅导\"]', '[\"周一至周五: 13:00-20:00\"]', '2025-05-08 13:58:39', '2025-05-08 18:55:04', 1);

-- ----------------------------
-- Table structure for ur_counselor_region
-- ----------------------------
DROP TABLE IF EXISTS `ur_counselor_region`;
CREATE TABLE `ur_counselor_region`  (
  `counselor_id` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '咨询师id',
  `region_id` int NOT NULL COMMENT '地区id',
  INDEX `FK_1`(`counselor_id` ASC) USING BTREE,
  INDEX `FK_2`(`region_id` ASC) USING BTREE,
  CONSTRAINT `FK_1` FOREIGN KEY (`counselor_id`) REFERENCES `ur_counselor` (`id`) ON DELETE CASCADE ON UPDATE RESTRICT,
  CONSTRAINT `FK_2` FOREIGN KEY (`region_id`) REFERENCES `ur_region` (`id`) ON DELETE CASCADE ON UPDATE RESTRICT
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of ur_counselor_region
-- ----------------------------
INSERT INTO `ur_counselor_region` VALUES ('c001', 1);

-- ----------------------------
-- Table structure for ur_counselor_reviews
-- ----------------------------
DROP TABLE IF EXISTS `ur_counselor_reviews`;
CREATE TABLE `ur_counselor_reviews`  (
  `review_id` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '评价ID',
  `counselor_id` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '咨询师ID',
  `order_id` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '关联订单ID',
  `content` text CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL COMMENT '评价内容',
  `rating` tinyint NOT NULL COMMENT '评分(1-5)',
  `create_time` datetime NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  PRIMARY KEY (`review_id`) USING BTREE,
  INDEX `counselor_id`(`counselor_id` ASC) USING BTREE,
  CONSTRAINT `ur_counselor_reviews_ibfk_1` FOREIGN KEY (`counselor_id`) REFERENCES `ur_counselor` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci COMMENT = '咨询师评价表' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of ur_counselor_reviews
-- ----------------------------
INSERT INTO `ur_counselor_reviews` VALUES ('r001', 'c001', 'o001', '咨询师非常专业，解决了我的心理问题', 5, '2023-06-01 10:00:00');
INSERT INTO `ur_counselor_reviews` VALUES ('r002', 'c002', 'o002', '很有耐心的咨询过程，收获很大', 4, '2023-06-02 14:30:00');
INSERT INTO `ur_counselor_reviews` VALUES ('r003', 'c003', 'o003', '对孩子心理问题分析很准确', 5, '2023-06-03 09:15:00');
INSERT INTO `ur_counselor_reviews` VALUES ('r004', 'c001', 'o004', '第二次咨询，效果依然很好', 4, '2023-06-04 11:20:00');
INSERT INTO `ur_counselor_reviews` VALUES ('r005', 'c001', 'o005', '婚姻咨询很有帮助，夫妻关系改善明显', 5, '2023-06-05 16:45:00');
INSERT INTO `ur_counselor_reviews` VALUES ('r1746754484310', 'c001', 'o001', '非常专业的咨询师，帮助我走出了困境', 5, '2025-05-09 09:34:44');

-- ----------------------------
-- Table structure for ur_course_info
-- ----------------------------
DROP TABLE IF EXISTS `ur_course_info`;
CREATE TABLE `ur_course_info`  (
  `id` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '课程ID',
  `title` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '课程标题',
  `cover_image` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL COMMENT '封面图URL',
  `teacher` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL COMMENT '讲师姓名',
  `teacher_title` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL COMMENT '讲师职称',
  `teacher_avatar` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL COMMENT '讲师头像URL',
  `price` decimal(10, 2) NULL DEFAULT NULL COMMENT '课程价格',
  `original_price` decimal(10, 2) NULL DEFAULT NULL COMMENT '原价',
  `lesson_count` int NULL DEFAULT NULL COMMENT '课时数',
  `student_count` int NULL DEFAULT 0 COMMENT '学习人数',
  `rating` decimal(3, 1) NULL DEFAULT 0.0 COMMENT '评分',
  `tags` json NULL COMMENT '课程标签',
  `description` text CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL COMMENT '课程描述',
  `create_time` datetime NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `update_time` datetime NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci COMMENT = '课程信息表' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of ur_course_info
-- ----------------------------
INSERT INTO `ur_course_info` VALUES ('course001', '情绪管理入门课程', 'https://example.com/course1.jpg', '王教授', '心理学教授', 'https://example.com/teacher1.jpg', 99.00, 199.00, 12, 2560, 4.7, '[\"情绪管理\", \"心理健康\", \"抑郁症\"]', '适合初学者的情绪管理课程...', '2025-05-08 19:30:36', '2025-05-09 15:12:14');
INSERT INTO `ur_course_info` VALUES ('course002', '职场压力管理', 'https://example.com/course2.jpg', '李老师', '职业心理咨询师', 'https://example.com/teacher2.jpg', 129.00, 259.00, 8, 1850, 4.5, '[\"职场心理\", \"压力管理\", \"青少年心理\"]', '帮助职场人士有效管理压力...', '2025-05-08 19:30:45', '2025-05-09 15:04:32');

-- ----------------------------
-- Table structure for ur_course_outline
-- ----------------------------
DROP TABLE IF EXISTS `ur_course_outline`;
CREATE TABLE `ur_course_outline`  (
  `id` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '大纲ID',
  `course_id` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '关联课程ID',
  `chapter_title` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL COMMENT '章节标题',
  `lesson_id` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL COMMENT '课时ID',
  `lesson_title` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL COMMENT '课时标题',
  `duration` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL COMMENT '课时时长',
  `video_url` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL COMMENT '视频链接',
  `is_free` tinyint(1) NULL DEFAULT 0 COMMENT '是否免费',
  `sort_order` int NULL DEFAULT NULL COMMENT '排序序号',
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `course_id`(`course_id` ASC) USING BTREE,
  CONSTRAINT `ur_course_outline_ibfk_1` FOREIGN KEY (`course_id`) REFERENCES `ur_course_info` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci COMMENT = '课程大纲表' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of ur_course_outline
-- ----------------------------
INSERT INTO `ur_course_outline` VALUES ('out001', 'course001', '第一章：认识情绪', 'l001', '什么是情绪', '20分钟', 'https://example.com/video1.mp4', 1, 1);
INSERT INTO `ur_course_outline` VALUES ('out002', 'course001', '第一章：认识情绪', 'l002', '情绪的分类', '25分钟', 'https://example.com/video2.mp4', 0, 2);
INSERT INTO `ur_course_outline` VALUES ('out003', 'course001', '第二章：情绪调节', 'l003', '基础调节技巧', '30分钟', 'https://example.com/video3.mp4', 0, 3);
INSERT INTO `ur_course_outline` VALUES ('out004', 'course002', '职场压力识别', 'l004', '认识职场压力', '18分钟', 'https://example.com/video4.mp4', 1, 1);
INSERT INTO `ur_course_outline` VALUES ('out005', 'course002', '压力管理技巧', 'l005', '实用减压方法', '22分钟', 'https://example.com/video5.mp4', 0, 2);

-- ----------------------------
-- Table structure for ur_disease_tags
-- ----------------------------
DROP TABLE IF EXISTS `ur_disease_tags`;
CREATE TABLE `ur_disease_tags`  (
  `id` int NOT NULL COMMENT '病症ID',
  `name` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '病症名称',
  `icon` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL COMMENT '病症图标URL',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci COMMENT = '病症标签表' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of ur_disease_tags
-- ----------------------------
INSERT INTO `ur_disease_tags` VALUES (1, '抑郁症', 'https://example.com/icons/depression.png');
INSERT INTO `ur_disease_tags` VALUES (2, '焦虑障碍', 'https://example.com/icons/anxiety.png');
INSERT INTO `ur_disease_tags` VALUES (3, '青少年心理', 'https://example.com/icons/teen-mental-health.png');
INSERT INTO `ur_disease_tags` VALUES (4, '婚姻咨询', 'https://example.com/icons/marriage-counseling.png');
INSERT INTO `ur_disease_tags` VALUES (5, '家庭治疗', 'https://example.com/icons/family-therapy.png');
INSERT INTO `ur_disease_tags` VALUES (6, '亲子关系', 'https://example.com/icons/parenting.png');
INSERT INTO `ur_disease_tags` VALUES (7, '学习障碍', 'https://example.com/icons/learning-disability.png');
INSERT INTO `ur_disease_tags` VALUES (8, '网络成瘾', 'https://example.com/icons/internet-addiction.png');

-- ----------------------------
-- Table structure for ur_orders
-- ----------------------------
DROP TABLE IF EXISTS `ur_orders`;
CREATE TABLE `ur_orders`  (
  `id` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '订单ID',
  `order_no` varchar(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '订单编号',
  `appointment_id` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL COMMENT '关联预约ID',
  `title` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL COMMENT '订单名称',
  `type` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL COMMENT '订单类型',
  `price` decimal(10, 2) NULL DEFAULT NULL COMMENT '订单金额',
  `discount` decimal(10, 2) NULL DEFAULT 0.00 COMMENT '折扣金额',
  `actual_paid` decimal(10, 2) NULL DEFAULT NULL COMMENT '实付金额',
  `payment_method` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL COMMENT '支付方式',
  `payment_time` datetime NULL DEFAULT NULL COMMENT '支付时间',
  `status` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL COMMENT '订单状态',
  `create_time` datetime NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `appointment_id`(`appointment_id` ASC) USING BTREE,
  CONSTRAINT `ur_orders_ibfk_1` FOREIGN KEY (`appointment_id`) REFERENCES `ur_appointments` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci COMMENT = '订单表' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of ur_orders
-- ----------------------------
INSERT INTO `ur_orders` VALUES ('o001', '2023060112345', 'y001', '心理咨询服务', 'counseling', 300.00, 0.00, 300.00, 'wechat', '2023-05-28 14:35:10', '1', '2023-05-28 14:30:25');
INSERT INTO `ur_orders` VALUES ('o002', '2023060212345', 'y002', '心理咨询服务', 'counseling', 300.00, 0.00, 0.00, NULL, NULL, '2', '2023-05-29 09:15:20');
INSERT INTO `ur_orders` VALUES ('o003', '2023060312345', 'y003', '心理咨询服务', 'counseling', 300.00, 50.00, 250.00, 'alipay', '2023-05-30 16:20:30', '1', '2023-05-30 16:10:15');
INSERT INTO `ur_orders` VALUES ('o004', '2023060412345', 'y004', '心理咨询服务', 'counseling', 300.00, 0.00, 0.00, NULL, NULL, '0', '2023-05-31 10:45:00');
INSERT INTO `ur_orders` VALUES ('o005', '2023060512345', 'y005', '心理咨询服务', 'counseling', 300.00, 30.00, 270.00, 'wechat', '2023-06-01 08:10:45', '2', '2023-06-01 08:00:00');

-- ----------------------------
-- Table structure for ur_region
-- ----------------------------
DROP TABLE IF EXISTS `ur_region`;
CREATE TABLE `ur_region`  (
  `id` int NOT NULL COMMENT '地区id',
  `name` varchar(10) CHARACTER SET utf8mb3 COLLATE utf8mb3_unicode_ci NULL DEFAULT NULL COMMENT '地区的名称',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8mb3 COLLATE = utf8mb3_unicode_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of ur_region
-- ----------------------------
INSERT INTO `ur_region` VALUES (1, '湖北');
INSERT INTO `ur_region` VALUES (2, '湖南');

-- ----------------------------
-- Table structure for ur_service
-- ----------------------------
DROP TABLE IF EXISTS `ur_service`;
CREATE TABLE `ur_service`  (
  `id` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '服务ID',
  `name` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '服务名称',
  `description` text CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL COMMENT '服务描述',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci COMMENT = '咨询服务表' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of ur_service
-- ----------------------------
INSERT INTO `ur_service` VALUES ('s001', '在线咨询', '通过线上聊天来咨询心理健康问题');
INSERT INTO `ur_service` VALUES ('s002', '面对面咨询', '线下面对面心理咨询服务');
INSERT INTO `ur_service` VALUES ('s003', '电话咨询', '通过电话进行心理咨询');
INSERT INTO `ur_service` VALUES ('s004', '团体辅导', '针对特定群体的团体心理辅导');
INSERT INTO `ur_service` VALUES ('s005', '心理测评', '专业的心理健康评估测试');

-- ----------------------------
-- Table structure for ur_user_favorite
-- ----------------------------
DROP TABLE IF EXISTS `ur_user_favorite`;
CREATE TABLE `ur_user_favorite`  (
  `id` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '收藏ID',
  `user_id` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '用户ID',
  `item_id` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '收藏项ID',
  `item_type` enum('course','counselor') CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '收藏类型(课程/咨询师)',
  `create_time` datetime NULL DEFAULT CURRENT_TIMESTAMP COMMENT '收藏时间',
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `user_id`(`user_id` ASC) USING BTREE,
  CONSTRAINT `ur_user_favorite_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `ur_user_info` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci COMMENT = '用户收藏表' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of ur_user_favorite
-- ----------------------------
INSERT INTO `ur_user_favorite` VALUES ('f1746886489202', 'u1001', 'c001', 'counselor', '2025-05-10 22:14:49');
INSERT INTO `ur_user_favorite` VALUES ('f1746889052408', 'u1001', 'course001', 'course', '2025-05-10 22:57:32');

-- ----------------------------
-- Table structure for ur_user_info
-- ----------------------------
DROP TABLE IF EXISTS `ur_user_info`;
CREATE TABLE `ur_user_info`  (
  `id` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '用户ID',
  `nickname` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '用户昵称',
  `name` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL COMMENT '用户姓名',
  `avatar` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL COMMENT '用户头像URL',
  `email` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL COMMENT '用户邮箱',
  `phone` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL COMMENT '手机号',
  `gender` enum('male','female','other') CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL COMMENT '性别',
  `age` tinyint UNSIGNED NULL DEFAULT NULL COMMENT '年龄',
  `bio` text CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL COMMENT '个人简介',
  `create_time` datetime NOT NULL COMMENT '创建时间',
  `update_time` datetime NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci COMMENT = '用户信息表' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of ur_user_info
-- ----------------------------
INSERT INTO `ur_user_info` VALUES ('u1001', '新昵称', '张小明', 'https://example.com/new-avatar.jpg', '1234@qq.com', '13812345678', 'male', 30, '更新后的个人简介', '2023-05-20 08:30:45', '2025-05-13 19:48:12');
INSERT INTO `ur_user_info` VALUES ('u1002', '李晓晓晓', '李小红', 'https://example.com/avatar2.jpg', '12d@qq.com', '13987654321', 'female', 28, '心理咨询爱好者', '2023-05-21 09:15:20', '2025-05-13 19:48:20');
INSERT INTO `ur_user_info` VALUES ('u1003', '大力哥', '王大力', 'https://example.com/avatar3.jpg', '1sdmf@qq.com', '13711223344', 'male', 32, '企业高管，压力管理需求', '2023-05-22 10:30:15', '2025-05-13 19:48:24');
INSERT INTO `ur_user_info` VALUES ('u1004', '小美姐', '赵小美', 'https://example.com/avatar4.jpg', 'ssajh@qq.com', '13655667788', 'female', 24, '大学生，情感咨询需求', '2023-05-23 14:20:30', '2025-05-13 19:48:29');
INSERT INTO `ur_user_info` VALUES ('u1005', '建设国家建设大地', '刘建国', 'https://example.com/avatar5.jpg', 'sjae@qq.com', '13599887766', 'male', 45, '中年危机咨询', '2023-05-24 16:45:00', '2025-05-13 19:48:34');

SET FOREIGN_KEY_CHECKS = 1;
