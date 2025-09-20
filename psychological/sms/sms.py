# -*- coding: utf-8 -*-
"""
阿里云短信服务模块
"""
import json
import random
import string
from typing import Dict, Optional
from datetime import datetime, timedelta

from alibabacloud_dysmsapi20170525.client import Client as Dysmsapi20170525Client
from alibabacloud_tea_openapi import models as open_api_models
from alibabacloud_dysmsapi20170525 import models as dysmsapi_20170525_models
from alibabacloud_tea_util import models as util_models

from .config import (
    ALIYUN_ACCESS_KEY_ID, 
    ALIYUN_ACCESS_KEY_SECRET, 
    SMS_ENDPOINT, 
    SMS_SIGN_NAME, 
    SMS_TEMPLATES,
    VERIFICATION_CODE
)
from ..utils.logger_client import get_logger
from ..utils.json_result import success_result, error_result

logger = get_logger(__name__)


class SmsService:
    """阿里云短信服务类"""
    
    def __init__(self):
        self.client = self._create_client()

    def _create_client(self) -> Dysmsapi20170525Client:
        """
        创建阿里云短信客户端
        @return: Client
        """
        try:
            config = open_api_models.Config(
                access_key_id=ALIYUN_ACCESS_KEY_ID,
                access_key_secret=ALIYUN_ACCESS_KEY_SECRET
            )
            config.endpoint = SMS_ENDPOINT
            return Dysmsapi20170525Client(config)
        except Exception as e:
            logger.error(f"创建阿里云短信客户端失败: {e}")
            raise
    
    def send_sms(self, phone_number: str, template_code: str, template_param: Dict = None, sign_name: str = None) -> Dict:
        """
        发送短信
        
        :param phone_number: 手机号码
        :param template_code: 短信模板CODE
        :param template_param: 短信模板变量对应的参数
        :param sign_name: 短信签名名称，默认使用配置中的签名
        :return: 发送结果
        """
        try:
            # 参数验证
            if not phone_number:
                return error_result("手机号码不能为空")
            
            if not template_code:
                return error_result("短信模板不能为空")
            
            # 使用默认签名
            if not sign_name:
                sign_name = SMS_SIGN_NAME
            
            # 构建请求
            request = dysmsapi_20170525_models.SendSmsRequest(
                phone_numbers=phone_number,
                sign_name=sign_name,
                template_code=template_code,
                template_param=json.dumps(template_param) if template_param else None
            )
            
            # 发送短信
            response = self.client.send_sms_with_options(request, util_models.RuntimeOptions())
            
            # 处理响应
            if response.body.code == 'OK':
                logger.info(f"短信发送成功: {phone_number}, 模板: {template_code}")
                return success_result("短信发送成功", {
                    'biz_id': response.body.biz_id,
                    'request_id': response.body.request_id,
                    'phone_number': phone_number,
                    'template_code': template_code
                })
            else:
                error_msg = f"短信发送失败: {response.body.message}"
                logger.error(f"{error_msg}, 错误码: {response.body.code}")
                return error_result(error_msg)
                
        except Exception as e:
            error_msg = f"短信发送异常: {str(e)}"
            logger.error(error_msg)
            return error_result(error_msg)
    
    def generate_verification_code(self, length: int = None) -> str:
        """
        生成验证码
        
        :param length: 验证码长度
        :return: 验证码
        """
        if not length:
            length = VERIFICATION_CODE['length']
        
        chars = VERIFICATION_CODE['chars']
        return ''.join(random.choice(chars) for _ in range(length))
    
    def send_verification_code(self, phone_number: str, code: str = None) -> Dict:
        """
        发送验证码短信
        
        :param phone_number: 手机号码
        :param code: 验证码，如果为空则自动生成
        :return: 发送结果
        """
        if not code:
            code = self.generate_verification_code()
        
        template_param = {'code': code}
        
        result = self.send_sms(
            phone_number=phone_number,
            template_code=SMS_TEMPLATES.get('verification_code'),
            template_param=template_param
        )
        
        if result['code'] == 200:
            result['data']['verification_code'] = code
        
        return result
    
    def send_appointment_reminder(self, phone_number: str, appointment_time: str, doctor_name: str) -> Dict:
        """
        发送预约提醒短信
        
        :param phone_number: 手机号码
        :param appointment_time: 预约时间
        :param doctor_name: 医生姓名
        :return: 发送结果
        """
        template_param = {
            'appointment_time': appointment_time,
            'doctor_name': doctor_name
        }
        
        return self.send_sms(
            phone_number=phone_number,
            template_code=SMS_TEMPLATES.get('appointment_reminder'),
            template_param=template_param
        )
    
    def send_login_notification(self, phone_number: str, login_time: str, login_location: str = None) -> Dict:
        """
        发送登录通知短信
        
        :param phone_number: 手机号码
        :param login_time: 登录时间
        :param login_location: 登录地点
        :return: 发送结果
        """
        template_param = {
            'login_time': login_time,
            'login_location': login_location or '未知'
        }
        
        return self.send_sms(
            phone_number=phone_number,
            template_code=SMS_TEMPLATES.get('login_notification'),
            template_param=template_param
        )
    
    def send_password_reset(self, phone_number: str, reset_code: str = None) -> Dict:
        """
        发送密码重置短信
        
        :param phone_number: 手机号码
        :param reset_code: 重置码，如果为空则自动生成
        :return: 发送结果
        """
        if not reset_code:
            reset_code = self.generate_verification_code()
        
        template_param = {'reset_code': reset_code}
        
        result = self.send_sms(
            phone_number=phone_number,
            template_code=SMS_TEMPLATES.get('password_reset'),
            template_param=template_param
        )
        
        if result['code'] == 200:
            result['data']['reset_code'] = reset_code
        
        return result
    
    def send_order_notification(self, phone_number: str, order_number: str, order_status: str) -> Dict:
        """
        发送订单通知短信
        
        :param phone_number: 手机号码
        :param order_number: 订单号
        :param order_status: 订单状态
        :return: 发送结果
        """
        template_param = {
            'order_number': order_number,
            'order_status': order_status
        }
        
        return self.send_sms(
            phone_number=phone_number,
            template_code=SMS_TEMPLATES.get('order_notification'),
            template_param=template_param
        )


