# MySQL 数据库配置说明

## 概述

本项目使用MySQL 8.0作为主数据库，通过Docker容器化部署。

## 配置说明

### 环境变量

在docker-compose.yml中配置的MySQL环境变量：

- `MYSQL_ROOT_PASSWORD`: root用户密码
- `MYSQL_DATABASE`: 应用数据库名称
- `MYSQL_USER`: 应用数据库用户
- `MYSQL_PASSWORD`: 应用数据库密码

### 数据库连接信息

- **主机**: localhost (本地) 或 服务器IP
- **端口**: 3306
- **数据库名**: psychological_health
- **用户名**: app_user
- **密码**: app_password
- **字符集**: utf8mb4

## 使用方法

### 1. 启动服务

```bash
# 启动所有服务
docker-compose up -d

# 仅启动MySQL
docker-compose up -d db
```

### 2. 连接数据库

#### 使用命令行客户端
```bash
# 连接到MySQL容器
docker exec -it psychological-health_db_1 mysql -u app_user -p

# 或者使用root用户
docker exec -it psychological-health_db_1 mysql -u root -p
```

#### 使用图形化工具
- **Navicat**: 连接localhost:3306
- **phpMyAdmin**: 访问 http://localhost:8080 (如果部署了phpMyAdmin)
- **MySQL Workbench**: 连接localhost:3306

### 3. 查看日志

```bash
# 查看MySQL日志
docker-compose logs db

# 实时查看日志
docker-compose logs -f db
```

### 4. 备份和恢复

#### 备份数据库
```bash
# 备份整个数据库
docker exec psychological-health_db_1 mysqldump -u root -p psychological_health > backup.sql

# 备份特定表
docker exec psychological-health_db_1 mysqldump -u root -p psychological_health users counselors > tables_backup.sql
```

#### 恢复数据库
```bash
# 恢复数据库
docker exec -i psychological-health_db_1 mysql -u root -p psychological_health < backup.sql
```

## 性能优化

### 内存配置

当前配置的内存使用：
- `innodb_buffer_pool_size`: 256M (InnoDB缓冲池)
- `query_cache_size`: 32M (查询缓存)

根据服务器内存调整：
- 小内存服务器 (1-2GB): 保持当前配置
- 中等内存服务器 (4-8GB): 增加到512M-1GB
- 大内存服务器 (16GB+): 增加到2-4GB

### 连接数配置

- `max_connections`: 200 (最大连接数)
- 根据应用负载调整

## 故障排除

### 常见问题

1. **连接被拒绝**
   ```bash
   # 检查MySQL服务状态
   docker-compose ps db
   
   # 检查端口是否开放
   netstat -tlnp | grep 3306
   ```

2. **字符集问题**
   ```sql
   -- 检查字符集设置
   SHOW VARIABLES LIKE 'character_set%';
   SHOW VARIABLES LIKE 'collation%';
   ```

3. **权限问题**
   ```sql
   -- 检查用户权限
   SHOW GRANTS FOR 'app_user'@'%';
   ```

### 重置数据库

如果需要完全重置数据库：

```bash
# 停止服务
docker-compose down

# 删除数据卷
docker volume rm psychological-health_mysql_data

# 重新启动
docker-compose up -d
```

## 安全建议

1. **修改默认密码**: 生产环境中修改所有默认密码
2. **限制网络访问**: 只允许应用服务器访问数据库
3. **定期备份**: 设置自动备份策略
4. **监控日志**: 监控慢查询和错误日志

## 扩展功能

### 添加phpMyAdmin

如果需要图形化管理界面，可以在docker-compose.yml中添加：

```yaml
phpmyadmin:
  image: phpmyadmin/phpmyadmin
  environment:
    PMA_HOST: db
    PMA_PORT: 3306
    PMA_USER: app_user
    PMA_PASSWORD: app_password
  ports:
    - "8080:80"
  depends_on:
    - db
```

### 主从复制

对于生产环境，可以配置MySQL主从复制以提高可用性和性能。 