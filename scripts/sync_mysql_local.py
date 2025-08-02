#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
MySQL数据库同步脚本
功能：将远程MySQL数据库同步到本地
使用方法：python sync_sql_local.py [配置文件路径]
"""

import os
import sys
import time
import yaml
import argparse
import subprocess
import logging
from datetime import datetime

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)

# 默认配置
DEFAULT_CONFIG = {
    "source": {
        "host": "remote_host",
        "port": 3306,
        "user": "remote_user",
        "password": "remote_password",
        "database": "remote_db"
    },
    "target": {
        "host": "localhost",
        "port": 3306,
        "user": "local_user",
        "password": "local_password",
        "database": "local_db"
    },
    "tables": [],  # 空列表表示同步所有表
    "exclude_tables": [],  # 排除的表
    "dump_options": "--single-transaction --quick --lock-tables=false",
    "backup_dir": "./backups"
}

def load_config(config_path):
    """加载YAML配置文件"""
    try:
        if not os.path.exists(config_path):
            logger.error(f"配置文件不存在: {config_path}")
            return None
        
        with open(config_path, 'r', encoding='utf-8') as f:
            config = yaml.safe_load(f)
        
        # 合并默认配置
        for key, value in DEFAULT_CONFIG.items():
            if key not in config:
                config[key] = value
        
        return config
    except Exception as e:
        logger.error(f"加载配置文件失败: {str(e)}")
        return None

def create_backup_dir(backup_dir):
    """创建备份目录"""
    if not os.path.exists(backup_dir):
        try:
            os.makedirs(backup_dir)
            logger.info(f"创建备份目录: {backup_dir}")
        except Exception as e:
            logger.error(f"创建备份目录失败: {str(e)}")
            return False
    return True

def get_tables(config):
    """获取需要同步的表列表"""
    source = config["source"]
    
    if config["tables"]:
        return config["tables"]
    
    try:
        cmd = f"mysql -h {source['host']} -P {source['port']} -u {source['user']} -p{source['password']} " \
              f"-e 'SHOW TABLES;' {source['database']}"
        
        output = subprocess.check_output(cmd, shell=True, stderr=subprocess.STDOUT).decode('utf-8')
        tables = [line for line in output.split('\n') if line and line != 'Tables_in_' + source['database']]
        
        # 排除不需要同步的表
        if config["exclude_tables"]:
            tables = [t for t in tables if t not in config["exclude_tables"]]
        
        return tables
    except subprocess.CalledProcessError as e:
        logger.error(f"获取表列表失败: {e.output.decode('utf-8')}")
        return []
    except Exception as e:
        logger.error(f"获取表列表失败: {str(e)}")
        return []

def dump_database(config, tables, backup_file):
    """导出数据库"""
    source = config["source"]
    
    try:
        tables_str = " ".join(tables)
        dump_options = config["dump_options"]
        
        cmd = f"mysqldump -h {source['host']} -P {source['port']} -u {source['user']} -p{source['password']} " \
              f"{dump_options} {source['database']} {tables_str} > {backup_file}"
        
        logger.info(f"开始导出数据库: {source['database']}")
        subprocess.run(cmd, shell=True, check=True)
        logger.info(f"数据库导出成功: {backup_file}")
        return True
    except subprocess.CalledProcessError as e:
        logger.error(f"导出数据库失败: {str(e)}")
        return False
    except Exception as e:
        logger.error(f"导出数据库失败: {str(e)}")
        return False

def restore_database(config, backup_file):
    """恢复数据库到本地"""
    target = config["target"]
    
    try:
        cmd = f"mysql -h {target['host']} -P {target['port']} -u {target['user']} -p{target['password']} " \
              f"{target['database']} < {backup_file}"
        
        logger.info(f"开始恢复数据库到本地: {target['database']}")
        subprocess.run(cmd, shell=True, check=True)
        logger.info(f"数据库恢复成功: {target['database']}")
        return True
    except subprocess.CalledProcessError as e:
        logger.error(f"恢复数据库失败: {str(e)}")
        return False
    except Exception as e:
        logger.error(f"恢复数据库失败: {str(e)}")
        return False

def sync_database(config_path):
    """同步数据库主函数"""
    # 加载配置
    config = load_config(config_path)
    if not config:
        return False
    
    # 创建备份目录
    backup_dir = config["backup_dir"]
    if not create_backup_dir(backup_dir):
        return False
    
    # 获取表列表
    tables = get_tables(config)
    if not tables:
        logger.error("没有找到要同步的表")
        return False
    
    logger.info(f"将同步以下表: {', '.join(tables)}")
    
    # 生成备份文件名
    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
    backup_file = os.path.join(backup_dir, f"{config['source']['database']}_{timestamp}.sql")
    
    # 导出数据库
    if not dump_database(config, tables, backup_file):
        return False
    
    # 恢复数据库到本地
    if not restore_database(config, backup_file):
        return False
    
    logger.info("数据库同步完成")
    return True

def create_sample_config():
    """创建示例配置文件"""
    config_path = "../config/sync_config.yaml"
    
    if os.path.exists(config_path):
        logger.warning(f"配置文件已存在: {config_path}")
        return
    
    with open(config_path, 'w', encoding='utf-8') as f:
        yaml.dump(DEFAULT_CONFIG, f, default_flow_style=False, allow_unicode=True, indent=2)
    
    logger.info(f"已创建示例配置文件: {config_path}")
    logger.info("请修改配置文件中的数据库连接信息后再运行同步命令")

def main():
    parser = argparse.ArgumentParser(description="MySQL数据库同步工具")
    parser.add_argument("config", nargs="?", default="sync_config.yaml", help="配置文件路径")
    parser.add_argument("--init", action="store_true", help="创建示例配置文件")
    
    args = parser.parse_args()
    
    if args.init:
        create_sample_config()
        return
    
    start_time = time.time()
    success = sync_database(args.config)
    end_time = time.time()
    
    if success:
        logger.info(f"同步完成，耗时: {end_time - start_time:.2f}秒")
    else:
        logger.error("同步失败")
        sys.exit(1)

if __name__ == "__main__":
    main()
