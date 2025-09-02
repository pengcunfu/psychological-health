#!/bin/bash

# 心理健康平台 - 数据目录设置脚本

set -e

# 颜色定义
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${GREEN}🔧 设置心理健康平台数据目录${NC}"
echo

# 检查操作系统
OS="$(uname -s)"
case "${OS}" in
    Linux*)     MACHINE=Linux;;
    Darwin*)    MACHINE=Mac;;
    CYGWIN*)    MACHINE=Cygwin;;
    MINGW*)     MACHINE=MinGw;;
    *)          MACHINE="UNKNOWN:${OS}"
esac

echo -e "${YELLOW}检测到操作系统: ${MACHINE}${NC}"

# 数据目录路径
DATA_DIR="$HOME/data/psychological-health"

echo -e "${YELLOW}数据目录: ${DATA_DIR}${NC}"

# 创建目录结构
echo "创建目录结构..."
mkdir -p "${DATA_DIR}/uploads"
mkdir -p "${DATA_DIR}/static"
mkdir -p "${DATA_DIR}/instance"
mkdir -p "${DATA_DIR}/web-logs"
mkdir -p "${DATA_DIR}/mysql"
mkdir -p "${DATA_DIR}/redis"

echo -e "${GREEN}✓ 目录创建完成${NC}"

# 设置权限（仅Linux和Mac）
if [[ "$MACHINE" == "Linux" || "$MACHINE" == "Mac" ]]; then
    echo "设置目录权限..."
    chmod -R 755 "${DATA_DIR}"
    
    # 特殊处理MySQL目录权限
    # MySQL容器通常以mysql用户运行（UID 999）
    if command -v docker &> /dev/null; then
        echo "调整MySQL目录权限..."
        # 给MySQL目录设置更宽松的权限，让容器可以写入
        chmod 777 "${DATA_DIR}/mysql"
        chmod 777 "${DATA_DIR}/redis"
    fi
    
    echo -e "${GREEN}✓ 权限设置完成${NC}"
fi

# 显示目录结构
echo
echo "创建的目录结构:"
if command -v tree &> /dev/null; then
    tree "${DATA_DIR}"
else
    ls -la "${DATA_DIR}"
fi

echo
echo -e "${GREEN}🎉 数据目录设置完成！${NC}"
echo
echo "现在可以运行以下命令启动服务:"
echo -e "${YELLOW}docker-compose up -d${NC}"
echo
echo "数据将持久化到以下位置:"
echo "  - 上传文件: ${DATA_DIR}/uploads"
echo "  - 静态文件: ${DATA_DIR}/static"
echo "  - 数据库文件: ${DATA_DIR}/mysql"
echo "  - Redis数据: ${DATA_DIR}/redis"
echo "  - Web日志: ${DATA_DIR}/web-logs"
echo "  - 实例数据: ${DATA_DIR}/instance" 