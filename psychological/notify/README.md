# 站内通知系统

基于心理健康平台的完整站内通知解决方案，提供丰富的通知功能和灵活的配置选项。

## 🚀 功能特性

### 核心功能
- **多类型通知**: 支持系统、业务、社交等多种通知类型
- **优先级管理**: 四级优先级（低、普通、高、紧急）
- **模板系统**: 预定义模板和自定义模板
- **定时发送**: 支持延时和定时通知
- **批量通知**: 高效的批量发送机制
- **通知统计**: 详细的发送和阅读统计

### 高级特性
- **频率控制**: 防止通知骚扰的智能限制
- **用户配置**: 个性化的通知偏好设置
- **过期管理**: 自动清理过期和旧通知
- **状态管理**: 未读、已读、归档、删除状态
- **关联对象**: 与业务对象的关联和跳转
- **扩展数据**: 灵活的元数据存储

## 📋 系统架构

```
notify/
├── __init__.py          # 模块初始化
├── types.py             # 类型定义和枚举
├── models.py            # 数据模型
├── config.py            # 配置文件
├── service.py           # 核心服务
├── manager.py           # 高级管理功能
├── triggers.py          # 业务触发器
├── migrations.py        # 数据库迁移
├── examples.py          # 使用示例
└── README.md           # 文档说明
```

## 🛠️ 安装配置

### 1. 初始化数据库

```bash
# 方法1: 使用命令行工具
flask notification init

# 方法2: 在代码中调用
from psychological.notify.migrations import migrate_notification_system
migrate_notification_system()
```

### 2. 注册API蓝图

在 `app.py` 中添加：

```python
from psychological.api.notification import notification_bp
app.register_blueprint(notification_bp)
```

### 3. 注册命令行工具

在 `commands/__init__.py` 中添加：

```python
from .notification import register_notification_commands
register_notification_commands(app)
```

## 📖 使用指南

### 基本用法

#### 1. 发送简单通知

```python
from psychological.notify.service import notification_service
from psychological.notify.types import NotificationType, NotificationPriority

# 发送通知
result = notification_service.create_notification(
    recipient_id="user123",
    title="欢迎加入平台",
    content="感谢您的注册，开始您的心理健康之旅吧！",
    notification_type=NotificationType.SYSTEM,
    priority=NotificationPriority.NORMAL
)
```

#### 2. 使用模板发送通知

```python
# 使用预定义模板
result = notification_service.create_notification_from_template(
    template_code='appointment_confirmed',
    recipient_id="user123",
    variables={
        'appointment_time': '2024-01-15 14:30:00',
        'counselor_name': '张医生',
        'location': '心理咨询室A'
    }
)
```

#### 3. 批量发送通知

```python
from psychological.notify.manager import notification_manager

# 批量发送
result = notification_manager.broadcast_notification(
    user_ids=["user1", "user2", "user3"],
    title="系统维护通知",
    content="系统将于今晚进行维护升级。"
)
```

### 业务集成

#### 1. 在业务代码中触发通知

```python
from psychological.notify.triggers import notification_triggers

# 预约确认时
def confirm_appointment(appointment):
    # 更新预约状态
    appointment.status = 'confirmed'
    db.session.commit()
    
    # 发送确认通知
    notification_triggers.on_appointment_confirmed(
        appointment_id=appointment.id,
        user_id=appointment.user_id,
        appointment_time=appointment.appointment_time.isoformat(),
        counselor_name=appointment.counselor.name
    )
```

#### 2. 在社交功能中集成

```python
# 用户关注时
def follow_user(follower_id, following_id):
    # 创建关注记录
    follow = SocialFollow(follower_id=follower_id, following_id=following_id)
    db.session.add(follow)
    db.session.commit()
    
    # 发送关注通知
    notification_triggers.on_user_followed(
        follower_id=follower_id,
        following_id=following_id,
        follower_name=get_user_name(follower_id)
    )
```

### API 使用

#### 1. 获取用户通知

