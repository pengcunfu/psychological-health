# -*- coding: utf-8 -*-
"""
云片网短信服务模块 - 使用HTTP API
"""
import json
from typing import Dict, Optional

# 按需导入requests
try:
    import requests
except ImportError as e:
    raise ImportError(
        "云片网短信服务需要安装requests依赖。请运行以下命令安装：\n"
        "pip install requests>=2.25.0"
    ) from e


class YunpianSMSService:
    """云片网短信服务类"""
    
    def __init__(self, api_key: str):
        """
        初始化短信服务
        
        Args:
            api_key: 云片网API Key
        """
        # 参数验证
        if not api_key:
            raise ValueError("API Key不能为空")
        
        self.api_key = api_key
        self.base_url = "https://sms.yunpian.com/v2/sms"
        self.session = requests.Session()
        self.session.headers.update({
            'Content-Type': 'application/x-www-form-urlencoded;charset=utf-8'
        })
    
    def send_sms(self, phone_number: str, text: str = None, 
                 template_param: Optional[Dict] = None,
                 verification_code: Optional[str] = None) -> bool:
        """
        发送短信
        
        Args:
            phone_number: 手机号码
            text: 短信内容（完整的短信内容，包含签名）
            template_param: 模板参数字典（暂不支持，云片网使用完整文本）
            verification_code: 验证码（如果提供，会自动构建短信内容）
            
        Returns:
            bool: 发送成功返回True，失败抛出异常
            
        Raises:
            ValueError: 参数错误
            Exception: 发送失败或其他异常
        """
        # 参数验证
        if not phone_number:
            raise ValueError("手机号码不能为空")
        
        # 处理短信内容
        final_text = text
        if verification_code:
            # 如果提供验证码，构建验证码短信内容
            final_text = f"【云片网】您的验证码是{verification_code}。如非本人操作，请忽略本短信"
        
        if not final_text:
            raise ValueError("短信内容不能为空")
        
        try:
            # 构建请求数据
            data = {
                'apikey': self.api_key,
                'mobile': phone_number,
                'text': final_text
            }
            
            # 发送请求
            response = self.session.post(
                f"{self.base_url}/single_send.json",
                data=data,
                timeout=30
            )
            
            if response.status_code != 200:
                raise Exception(f"HTTP请求失败，状态码: {response.status_code}")
            
            response_data = response.json()
            
            # 处理响应
            if response_data.get('code') == 0:
                return True
            else:
                error_msg = response_data.get('msg', '未知错误')
                error_detail = response_data.get('detail', '')
                full_error = f"{error_msg}({error_detail})" if error_detail else error_msg
                raise Exception(f"短信发送失败: {full_error}")
                
        except requests.exceptions.Timeout:
            raise Exception("请求超时")
        except requests.exceptions.ConnectionError:
            raise Exception("网络连接错误")
        except requests.exceptions.RequestException as e:
            raise Exception(f"请求异常: {str(e)}")
        except json.JSONDecodeError:
            raise Exception("响应数据格式错误")
        except Exception as e:
            if isinstance(e, ValueError):
                raise
            raise Exception(f"发送短信异常: {str(e)}")
    
    def get_account_info(self) -> Dict:
        """
        获取账户信息
        
        Returns:
            Dict: 账户信息字典
            
        Raises:
            Exception: 获取失败时抛出异常
        """
        try:
            data = {'apikey': self.api_key}
            
            response = self.session.post(
                "https://sms.yunpian.com/v2/user/get.json",
                data=data,
                timeout=30
            )
            
            if response.status_code != 200:
                raise Exception(f"HTTP请求失败，状态码: {response.status_code}")
            
            response_data = response.json()
            
            if response_data.get('code') == 0:
                user_info = response_data.get('user', {})
                return {
                    'nick': user_info.get('nick'),
                    'balance': user_info.get('balance'),
                    'alarm_balance': user_info.get('alarm_balance'),
                    'emergency_contact': user_info.get('emergency_contact'),
                    'emergency_mobile': user_info.get('emergency_mobile')
                }
            else:
                error_msg = response_data.get('msg', '未知错误')
                raise Exception(f"获取账户信息失败: {error_msg}")
                
        except requests.exceptions.Timeout:
            raise Exception("请求超时")
        except requests.exceptions.ConnectionError:
            raise Exception("网络连接错误")
        except requests.exceptions.RequestException as e:
            raise Exception(f"请求异常: {str(e)}")
        except json.JSONDecodeError:
            raise Exception("响应数据格式错误")
        except Exception as e:
            raise Exception(f"获取账户信息异常: {str(e)}")
    
    def send_batch_sms(self, phone_numbers: list, text: str) -> bool:
        """
        批量发送短信
        
        Args:
            phone_numbers: 手机号码列表
            text: 短信内容
            
        Returns:
            bool: 发送成功返回True，失败抛出异常
            
        Raises:
            ValueError: 参数错误
            Exception: 发送失败或其他异常
        """
        if not phone_numbers:
            raise ValueError("手机号码列表不能为空")
        
        if not text:
            raise ValueError("短信内容不能为空")
        
        try:
            # 云片网批量发送支持逗号分隔的手机号
            mobile_str = ','.join(phone_numbers)
            
            data = {
                'apikey': self.api_key,
                'mobile': mobile_str,
                'text': text
            }
            
            response = self.session.post(
                f"{self.base_url}/batch_send.json",
                data=data,
                timeout=60
            )
            
            if response.status_code != 200:
                raise Exception(f"HTTP请求失败，状态码: {response.status_code}")
            
            response_data = response.json()
            
            if response_data.get('code') == 0:
                return True
            else:
                error_msg = response_data.get('msg', '未知错误')
                raise Exception(f"批量短信发送失败: {error_msg}")
                
        except requests.exceptions.Timeout:
            raise Exception("请求超时")
        except requests.exceptions.ConnectionError:
            raise Exception("网络连接错误")
        except requests.exceptions.RequestException as e:
            raise Exception(f"请求异常: {str(e)}")
        except json.JSONDecodeError:
            raise Exception("响应数据格式错误")
        except Exception as e:
            if isinstance(e, ValueError):
                raise
            raise Exception(f"批量发送短信异常: {str(e)}")
