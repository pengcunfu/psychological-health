# 心理健康预约咨询系统

<p align="center">
	<img alt="logo" src="https://oscimg.oschina.net/oscnet/up-d3d0a9303e11d522a06cd263f3079027715.png">
</p>

## 项目介绍

心理健康预约咨询系统是一个基于 SpringBoot + Vue 的前后端分离项目。本系统旨在为用户提供便捷的心理咨询预约服务，帮助用户获得专业的心理健康指导。系统采用 RuoYi v3.8.9 框架开发，具有完善的权限管理和安全机制。

### 主要功能

1. 用户端功能
   - 在线心理咨询预约
   - 咨询师查询与筛选
   - 个人咨询记录管理
   - 在线支付功能
   - 评价反馈系统

2. 咨询师功能
   - 个人排班管理
   - 预约订单处理
   - 咨询记录管理
   - 用户反馈查看
   - 收入统计

3. 管理端功能
   - 用户管理
   - 咨询师管理
   - 预约订单管理
   - 咨询类型管理
   - 收费标准管理
   - 统计分析
   - 系统配置

### 技术架构

#### 后端技术栈

- 基础框架：Spring Boot 2.5.15
- 安全框架：Spring Security 5.7.12
- 权限认证：JWT 0.9.1
- 数据库连接池：Alibaba Druid 1.2.23
- 数据库分页：PageHelper 1.4.7
- 接口文档：Swagger 3.0.0
- 定时任务：Quartz
- 其他工具：FastJSON、POI、Velocity 等

#### 前端技术栈

管理后台：
- Vue.js
- Element UI
- Vue Router
- Vuex
- Axios
- ECharts

用户端：
- uni-app
- Vuex
- uView UI

### 项目结构

```
├── qiyun-admin        // 后台管理模块
├── qiyun-framework    // 核心框架
├── qiyun-system      // 系统功能
├── qiyun-quartz      // 定时任务
├── qiyun-generator   // 代码生成
├── qiyun-common      // 通用工具
├── qiyun-ur          // 用户端接口
├── ui-admin          // 管理后台前端
└── ui-user           // 用户端前端
```

### 环境要求

- JDK >= 1.8
- MySQL >= 5.7
- Maven >= 3.6
- Node.js >= 12
- Redis >= 5.0

### 部署说明

1. 后端部署
```bash
# 打包
mvn clean package

# 运行
java -jar qiyun-admin/target/qiyun-admin.jar
```

2. 前端部署
```bash
# 管理后台
cd ui-admin
npm install
npm run build:prod

# 用户端
cd ui-user
npm install
npm run build
```

### 在线体验

- 管理后台演示地址：http://xxx.xxx.xxx
- 用户端演示地址：http://xxx.xxx.xxx

管理员账号：admin/admin123

### 开发计划

- [ ] 视频咨询功能
- [ ] AI 智能问答
- [ ] 心理测评系统
- [ ] 小程序端适配
- [ ] 咨询师资质认证

### 获取帮助

如果您在使用过程中遇到任何问题，可以通过以下方式获取帮助：

- 提交 Issue
- 联系技术支持：support@xxx.com
- 官方QQ群：xxxxxx

### 版权说明

本项目基于 [MIT](https://opensource.org/licenses/MIT) 协议，请自由地享受和参与开源。

### 特别鸣谢

- 感谢 [RuoYi-Vue](https://gitee.com/y_project/RuoYi-Vue) 提供的优秀开源项目
- 感谢所有为这个项目做出贡献的开发者