# -*- coding: utf-8 -*-
"""
短信服务工具
提供短信服务初始化和验证码发送便捷函数
"""
from typing import Optional
from pcf_flask_helper.sms.yunpian_sms import YunpianSMSService
from psychological.config import cfg


class SMSService:
    """短信服务类 - 管理云片网短信服务"""
    
    _sms_service: Optional[YunpianSMSService] = None
    
    @classmethod
    def get_sms_service(cls) -> YunpianSMSService:
        """获取短信服务实例"""
        if cls._sms_service is None:
            api_key = cfg.get("sms.yunpian.api_key")
            if not api_key:
                raise ValueError("未配置云片网API Key，请在配置文件中设置 sms.yunpian.api_key")
            
            cls._sms_service = YunpianSMSService(api_key=api_key)
        return cls._sms_service
    
    @classmethod
    def reset_service(cls):
        """重置服务实例（用于测试或重新初始化）"""
        cls._sms_service = None


def get_sms_service() -> YunpianSMSService:
    """获取短信服务实例"""
    return SMSService.get_sms_service()


def send_verification_code(phone_number: str, verification_code: str) -> bool:
    """
    发送验证码短信
    
    Args:
        phone_number: 手机号码
        verification_code: 验证码
        
    Returns:
        bool: 发送成功返回True，失败抛出异常
        
    Raises:
        ValueError: 参数错误
        Exception: 发送失败
    """
    if not phone_number:
        raise ValueError("手机号码不能为空")
    if not verification_code:
        raise ValueError("验证码不能为空")
    
    sms_service = get_sms_service()
    return sms_service.send_sms(
        phone_number=phone_number,
        verification_code=verification_code
    )


def send_custom_sms(phone_number: str, content: str, sign_name: str = None) -> bool:
    """
    发送自定义短信
    
    Args:
        phone_number: 手机号码
        content: 短信内容
        sign_name: 短信签名，如果不提供则使用默认签名
        
    Returns:
        bool: 发送成功返回True，失败抛出异常
        
    Raises:
        ValueError: 参数错误
        Exception: 发送失败
    """
    if not phone_number:
        raise ValueError("手机号码不能为空")
    if not content:
        raise ValueError("短信内容不能为空")
    
    # 如果没有提供签名，使用配置中的默认签名
    if not sign_name:
        sign_name = cfg.get("sms.default_sign", "心理健康平台")
    
    # 构建完整的短信内容（包含签名）
    full_content = f"【{sign_name}】{content}"
    
    sms_service = get_sms_service()
    return sms_service.send_sms(
        phone_number=phone_number,
        text=full_content
    )


def send_appointment_reminder(phone_number: str, patient_name: str, 
                            appointment_time: str, doctor_name: str) -> bool:
    """
    发送预约提醒短信
    
    Args:
        phone_number: 手机号码
        patient_name: 患者姓名
        appointment_time: 预约时间
        doctor_name: 医生姓名
        
    Returns:
        bool: 发送成功返回True，失败抛出异常
    """
    content = f"亲爱的{patient_name}，您预约的{doctor_name}医生咨询时间为{appointment_time}，请准时参加。如需调整请提前联系我们。"
    return send_custom_sms(phone_number, content)


def send_order_notification(phone_number: str, order_number: str, 
                          order_status: str, amount: str = None) -> bool:
    """
    发送订单通知短信
    
    Args:
        phone_number: 手机号码
        order_number: 订单号
        order_status: 订单状态
        amount: 订单金额（可选）
        
    Returns:
        bool: 发送成功返回True，失败抛出异常
    """
    if amount:
        content = f"您的订单{order_number}状态已更新为：{order_status}，金额：{amount}元。感谢您的信任！"
    else:
        content = f"您的订单{order_number}状态已更新为：{order_status}。感谢您的信任！"
    
    return send_custom_sms(phone_number, content)


def get_account_balance() -> dict:
    """
    获取短信账户余额信息
    
    Returns:
        dict: 账户信息
        
    Raises:
        Exception: 获取失败
    """
    sms_service = get_sms_service()
    return sms_service.get_account_info()


def send_batch_sms(phone_numbers: list, content: str, sign_name: str = None) -> bool:
    """
    批量发送短信
    
    Args:
        phone_numbers: 手机号码列表
        content: 短信内容
        sign_name: 短信签名，如果不提供则使用默认签名
        
    Returns:
        bool: 发送成功返回True，失败抛出异常
    """
    if not phone_numbers:
        raise ValueError("手机号码列表不能为空")
    if not content:
        raise ValueError("短信内容不能为空")
    
    # 如果没有提供签名，使用配置中的默认签名
    if not sign_name:
        sign_name = cfg.get("sms.default_sign", "心理健康平台")
    
    # 构建完整的短信内容（包含签名）
    full_content = f"【{sign_name}】{content}"
    
    sms_service = get_sms_service()
    return sms_service.send_batch_sms(phone_numbers, full_content)