```http
GET /notification?page=1&per_page=20&status=unread
Authorization: Bearer {token}
```

#### 2. 标记通知已读

```http
POST /notification/mark-read
Content-Type: application/json

{
    "notification_ids": ["id1", "id2"]
}
```

#### 3. 获取未读数量

```http
GET /notification/unread-count
Authorization: Bearer {token}
```

## 🔧 配置选项

### 系统配置

在 `config.py` 中设置：

```python
class NotificationConfig:
    # 通知保留时间
    NOTIFICATION_RETENTION_DAYS = 90
    READ_NOTIFICATION_RETENTION_DAYS = 30
    
    # 频率控制
    DEFAULT_MAX_DAILY_NOTIFICATIONS = 50
    DEFAULT_MAX_HOURLY_NOTIFICATIONS = 10
    
    # 批量操作限制
    MAX_BATCH_SIZE = 1000
```

### 用户配置

用户可以配置不同类型通知的接收偏好：

```python
# 更新用户配置
notification_manager.update_user_notification_config(
    user_id="user123",
    notification_type=NotificationType.SOCIAL_LIKE,
    config_data={
        'in_app_enabled': True,
        'email_enabled': False,
        'quiet_start_time': '22:00',
        'quiet_end_time': '08:00'
    }
)
```

## 📊 通知类型

系统支持以下通知类型：

| 类型 | 说明 | 示例场景 |
|------|------|----------|
| SYSTEM | 系统通知 | 系统维护、版本更新 |
| ANNOUNCEMENT | 公告通知 | 平台公告、活动通知 |
| APPOINTMENT | 预约通知 | 预约确认、提醒、取消 |
| ORDER | 订单通知 | 支付成功、退款、发货 |
| COURSE | 课程通知 | 订阅成功、学习提醒 |
| ASSESSMENT | 测评通知 | 测评完成、结果生成 |
| SOCIAL_FOLLOW | 关注通知 | 新增关注者 |
| SOCIAL_LIKE | 点赞通知 | 内容被点赞 |
| SOCIAL_COMMENT | 评论通知 | 内容被评论 |
| ACCOUNT | 账户通知 | 注册欢迎、资料完善 |
| SECURITY | 安全通知 | 异地登录、密码修改 |
| REMINDER | 提醒通知 | 定时提醒、任务提醒 |
| PROMOTION | 推广通知 | 优惠活动、推荐内容 |

## 🎯 预定义模板

系统内置了常用的通知模板：

### 预约相关
- `appointment_confirmed` - 预约确认通知
- `appointment_cancelled` - 预约取消通知  
- `appointment_reminder` - 预约提醒通知

### 订单相关
- `order_paid` - 订单支付成功
- `order_refunded` - 订单退款通知

### 课程相关
- `course_subscribed` - 课程订阅成功
- `course_completed` - 课程完成通知

### 社交相关
- `social_followed` - 新关注通知
- `social_liked` - 内容被点赞
- `social_commented` - 内容被评论

### 系统安全
- `system_announcement` - 系统公告
- `security_login` - 异地登录通知
- `security_password_changed` - 密码修改通知

## 🛡️ 最佳实践

### 1. 合理设置优先级

```python
# 紧急通知：安全相关
NotificationPriority.URGENT

# 高优先级：重要业务操作
NotificationPriority.HIGH

# 普通优先级：一般业务通知
NotificationPriority.NORMAL

# 低优先级：社交互动
NotificationPriority.LOW
```

### 2. 使用模板提高一致性

```python
# 推荐：使用模板
notification_service.create_notification_from_template(
    template_code='order_paid',
    recipient_id=user_id,
    variables={'order_number': order.number}
)

# 避免：重复的硬编码
notification_service.create_notification(
    title='订单支付成功',
    content=f'您的订单 {order.number} 已支付成功...'
)
```

### 3. 设置合理的过期时间

```python
from datetime import datetime, timedelta

# 短期通知（如验证码）
expire_time = datetime.utcnow() + timedelta(minutes=10)

# 一般通知（如订单状态）
expire_time = datetime.utcnow() + timedelta(days=7)

# 重要通知（如系统公告）
expire_time = datetime.utcnow() + timedelta(days=30)
```

