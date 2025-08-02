# Swagger API 文档集成说明

## 概述

本项目已成功集成 Swagger API 文档，使用 `flask-restx` 库提供交互式 API 文档界面。

## 访问方式

启动服务器后，可通过以下地址访问 Swagger 文档：

- **Swagger UI**: `http://localhost:5000/api/docs/`
- **API JSON**: `http://localhost:5000/api/swagger.json`

## 功能特性

### 1. 交互式文档
- 提供完整的 API 接口文档
- 支持在线测试 API 接口
- 自动生成请求/响应示例
- 支持参数验证和错误提示

### 2. 认证支持
- 支持 JWT Bearer Token 认证
- 在 Swagger UI 中可配置认证信息
- 自动在请求头中添加 Authorization

### 3. 数据模型
- 完整的请求/响应数据模型定义
- 支持数据类型验证
- 提供示例数据

## 已集成的 API 模块

### 1. 用户管理 (`/api/users`)
- `GET /api/users` - 获取用户列表（支持分页和搜索）
- `POST /api/users` - 创建新用户
- `GET /api/users/{user_id}` - 获取用户详情
- `PUT /api/users/{user_id}` - 更新用户信息
- `DELETE /api/users/{user_id}` - 删除用户

### 2. 咨询师管理 (`/api/counselors`)
- `GET /api/counselors` - 获取咨询师列表
- `POST /api/counselors` - 创建新咨询师
- `GET /api/counselors/{counselor_id}` - 获取咨询师详情
- `PUT /api/counselors/{counselor_id}` - 更新咨询师信息
- `DELETE /api/counselors/{counselor_id}` - 删除咨询师

### 3. 订单管理 (`/api/orders`)
- `GET /api/orders` - 获取订单列表（支持多条件筛选）
- `POST /api/orders` - 创建新订单
- `GET /api/orders/{order_id}` - 获取订单详情
- `PUT /api/orders/{order_id}` - 更新订单状态
- `DELETE /api/orders/{order_id}` - 删除订单
- `POST /api/orders/{order_id}/pay` - 支付订单

## 使用指南

### 1. 启动服务
```bash
# 安装依赖
pip install -r requirements.txt

# 启动服务
python app.py
```

### 2. 访问文档
打开浏览器访问：`http://localhost:5000/api/docs/`

### 3. 测试 API
1. 在 Swagger UI 中选择要测试的接口
2. 点击 "Try it out" 按钮
3. 填写必要的参数
4. 点击 "Execute" 执行请求
5. 查看响应结果

### 4. 认证配置
1. 点击页面右上角的 "Authorize" 按钮
2. 在 Bearer 字段中输入 JWT Token
3. 点击 "Authorize" 确认
4. 后续请求将自动携带认证信息

## 扩展其他 API

如需为其他 API 模块添加 Swagger 文档，请按以下步骤操作：

### 1. 创建 Swagger API 文件
```python
# 例如：api/swagger_example.py
from flask_restx import Resource, fields
from utils.swagger_config import api

# 创建命名空间
example_ns = api.namespace('examples', description='示例接口')

# 定义数据模型
example_model = api.model('Example', {
    'id': fields.String(description='ID'),
    'name': fields.String(description='名称')
})

# 定义 API 资源
@example_ns.route('')
class ExampleListAPI(Resource):
    @api.doc('get_examples')
    @api.marshal_with(success_response)
    def get(self):
        """获取示例列表"""
        # 实现逻辑
        pass
```

### 2. 注册命名空间
在 `utils/swagger_config.py` 中添加：
```python
from api.swagger_example import example_ns
api.add_namespace(example_ns)
```

### 3. 重启服务
重启 Flask 应用，新的 API 文档将自动出现在 Swagger UI 中。

## 注意事项

1. **数据验证**: 使用 `@api.expect()` 装饰器进行请求数据验证
2. **响应模型**: 使用 `@api.marshal_with()` 装饰器定义响应格式
3. **错误处理**: 使用 `@api.response()` 装饰器定义错误响应
4. **文档描述**: 在函数文档字符串中提供详细的接口说明
5. **示例数据**: 在模型定义中提供 `example` 参数

## 技术栈

- **Flask-RESTX**: Swagger 集成库
- **Flask**: Web 框架
- **SQLAlchemy**: ORM 数据库操作
- **Swagger UI**: 交互式 API 文档界面

## 相关文件

- `utils/swagger_config.py` - Swagger 配置和通用模型
- `api/swagger_*.py` - 各模块的 Swagger API 定义
- `requirements.txt` - 项目依赖（已添加 flask-restx）
- `app.py` - 主应用文件（已注册 Swagger 蓝图）

## 常见问题

### Q: 如何自定义 Swagger UI 主题？
A: 可以在 `swagger_config.py` 中的 Api 配置中添加自定义 CSS 和 JS。

### Q: 如何添加全局请求头？
A: 在 `authorizations` 配置中添加新的认证方式。

### Q: 如何隐藏某些接口？
A: 使用 `@api.doc(False)` 装饰器可以隐藏接口。

### Q: 如何自定义错误响应格式？
A: 在 `swagger_config.py` 中修改 `error_response` 模型定义。

---

更多详细信息请参考 [Flask-RESTX 官方文档](https://flask-restx.readthedocs.io/)