# 数据库备份工具

这个目录包含了心理健康咨询系统的数据库脚本和备份工具。

## 文件说明

- `mental_health.sql`: 数据库初始化脚本
- `db_backup.py`: 数据库备份和恢复工具（Python版本）
- `db_backup.bat`: 数据库备份和恢复工具（Windows批处理版本）
- `.env`: 数据库配置文件（需要自行创建）
- `.env.example`: 数据库配置文件示例

## 环境要求

- MySQL 8.0
- Python 3.6+（如果使用Python版本工具）
- Windows系统（如果使用批处理版本工具）

## 使用说明

### 首次使用

1. 复制 `.env.example` 为 `.env`：
```bash
copy .env.example .env
```

2. 编辑 `.env` 文件，填入正确的数据库配置：
```env
MYSQL_HOME=MySQL安装路径
MYSQL_HOST=数据库主机
MYSQL_PORT=数据库端口
MYSQL_DATABASE=数据库名
MYSQL_USERNAME=用户名
MYSQL_PASSWORD=密码
```

### 使用备份工具

#### Python版本（推荐）

运行 Python 脚本：
```bash
python db_backup.py
```

#### Windows批处理版本

双击运行 `db_backup.bat`

两个版本都会显示相同的菜单：

1. Export Database（导出数据库）
   - 将自动导出数据库为 `mental_health_时间戳.sql`
   - 例如：`mental_health_20240421235959.sql`

2. Import Database（导入数据库）
   - 会显示当前目录下所有 SQL 文件
   - 选择要导入的文件编号即可

3. Exit（退出程序）

## 注意事项

1. 确保 MySQL 8.0 已正确安装
2. 确保 `.env` 文件中的配置正确
3. 运行备份工具需要管理员权限
4. 建议定期备份数据库
5. 导入数据库时会覆盖现有数据，请谨慎操作
6. Python版本需要安装Python 3.6或更高版本

## 目录结构

```
sql/
├── mental_health.sql     # 初始数据库脚本
├── db_backup.py         # 备份工具（Python版本）
├── db_backup.bat        # 备份工具（批处理版本）
├── .env                 # 数据库配置（被git忽略）
├── .env.example         # 配置文件示例
├── .gitignore          # git忽略配置
└── README.md           # 说明文档
```

## 版本特点对比

### Python版本（db_backup.py）
- 更好的错误处理
- 跨平台支持（Windows/Linux/Mac）
- 更安全的密码处理
- 更好的编码支持
- 更容易维护和扩展

### 批处理版本（db_backup.bat）
- 无需安装Python
- Windows原生支持
- 轻量级
- 适合简单使用场景

## 常见问题

1. 找不到 MySQL
   - 检查 `.env` 中的 `MYSQL_HOME` 路径是否正确
   - 确保 MySQL 已正确安装

2. 访问被拒绝
   - 检查用户名和密码是否正确
   - 确保用户有适当的数据库权限

3. 备份文件太大
   - 可以使用压缩工具压缩 SQL 文件
   - 建议定期清理旧的备份文件

4. Python版本问题
   - 确保安装了 Python 3.6 或更高版本
   - 可以使用 `python --version` 检查版本

5. 字符编码问题
   - Python版本默认使用 UTF-8 编码
   - 如果出现中文乱码，请检查数据库和文件的编码设置 