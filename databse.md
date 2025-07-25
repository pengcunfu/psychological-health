# 心理健康平台数据库文档

## 数据库概述

本文档描述了心理健康平台的数据库结构，包括表结构、字段说明、约束条件以及表之间的关系。该数据库设计支持用户管理、咨询师管理、预约系统、课程管理、订单系统等功能。

## 基础模型

所有模型都继承自 `BaseModel`，包含以下公共字段：

| 字段名 | 类型 | 说明 | 约束 |
| --- | --- | --- | --- |
| id | Integer | 主键ID | 主键、自增 |
| create_time | DateTime | 创建时间 | 默认为当前UTC时间 |
| update_time | DateTime | 更新时间 | 默认为当前UTC时间，自动更新 |

## 用户与权限管理

### users 用户表

存储用户基本信息。

| 字段名 | 类型 | 说明 | 约束 |
| --- | --- | --- | --- |
| id | String(50) | 用户ID | 主键 |
| username | String(100) | 用户名 | 非空 |
| avatar | String(255) | 头像URL | 可空 |
| phone | String(20) | 手机号 | 可空 |
| email | String(100) | 邮箱 | 可空 |

### user_passwords 用户密码表

存储用户密码信息，与用户表分离以提高安全性。

| 字段名 | 类型 | 说明 | 约束 |
| --- | --- | --- | --- |
| id | String(50) | 密码记录ID | 主键 |
| user_id | String(50) | 用户ID | 外键(users.id)，非空，唯一 |
| password_hash | String(255) | 密码哈希值 | 非空 |

### roles 角色表

定义系统角色及其权限。

| 字段名 | 类型 | 说明 | 约束 |
| --- | --- | --- | --- |
| id | String(50) | 角色ID | 主键 |
| name | String(100) | 角色名称 | 非空 |
| code | String(50) | 角色编码 | 非空，唯一 |
| description | Text | 角色描述 | 可空 |
| sort_order | Integer | 排序顺序 | 默认0 |
| data_scope | Integer | 数据权限范围 | 默认1 |
| menu_ids_json | Text | 菜单权限ID列表 | JSON格式存储 |
| status | Integer | 状态 | 默认1 (0-禁用，1-启用) |
| is_default | Boolean | 是否默认角色 | 默认False |
| remark | Text | 备注 | 可空 |

数据权限范围说明：
- 1: 全部数据
- 2: 自定义数据
- 3: 本部门数据
- 4: 本部门及以下数据
- 5: 仅本人数据

### user_roles 用户角色关联表

用户与角色的多对多关系表。

| 字段名 | 类型 | 说明 | 约束 |
| --- | --- | --- | --- |
| id | String(50) | 关联ID | 主键 |
| user_id | String(50) | 用户ID | 外键(users.id)，非空 |
| role_id | String(50) | 角色ID | 外键(roles.id)，非空 |

### menus 菜单表

系统菜单及权限定义。

| 字段名 | 类型 | 说明 | 约束 |
| --- | --- | --- | --- |
| id | String(50) | 菜单ID | 主键 |
| name | String(100) | 菜单名称 | 非空 |
| path | String(255) | 菜单路径 | 可空 |
| icon | String(100) | 菜单图标 | 可空 |
| parent_id | String(50) | 父菜单ID | 默认空字符串 |
| level | Integer | 菜单层级 | 默认1 |
| sort_order | Integer | 排序顺序 | 默认0 |
| menu_type | Integer | 菜单类型 | 默认2 (1-目录，2-菜单，3-按钮) |
| permission | String(100) | 权限标识 | 可空 |
| component | String(255) | 组件路径 | 可空 |
| is_external | Boolean | 是否外链 | 默认False |
| is_visible | Boolean | 是否显示 | 默认True |
| is_cache | Boolean | 是否缓存 | 默认False |
| status | Integer | 状态 | 默认1 (0-禁用，1-启用) |
| remark | String(500) | 备注 | 可空 |

## 咨询服务相关表

### counselors 咨询师表

存储咨询师信息。

| 字段名 | 类型 | 说明 | 约束 |
| --- | --- | --- | --- |
| id | String(50) | 咨询师ID | 主键 |
| name | String(100) | 咨询师姓名 | 非空 |
| avatar | String(255) | 头像URL | 可空 |
| title | String(100) | 职称 | 可空 |
| tags_json | Text | 专业领域标签 | JSON格式存储 |
| price | Float | 咨询价格(每小时) | 默认0.0 |
| rating | Float | 评分 | 默认0.0 |
| consultation_count | Integer | 咨询次数 | 默认0 |
| introduction | Text | 简介 | 可空 |

### appointments 预约表

存储咨询预约信息。

