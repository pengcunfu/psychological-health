本项目为心理健康服务后端，基于 Flask 框架实现，提供了用户、咨询师、课程、预约、订单、公告等相关接口，适用于小程序或 Web 前端对接。

## 主要功能
- 用户管理
- 咨询师管理
- 课程管理
- 预约管理
- 订单管理
- 公告管理
- 疾病标签管理
- 用户收藏与评价

## 目录结构
```
wx-server/
  ├── app.py                # Flask 应用入口
  ├── controller/           # 路由蓝图目录
  ├── models/               # 数据模型目录
  ├── config.yaml           # 配置文件（支持多环境）
  ├── requirements.txt      # 依赖文件
  └── README.md             # 项目说明
```

## 配置说明
本项目使用 `config.yaml` 作为配置文件，支持开发（development）、测试（testing）、生产（production）三种环境。你可以根据实际需求修改各环境下的参数。

### 示例 config.yaml
```yaml
development:
  DEBUG: true
  SECRET_KEY: dev-secret-key
  DATABASE_URI: sqlite:///dev.db
  CORS_ORIGINS: '*'

testing:
  DEBUG: true
  SECRET_KEY: test-secret-key
  DATABASE_URI: sqlite:///test.db
  CORS_ORIGINS: '*'

production:
  DEBUG: false
  SECRET_KEY: prod-secret-key
  DATABASE_URI: sqlite:///prod.db
  CORS_ORIGINS: 'https://yourdomain.com'
```

### 切换环境
你可以通过设置环境变量 `APP_ENV` 来切换不同的配置环境，例如：
```bash
set APP_ENV=development  # Windows
export APP_ENV=production  # Linux/Mac
```

## 安装依赖
```bash
pip install -r requirements.txt
```

## 启动项目
```bash
python app.py
```

## 说明
- 已支持跨域（CORS），可直接对接前端。
- 仅包含接口路由定义，具体业务逻辑需自行实现。

如有问题欢迎反馈！ 