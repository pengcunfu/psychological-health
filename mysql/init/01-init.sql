-- 心理健康平台数据库初始化脚本
-- 创建数据库和用户权限

-- 创建数据库（如果不存在）
CREATE DATABASE IF NOT EXISTS `psychological_health` 
CHARACTER SET utf8mb4 
COLLATE utf8mb4_unicode_ci;

-- 使用数据库
USE `psychological_health`;

-- 创建用户并授权（如果不存在）
CREATE USER IF NOT EXISTS 'app_user'@'%' IDENTIFIED BY 'app_password';
GRANT ALL PRIVILEGES ON `psychological_health`.* TO 'app_user'@'%';
FLUSH PRIVILEGES;

-- 设置字符集
SET NAMES utf8mb4;
SET CHARACTER_SET_CLIENT = utf8mb4;
SET CHARACTER_SET_CONNECTION = utf8mb4;
SET CHARACTER_SET_DATABASE = utf8mb4;
SET CHARACTER_SET_RESULTS = utf8mb4;
SET CHARACTER_SET_SERVER = utf8mb4;

-- 显示数据库信息
SHOW DATABASES;
SHOW GRANTS FOR 'app_user'@'%'; 