| 字段名 | 类型 | 说明 | 约束 |
| --- | --- | --- | --- |
| id | Integer | 预约ID | 主键，自增 |
| user_id | String(50) | 用户ID | 非空 |
| counselor_id | String(50) | 咨询师ID | 非空 |
| appointment_time | DateTime | 预约时间 | 非空 |
| status | Integer | 预约状态 | 默认0 (0-待确认，1-已确认，2-已完成，3-已取消) |

### reviews 评价表

存储用户对咨询师的评价。

| 字段名 | 类型 | 说明 | 约束 |
| --- | --- | --- | --- |
| id | String(50) | 评价ID | 主键 |
| counselor_id | String(50) | 咨询师ID | 非空 |
| order_id | String(50) | 订单ID | 非空 |
| content | Text | 评价内容 | 可空 |
| rating | Integer | 评分 | 默认5 |

### disease_tags 疾病标签表

存储心理疾病或问题的标签。

| 字段名 | 类型 | 说明 | 约束 |
| --- | --- | --- | --- |
| id | String(50) | 标签ID | 主键 |
| name | String(100) | 标签名称 | 非空 |
| description | String(500) | 标签描述 | 可空 |

### announcements 公告表

存储系统公告信息。

| 字段名 | 类型 | 说明 | 约束 |
| --- | --- | --- | --- |
| id | String(50) | 公告ID | 主键 |
| counselor_id | String(50) | 咨询师ID | 非空 |
| service_id | String(50) | 服务ID | 非空 |
| user_id | String(50) | 用户ID | 非空 |
| date | String(20) | 日期 | 非空 |
| note | String(500) | 备注 | 可空 |
| time_slot | String(50) | 时间段 | 非空 |
| status | Integer | 状态 | 默认1 |

## 课程管理相关表

### courses 课程表

存储课程基本信息。

| 字段名 | 类型 | 说明 | 约束 |
| --- | --- | --- | --- |
| id | String(50) | 课程ID | 主键 |
| title | String(200) | 课程标题 | 非空 |
| cover_image | String(255) | 课程封面图片URL | 可空 |
| teacher | String(100) | 教师姓名 | 非空 |
| teacher_title | String(100) | 教师职称 | 可空 |
| teacher_avatar | String(255) | 教师头像URL | 可空 |
| price | Float | 课程现价 | 默认0.0 |
| original_price | Float | 课程原价 | 默认0.0 |
| lesson_count | Integer | 课时数量 | 默认0 |
| student_count | Integer | 学生数量 | 默认0 |
| rating | Float | 课程评分 | 默认0.0 |
| _tags | Text | 课程标签列表 | JSON格式存储 |
| description | Text | 课程描述 | 可空 |

### course_outlines 课程大纲表

存储课程章节信息。

| 字段名 | 类型 | 说明 | 约束 |
| --- | --- | --- | --- |
| id | Integer | 章节ID | 主键，自增 |
| course_id | String(50) | 课程ID | 非空 |
| title | String(200) | 章节标题 | 非空 |
| content | Text | 章节内容 | 可空 |
| sort_order | Integer | 排序序号 | 默认0 |

## 订单与支付相关表

### orders 订单表

存储订单信息。

| 字段名 | 类型 | 说明 | 约束 |
| --- | --- | --- | --- |
| id | String(50) | 订单ID | 主键 |
| user_id | String(50) | 用户ID | 非空 |
| product_id | String(50) | 商品ID | 非空 |
| type | Integer | 商品类型 | 非空 (1-课程，2-咨询) |
| amount | Float | 订单金额 | 默认0.0 |
| status | Integer | 支付状态 | 默认0 (0-未支付，1-已支付，2-已退款) |

## 用户交互相关表

### user_favorites 用户收藏表

存储用户收藏的内容。

| 字段名 | 类型 | 说明 | 约束 |
| --- | --- | --- | --- |
| id | String(50) | 收藏ID | 主键 |
| user_id | String(50) | 用户ID | 非空 |
| item_id | String(50) | 收藏项ID | 非空 |
| item_type | String(50) | 收藏项类型 | 非空 |

### categories 咨询类型表

存储咨询服务的分类。

| 字段名 | 类型 | 说明 | 约束 |
| --- | --- | --- | --- |
| id | String(50) | 类型ID | 主键 |
| name | String(100) | 类型名称 | 非空 |
| icon | String(255) | 图标URL | 可空 |
| path | String(255) | 跳转路径 | 可空 |
| description | String(500) | 类型描述 | 可空 |
| sort_order | Integer | 排序顺序 | 默认0 |
| status | Integer | 状态 | 默认1 (0-禁用，1-启用) |

## UI相关表

### banners 轮播图表

存储首页轮播图信息。

| 字段名 | 类型 | 说明 | 约束 |
| --- | --- | --- | --- |
| id | Integer | 轮播图ID | 主键，自增 |
| title | String(100) | 轮播图标题 | 非空 |
| image_url | String(255) | 图片URL | 非空 |
| link_url | String(255) | 跳转链接 | 可空 |
| sort_order | Integer | 排序顺序 | 默认0 |
| status | Integer | 状态 | 默认1 (0-禁用，1-启用) |

