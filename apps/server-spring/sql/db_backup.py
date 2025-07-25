#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import time
import subprocess
from datetime import datetime
from pathlib import Path
from typing import Dict, Optional

def load_env(env_file: str = '.env') -> Dict[str, str]:
    """加载环境变量文件"""
    env_vars = {}
    try:
        with open(env_file, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#'):
                    key, value = line.split('=', 1)
                    env_vars[key.strip()] = value.strip()
        return env_vars
    except FileNotFoundError:
        print(f"错误: 找不到 {env_file} 文件")
        print(f"请复制 {env_file}.example 为 {env_file} 并配置正确的数据库信息")
        sys.exit(1)

def check_mysql_path(mysql_home: str) -> bool:
    """检查MySQL路径是否正确"""
    mysql_path = Path(mysql_home) / 'bin' / ('mysql.exe' if sys.platform == 'win32' else 'mysql')
    return mysql_path.exists()

def get_timestamp() -> str:
    """获取当前时间戳"""
    return datetime.now().strftime('%Y%m%d%H%M%S')

def list_sql_files() -> list:
    """列出当前目录下的所有SQL文件"""
    return sorted([f for f in os.listdir('.') if f.endswith('.sql')])

def export_database(env_vars: Dict[str, str]) -> None:
    """导出数据库"""
    timestamp = get_timestamp()
    output_file = f"mental_health_{timestamp}.sql"
    
    mysqldump_path = Path(env_vars['MYSQL_HOME']) / 'bin' / ('mysqldump.exe' if sys.platform == 'win32' else 'mysqldump')
    
    cmd = [
        str(mysqldump_path),
        f"-h{env_vars['MYSQL_HOST']}",
        f"-P{env_vars['MYSQL_PORT']}",
        f"-u{env_vars['MYSQL_USERNAME']}",
        f"-p{env_vars['MYSQL_PASSWORD']}",
        env_vars['MYSQL_DATABASE']
    ]
    
    try:
        print("正在导出数据库...")
        with open(output_file, 'w', encoding='utf-8') as f:
            subprocess.run(cmd, stdout=f, check=True)
        print(f"数据库成功导出到: {output_file}")
    except subprocess.CalledProcessError:
        print("导出数据库时发生错误")
    except Exception as e:
        print(f"发生错误: {str(e)}")

def import_database(env_vars: Dict[str, str], sql_file: str) -> None:
    """导入数据库"""
    mysql_path = Path(env_vars['MYSQL_HOME']) / 'bin' / ('mysql.exe' if sys.platform == 'win32' else 'mysql')
    
    cmd = [
        str(mysql_path),
        f"-h{env_vars['MYSQL_HOST']}",
        f"-P{env_vars['MYSQL_PORT']}",
        f"-u{env_vars['MYSQL_USERNAME']}",
        f"-p{env_vars['MYSQL_PASSWORD']}",
        env_vars['MYSQL_DATABASE']
    ]
    
    try:
        print(f"正在导入 {sql_file}...")
        with open(sql_file, 'r', encoding='utf-8') as f:
            subprocess.run(cmd, stdin=f, check=True)
        print("数据库导入成功")
    except subprocess.CalledProcessError:
        print("导入数据库时发生错误")
    except Exception as e:
        print(f"发生错误: {str(e)}")

def show_menu() -> None:
    """显示主菜单"""
    print("\n=====================================")
    print("   MySQL Database Backup Utility")
    print("=====================================")
    print("1. Export Database")
    print("2. Import Database")
    print("3. Exit")
    print()

def main():
    """主函数"""
    # 加载环境变量
    env_vars = load_env()
    
    # 检查MySQL路径
    if not check_mysql_path(env_vars['MYSQL_HOME']):
        print(f"错误: MySQL路径不正确: {env_vars['MYSQL_HOME']}")
        print("请检查 .env 文件中的 MYSQL_HOME 配置")
        sys.exit(1)
    
    while True:
        show_menu()
        choice = input("请输入选项 (1-3): ").strip()
        
        if choice == '1':
            export_database(env_vars)
        elif choice == '2':
            sql_files = list_sql_files()
            if not sql_files:
                print("当前目录下没有找到SQL文件")
                continue
                
            print("\n可用的SQL文件:")
            for i, file in enumerate(sql_files, 1):
                print(f"{i}. {file}")
            
            try:
                file_num = int(input("\n请输入要导入的文件编号: "))
                if 1 <= file_num <= len(sql_files):
                    import_database(env_vars, sql_files[file_num - 1])
                else:
                    print("无效的文件编号")
            except ValueError:
                print("请输入有效的数字")
        elif choice == '3':
            print("再见!")
            break
        else:
            print("无效的选项，请重试")
        
        input("\n按回车键继续...")

if __name__ == '__main__':
    main() 