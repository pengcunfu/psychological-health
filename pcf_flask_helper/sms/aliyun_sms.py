# -*- coding: utf-8 -*-
"""
阿里云短信服务模块 - 使用官方SDK简化版本
"""
import json
from typing import Dict, Optional

# 按需导入阿里云SDK
try:
    from aliyunsdkcore.client import AcsClient
    from aliyunsdkcore.request import CommonRequest
    from aliyunsdkcore.acs_exception.exceptions import ClientException, ServerException
except ImportError as e:
    raise ImportError(
        "阿里云短信服务需要安装阿里云SDK依赖。请运行以下命令安装：\n"
        "pip install aliyun-python-sdk-core>=2.13.0 aliyun-python-sdk-dysmsapi>=2.0.0"
    ) from e


class AliyunSMSService:
    """阿里云短信服务类"""
    
    def __init__(self, access_key_id: str, access_key_secret: str, region: str):
        """
        初始化短信服务
        
        Args:
            access_key_id: 阿里云AccessKey ID
            access_key_secret: 阿里云AccessKey Secret
            region: 阿里云区域
        """
        # 参数验证
        if not access_key_id:
            raise ValueError("AccessKey ID不能为空")
        if not access_key_secret:
            raise ValueError("AccessKey Secret不能为空")
        if not region:
            raise ValueError("区域不能为空")
        
        self.access_key_id = access_key_id
        self.access_key_secret = access_key_secret
        self.region = region
        
        self.client = AcsClient(
            access_key_id,
            access_key_secret,
            region
        )
    
    def send_sms(self, phone_number: str, template_code: str, 
                 sign_name: str, template_param: Optional[Dict] = None,
                 verification_code: Optional[str] = None) -> bool:
        """
        发送短信
        
        Args:
            phone_number: 手机号码
            template_code: 短信模板代码
            sign_name: 短信签名
            template_param: 模板参数字典
            verification_code: 验证码（如果提供，会自动构建为 {'code': verification_code}）
            
        Returns:
            bool: 发送成功返回True，失败抛出异常
            
        Raises:
            ValueError: 参数错误
            Exception: 发送失败或其他异常
        """
        # 参数验证
        if not phone_number:
            raise ValueError("手机号码不能为空")
        
        if not template_code:
            raise ValueError("短信模板代码不能为空")
        
        if not sign_name:
            raise ValueError("短信签名不能为空")
        
        # 处理模板参数
        final_template_param = template_param
        if verification_code:
            final_template_param = {'code': verification_code}
        
        try:
            # 构建请求
            request = CommonRequest()
            request.set_accept_format('json')
            request.set_domain('dysmsapi.aliyuncs.com')
            request.set_method('POST')
            request.set_version('2017-05-25')
            request.set_action_name('SendSms')
            
            request.add_query_param('PhoneNumbers', phone_number)
            request.add_query_param('SignName', sign_name)
            request.add_query_param('TemplateCode', template_code)
            
            if final_template_param:
                request.add_query_param('TemplateParam', json.dumps(final_template_param))
            
            # 发送请求
            response = self.client.do_action_with_exception(request)
            response_data = json.loads(response.decode('utf-8'))
            
            # 处理响应
            if response_data.get('Code') == 'OK':
                return True
            else:
                error_msg = response_data.get('Message', '未知错误')
                raise Exception(f"短信发送失败: {error_msg}")
                
        except ClientException as e:
            raise Exception(f"客户端错误: {e.get_error_msg()}")
        except ServerException as e:
            raise Exception(f"服务端错误: {e.get_error_msg()}")
        except Exception as e:
            if isinstance(e, ValueError):
                raise
            raise Exception(f"发送短信异常: {str(e)}")