### 4. 批量操作优化

```python
# 对于大量用户，分批发送
user_ids = get_all_active_users()
batch_size = 500

for i in range(0, len(user_ids), batch_size):
    batch = user_ids[i:i + batch_size]
    notification_manager.broadcast_notification(
        user_ids=batch,
        title="系统公告",
        content="重要系统更新通知"
    )
```

## ⚡ 性能优化

### 1. 数据库索引
系统已创建必要的数据库索引：
- `(recipient_id, status, create_time)` - 用户通知查询
- `(type, priority, create_time)` - 类型和优先级查询
- `(related_type, related_id)` - 关联对象查询

### 2. 批量操作
- 使用 `broadcast_notification` 进行批量发送
- 限制单次批量操作的数量
- 异步处理大量通知

### 3. 定期清理
```bash
# 设置定时任务清理过期通知
flask notification cleanup-old

# 或在代码中调用
notification_service.cleanup_old_notifications()
```

## 🧪 测试

### 运行示例
```python
from psychological.notify.examples import NotificationExamples
NotificationExamples.run_all_examples()
```

### 命令行测试
```bash
# 发送测试通知
flask notification send --user-id user123 --title "测试通知" --content "这是一条测试通知"

# 使用模板发送
flask notification send-template --template-code appointment_confirmed --user-id user123 --variables '{"appointment_time":"2024-01-15 14:30","counselor_name":"张医生"}'

# 查看统计
flask notification stats --user-id user123 --days 7
```

## 📈 监控和统计

### 获取通知统计
```python
# 获取用户通知统计
result = notification_manager.get_notification_statistics(
    user_id="user123",
    start_date=datetime(2024, 1, 1),
    end_date=datetime(2024, 1, 31)
)

# 获取系统整体统计
result = notification_manager.get_notification_statistics()
```

### 监控指标
- 通知发送成功率
- 用户阅读率
- 不同类型通知的效果
- 系统性能指标

## 🔍 故障排除

### 常见问题

1. **通知没有发送**
   - 检查用户通知配置是否启用
   - 验证频率限制设置
   - 查看日志文件

2. **模板渲染失败**
   - 检查模板变量是否正确
   - 验证模板语法
   - 确认模板是否激活

3. **性能问题**
   - 检查数据库索引
   - 优化查询条件
   - 考虑异步处理

### 调试方法

```python
# 启用调试日志
import logging
logging.getLogger('psychological.notify').setLevel(logging.DEBUG)

# 检查系统状态
from psychological.notify.migrations import check_notification_system
check_notification_system()
```

## 🚀 扩展开发

### 添加新的通知类型

1. 在 `types.py` 中添加新类型：
```python
class NotificationType(enum.Enum):
    # ... 现有类型
    NEW_TYPE = "new_type"
```

2. 在 `config.py` 中添加模板：
```python
NOTIFICATION_TEMPLATES['new_template'] = {
    'name': '新通知模板',
    'type': 'new_type',
    'title_template': '新通知：$title',
    'content_template': '$content'
}
```

3. 在 `triggers.py` 中添加触发器：
```python
@staticmethod
def on_new_event(user_id, data):
    return notification_service.create_notification_from_template(
        template_code='new_template',
        recipient_id=user_id,
        variables=data
    )
```

### 自定义渲染引擎

```python
from psychological.notify.models import NotificationTemplate

class CustomTemplate(NotificationTemplate):
    def render_notification_data(self, variables_data):
        # 自定义渲染逻辑
        pass
```

## 📞 技术支持

如果您在使用过程中遇到问题，请：

1. 查看日志文件获取详细错误信息
2. 使用 `flask notification check` 检查系统状态
3. 参考本文档的故障排除部分
4. 联系技术支持团队

## 📄 许可证

本通知系统是心理健康平台的一部分，遵循项目的整体许可协议。