### tab_bars 底部导航栏表

存储移动端底部导航栏配置。

| 字段名 | 类型 | 说明 | 约束 |
| --- | --- | --- | --- |
| id | String(50) | 导航项ID | 主键 |
| icon | String(255) | 图标URL | 可空 |
| active_icon | String(255) | 激活态图标URL | 可空 |
| text | String(50) | 导航文本 | 非空 |
| path | String(255) | 跳转路径 | 可空 |
| sort_order | Integer | 排序顺序 | 默认0 |
| status | Integer | 状态 | 默认1 (0-禁用，1-启用) |
| role | String(20) | 角色 | 默认'user' (user-普通用户，counselor-咨询师) |

## 场所相关表

### workspaces 心理工作室表

存储心理工作室信息。

| 字段名 | 类型 | 说明 | 约束 |
| --- | --- | --- | --- |
| id | String(50) | 工作室ID | 主键 |
| name | String(200) | 工作室名称 | 非空 |
| cover_image | String(255) | 封面图片URL | 可空 |
| address | String(500) | 详细地址 | 可空 |
| distance | Float | 距离(km) | 默认0.0 |
| business_hours | String(200) | 营业时间 | 可空 |
| _environment_images | Text | 环境照片URL列表 | JSON格式存储 |
| introduction | Text | 工作室简介 | 可空 |
| slogan | String(500) | 工作室寄语 | 可空 |
| latitude | Float | 纬度 | 默认0.0 |
| longitude | Float | 经度 | 默认0.0 |
| status | Integer | 状态 | 默认1 (0-关闭，1-营业中) |

### groups 团体小组表

存储团体心理辅导小组信息。

| 字段名 | 类型 | 说明 | 约束 |
| --- | --- | --- | --- |
| id | String(50) | 小组ID | 主键 |
| title | String(200) | 小组标题 | 非空 |
| cover_image | String(255) | 封面图片URL | 可空 |
| counselor_id | String(50) | 导师ID | 非空 |
| counselor_name | String(100) | 导师姓名 | 非空 |
| price | Float | 价格(元/人) | 默认0.0 |
| capacity | Integer | 人数容量 | 默认0 |
| enrolled | Integer | 已报名人数 | 默认0 |
| location | String(200) | 地点 | 可空 |
| city | String(100) | 城市 | 可空 |
| type | String(50) | 类型 | 可空 (线上/线下) |
| start_date | String(20) | 开始日期 | 可空 |
| duration | String(100) | 持续时间 | 可空 |
| schedule | String(200) | 时间安排 | 可空 |
| description | Text | 课程介绍 | 可空 |
| status | Integer | 状态 | 默认1 (0-未开始，1-报名中，2-已结束) |

## 表关系说明

1. **用户与角色**：多对多关系，通过 `user_roles` 表关联
2. **角色与菜单**：多对多关系，通过 `roles` 表中的 `menu_ids_json` 字段关联
3. **用户与密码**：一对一关系，通过 `user_passwords` 表中的 `user_id` 关联
4. **用户与预约**：一对多关系，一个用户可以有多个预约
5. **咨询师与预约**：一对多关系，一个咨询师可以有多个预约
6. **课程与课程大纲**：一对多关系，一个课程可以有多个章节
7. **用户与收藏**：一对多关系，一个用户可以有多个收藏
8. **咨询师与评价**：一对多关系，一个咨询师可以有多个评价
9. **订单与评价**：一对一关系，一个订单对应一个评价
10. **咨询师与团体小组**：一对多关系，一个咨询师可以创建多个团体小组

## 索引建议

1. `users` 表：为 `username`, `phone`, `email` 字段创建索引
2. `counselors` 表：为 `name` 字段创建索引
3. `appointments` 表：为 `user_id`, `counselor_id`, `appointment_time` 字段创建索引
4. `courses` 表：为 `title`, `teacher` 字段创建索引
5. `orders` 表：为 `user_id`, `product_id`, `status` 字段创建索引
6. `user_favorites` 表：为 `user_id`, `item_id` 字段创建索引
7. `workspaces` 表：为 `name`, `city` 字段创建索引
8. `groups` 表：为 `counselor_id`, `city`, `status` 字段创建索引

## 数据完整性约束

1. 外键约束：确保关联字段引用的记录存在
2. 唯一性约束：如 `user_passwords` 表中的 `user_id` 字段，确保一个用户只有一个密码记录
3. 非空约束：确保必要字段不为空
4. 默认值：为部分字段设置合理的默认值，如状态字段默认为启用状态
5. 数据类型约束：确保数据类型与业务需求匹配，如价格字段使用 Float 类型