# 创建全局短信服务实例
sms_service = SmsService()


# 便捷函数
def send_sms(phone_number: str, template_code: str, template_param: Dict = None, sign_name: str = None) -> Dict:
    """
    发送短信的便捷函数
    
    :param phone_number: 手机号码
    :param template_code: 短信模板CODE
    :param template_param: 短信模板变量对应的参数
    :param sign_name: 短信签名名称
    :return: 发送结果
    """
    return sms_service.send_sms(phone_number, template_code, template_param, sign_name)


def send_verification_code(phone_number: str, code: str = None) -> Dict:
    """
    发送验证码短信的便捷函数
    
    :param phone_number: 手机号码
    :param code: 验证码
    :return: 发送结果
    """
    return sms_service.send_verification_code(phone_number, code)


def send_appointment_reminder(phone_number: str, appointment_time: str, doctor_name: str) -> Dict:
    """
    发送预约提醒短信的便捷函数
    """
    return sms_service.send_appointment_reminder(phone_number, appointment_time, doctor_name)


def send_login_notification(phone_number: str, login_time: str, login_location: str = None) -> Dict:
    """
    发送登录通知短信的便捷函数
    """
    return sms_service.send_login_notification(phone_number, login_time, login_location)


def send_password_reset(phone_number: str, reset_code: str = None) -> Dict:
    """
    发送密码重置短信的便捷函数
    """
    return sms_service.send_password_reset(phone_number, reset_code)


def send_order_notification(phone_number: str, order_number: str, order_status: str) -> Dict:
    """
    发送订单通知短信的便捷函数
    """
    return sms_service.send_order_notification(phone_number, order_number, order_status)


def generate_verification_code(length: int = None) -> str:
    """
    生成验证码的便捷函数
    
    :param length: 验证码长度
    :return: 验证码
    """
    return sms_service.generate_verification_code(length)