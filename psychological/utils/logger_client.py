import logging
import sys
from typing import Optional


class LoggerClient:
    """日志客户端，统一管理应用日志配置"""

    _initialized = False

    @classmethod
    def init_logging(cls, level: str = 'INFO', format_string: Optional[str] = None):
        """初始化日志配置

        Args:
            level: 日志级别 ('DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL')
            format_string: 自定义日志格式
        """
        if cls._initialized:
            return

        if format_string is None:
            format_string = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'

        # 配置根日志器
        logging.basicConfig(
            level=getattr(logging, level.upper()),
            format=format_string,
            handlers=[
                logging.StreamHandler(sys.stdout)
            ]
        )

        cls._initialized = True

    @classmethod
    def get_logger(cls, name: str = None) -> logging.Logger:
        """获取logger实例

        Args:
            name: logger名称，如果为None则使用调用模块的名称

        Returns:
            logging.Logger: logger实例
        """
        if not cls._initialized:
            cls.init_logging()

        if name is None:
            # 获取调用者的模块名
            import inspect
            frame = inspect.currentframe().f_back
            name = frame.f_globals.get('__name__', 'unknown')

        return logging.getLogger(name)


# 便捷函数
def init_logging(level: str = 'INFO', format_string: Optional[str] = None):
    """初始化日志配置的便捷函数"""
    LoggerClient.init_logging(level, format_string)


def get_logger(name: str = None) -> logging.Logger:
    """获取logger实例的便捷函数"""
    return LoggerClient.get_logger(name)


# 默认logger实例（向后兼容）
logger = LoggerClient.get_logger('app')
