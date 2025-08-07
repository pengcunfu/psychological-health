# Redis会话存储系统

## 概述

本系统已从内存会话存储升级为基于Redis的分布式会话存储，提供更好的性能、可靠性和可扩展性。

## 特性

### ✅ 已实现的功能

1. **Redis会话存储**
   - 使用Redis存储用户登录会话
   - 支持会话过期自动清理
   - 支持会话有效期延长

2. **降级机制**
   - Redis不可用时自动降级到内存存储
   - 内存模式下定期清理过期会话
   - 平滑的故障转移

3. **监控和健康检查**
   - Redis连接状态监控
   - 会话统计信息
   - 健康检查接口

## 配置

### Redis配置

在 `config.yaml` 或 `config-prod.yaml` 中配置Redis连接：

```yaml
# Redis配置
REDIS:
  HOST: localhost          # Redis服务器地址
  PORT: 6379              # Redis端口
  DB: 0                   # Redis数据库编号
  PASSWORD: null          # Redis密码（可选）
  DECODE_RESPONSES: true  # 自动解码响应

# Session配置
SESSION:
  TYPE: redis
  PERMANENT: false
  USE_SIGNER: true
  KEY_PREFIX: 'session:'
  REDIS_KEY_PREFIX: 'session:'
  COOKIE_HTTPONLY: true
  COOKIE_SECURE: false    # 开发环境设为false，生产环境设为true
  EXPIRES: 7200           # 会话过期时间（秒）
```

### 环境变量配置

支持通过环境变量覆盖配置：

```bash
export REDIS_HOST=localhost
export REDIS_PORT=6379
export REDIS_DB=0
export REDIS_PASSWORD=your_password
```

## 部署

### 使用Docker Compose

项目已包含Redis服务配置，直接启动：

```bash
docker-compose up -d
```

### 手动部署Redis

1. **安装Redis**
   ```bash
   # Ubuntu/Debian
   sudo apt-get install redis-server
   
   # CentOS/RHEL
   sudo yum install redis
   
   # macOS
   brew install redis
   ```

2. **启动Redis服务**
   ```bash
   # Linux
   sudo systemctl start redis
   
   # macOS
   brew services start redis
   ```

3. **验证Redis运行**
   ```bash
   redis-cli ping
   # 应该返回: PONG
   ```

## API接口

### 会话统计

获取当前会话统计信息：

```http
GET /api/session/stats
```

响应示例：
```json
{
  "success": true,
  "data": {
    "total_sessions": 15,
    "redis_available": true
  }
}
```

### Redis健康检查

检查Redis服务状态：

```http
GET /api/health/redis
```

响应示例：
```json
{
  "success": true,
  "data": {
    "status": "healthy",
    "message": "Redis连接正常",
    "session_count": 15
  }
}
```

## 故障处理

### Redis连接失败

当Redis不可用时，系统会：

1. **自动降级**：切换到内存存储模式
2. **日志记录**：记录Redis连接失败信息
3. **继续服务**：不影响用户正常登录使用

### 内存模式特点

- 会话数据存储在应用内存中
- 应用重启会丢失所有会话
- 自动清理过期会话（每5分钟）
- 适合开发环境和小规模部署

### 恢复Redis服务

Redis服务恢复后，系统会：

1. 自动重新连接Redis
2. 新的会话将存储到Redis
3. 现有内存会话继续有效直到过期

## 性能优化

### Redis配置优化

在Redis配置文件 `redis.conf` 中：

```ini
# 内存优化
maxmemory 256mb
maxmemory-policy allkeys-lru

# 持久化配置（根据需求选择）
save 900 1
save 300 10
save 60 10000

# 网络优化
tcp-keepalive 60
timeout 300
```

### 应用层优化

1. **连接池配置**：Redis客户端使用连接池
2. **超时设置**：合理设置连接和操作超时
3. **重试机制**：网络异常时自动重试

## 监控建议

### 关键指标

1. **Redis状态**
   - 连接状态
   - 内存使用率
   - 命令执行延迟

2. **会话指标**
   - 活跃会话数量
   - 会话创建/销毁速率
   - 平均会话时长

### 监控工具

- Redis自带的 `redis-cli --stat`
- 第三方监控工具如Prometheus + Grafana
- 应用日志监控

## 安全考虑

### Redis安全

1. **访问控制**
   ```ini
   # redis.conf
   bind 127.0.0.1
   requirepass your_strong_password
   ```

2. **网络隔离**
   - 使用防火墙限制Redis端口访问
   - 在生产环境中不要暴露Redis到公网

### 会话安全

1. **令牌安全**：使用强随机令牌
2. **传输安全**：HTTPS传输
3. **存储安全**：敏感信息不存储在会话中

## 故障排查

### 常见问题

1. **Redis连接超时**
   ```
   检查Redis服务状态
   检查网络连接
   检查防火墙设置
   ```

2. **内存不足**
   ```
   检查Redis内存使用
   清理过期会话
   调整maxmemory配置
   ```

3. **会话丢失**
   ```
   检查Redis持久化配置
   检查会话过期时间设置
   查看应用日志
   ```

### 日志分析

关键日志信息：
```
Redis连接成功，会话将存储到Redis
Redis连接失败，会话将存储到内存（降级模式）
会话已创建到Redis: 12345678...
会话已从Redis删除: 12345678...
```

## 升级说明

### 从内存存储升级

1. **数据迁移**：无需迁移，旧会话自然过期
2. **配置更新**：添加Redis配置项
3. **依赖安装**：安装Redis相关依赖
4. **服务重启**：重启应用服务

### 兼容性

- 向后兼容现有API接口
- 客户端无需任何修改
- 会话令牌格式保持不变

## 开发指南

### 本地开发

1. **启动Redis**
   ```bash
   redis-server
   ```

2. **配置环境**
   ```bash
   export REDIS_HOST=localhost
   export REDIS_PORT=6379
   ```

3. **运行应用**
   ```bash
   python app.py
   ```

### 测试

运行Redis相关测试：
```bash
# 测试Redis连接
curl http://localhost:5000/api/health/redis

# 测试会话统计
curl http://localhost:5000/api/session/stats
```

---

## 联系信息

如有问题或建议，请联系开发团队。 