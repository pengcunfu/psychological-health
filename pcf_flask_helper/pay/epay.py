# -*- coding: utf-8 -*-
"""
易支付统一模块
基于配置类和支付类的架构，支持外部配置传入
"""
import hashlib
import datetime
import random
import requests
import urllib.parse
from typing import Dict, Optional, Union, Tuple, Any


class EpayConfig:
    """易支付配置类"""
    
    def __init__(self, 
                 pid: str, 
                 key: str, 
                 api_url: str, 
                 notify_url: str, 
                 return_url: str, 
                 order_prefix: str = 'EPAY', 
                 default_name: str = '商品', 
                 default_sitename: str = '网站') -> None:
        """
        初始化易支付配置
        :param pid: 易支付商户ID
        :param key: 易支付商户密钥
        :param api_url: 易支付平台域名
        :param notify_url: 异步回调地址
        :param return_url: 同步回调地址
        :param order_prefix: 订单号前缀
        :param default_name: 默认商品名称
        :param default_sitename: 默认网站名称
        """
        self.pid: str = pid
        self.key: str = key
        self.api_url: str = api_url.rstrip('/')
        self.submit_url: str = f'{self.api_url}/submit.php'
        self.api_url_path: str = f'{self.api_url}/api.php'
        self.notify_url: str = notify_url
        self.return_url: str = return_url
        self.order_prefix: str = order_prefix
        self.default_name: str = default_name
        self.default_sitename: str = default_sitename
        self.default_timeout: int = 300
        
        # 支付方式配置
        self.payment_types: Dict[str, str] = {
            'alipay': 'alipay',      # 支付宝
            'wxpay': 'wxpay',        # 微信支付
            'qqpay': 'qqpay',        # QQ钱包
            'bank': 'bank',          # 网银支付
        }


class EpayClient:
    """易支付客户端类"""
    
    def __init__(self, config: EpayConfig) -> None:
        """
        初始化易支付客户端
        :param config: EpayConfig 配置对象
        """
        self.config: EpayConfig = config

    def generate_sign(self, params: Dict[str, Any]) -> str:
        """
        生成易支付签名
        :param params: 参数字典
        :return: 签名字符串
        """
        # 过滤空值和sign参数
        filtered_params = {k: v for k, v in params.items() if v != '' and k != 'sign'}
        
        # 按key排序
        sorted_params = sorted(filtered_params.items())
        
        # 拼接字符串
        sign_str = '&'.join([f'{k}={v}' for k, v in sorted_params])
        sign_str += self.config.key
        
        # MD5加密
        return hashlib.md5(sign_str.encode('utf-8')).hexdigest()

    def verify_sign(self, params: Dict[str, Any]) -> bool:
        """
        验证易支付签名
        :param params: 参数字典
        :return: 验证结果
        """
        if 'sign' not in params:
            return False
        
        received_sign = params['sign']
        calculated_sign = self.generate_sign(params)
        
        return received_sign.lower() == calculated_sign.lower()

    def generate_trade_no(self) -> str:
        """
        生成商户订单号
        :return: 订单号
        """
        now = datetime.datetime.now()
        timestamp = now.strftime("%Y%m%d%H%M%S")
        random_num = str(random.randint(1000, 9999))
        return f"{self.config.order_prefix}{timestamp}{random_num}"

    def format_money(self, amount: Union[int, float, str]) -> str:
        """
        格式化金额（保留2位小数）
        :param amount: 金额
        :return: 格式化后的金额字符串
        """
        return f"{float(amount):.2f}"

    def create_payment_form(self, 
                           out_trade_no: str, 
                           name: str, 
                           money: Union[int, float, str], 
                           pay_type: str, 
                           notify_url: Optional[str] = None, 
                           return_url: Optional[str] = None, 
                           sitename: Optional[str] = None) -> Dict[str, str]:
        """
        创建支付表单数据
        :param out_trade_no: 商户订单号
        :param name: 商品名称
        :param money: 支付金额（元）
        :param pay_type: 支付方式
        :param notify_url: 异步回调地址
        :param return_url: 同步回调地址
        :param sitename: 网站名称
        :return: 支付表单数据
        """
        params = {
            'pid': self.config.pid,
            'type': pay_type,
            'out_trade_no': out_trade_no,
            'notify_url': notify_url or self.config.notify_url,
            'return_url': return_url or self.config.return_url,
            'name': name or self.config.default_name,
            'money': str(money),
            'sitename': sitename or self.config.default_sitename,
        }
        
        # 生成签名
        params['sign'] = self.generate_sign(params)
        params['sign_type'] = 'MD5'
        
        return params

    def create_payment_url(self, out_trade_no, name, money, pay_type, notify_url=None, return_url=None, sitename=None):
        """
        创建支付链接
        :param out_trade_no: 商户订单号
        :param name: 商品名称
        :param money: 支付金额（元）
        :param pay_type: 支付方式
        :param notify_url: 异步回调地址
        :param return_url: 同步回调地址
        :param sitename: 网站名称
        :return: 支付链接
        """
        params = self.create_payment_form(out_trade_no, name, money, pay_type, notify_url, return_url, sitename)
        
        # 构建支付URL
        query_string = urllib.parse.urlencode(params)
        payment_url = f"{self.config.submit_url}?{query_string}"
        
        return payment_url

    def create_qr_payment(self, out_trade_no, name, money, pay_type, notify_url=None, return_url=None):
        """
        创建二维码支付（适用于扫码支付）
        :param out_trade_no: 商户订单号
        :param name: 商品名称
        :param money: 支付金额（元）
        :param pay_type: 支付方式
        :param notify_url: 异步回调地址
        :param return_url: 同步回调地址
        :return: 二维码支付数据
        """
        params = {
            'pid': self.config.pid,
            'type': pay_type,
            'out_trade_no': out_trade_no,
            'notify_url': notify_url or self.config.notify_url,
            'return_url': return_url or self.config.return_url,
            'name': name,
            'money': str(money),
            'device': 'pc',  # 指定为PC端，返回二维码
        }
        
        # 生成签名
        params['sign'] = self.generate_sign(params)
        params['sign_type'] = 'MD5'
        
        try:
            response = requests.post(self.config.submit_url, data=params, timeout=30)
            response.raise_for_status()
            
            # 易支付通常返回JSON格式的二维码数据
            result = response.json()
            return result
            
        except requests.RequestException as e:
            return {'code': -1, 'msg': f'网络请求失败: {str(e)}'}
        except Exception as e:
            return {'code': -1, 'msg': f'创建二维码支付失败: {str(e)}'}

    def query_order_status(self, out_trade_no):
        """
        查询订单状态
        :param out_trade_no: 商户订单号
        :return: 查询结果
        """
        params = {
            'act': 'order',
            'pid': self.config.pid,
            'key': self.config.key,
            'out_trade_no': out_trade_no,
        }
        
        try:
            response = requests.get(self.config.api_url_path, params=params, timeout=30)
            response.raise_for_status()
            
            result = response.json()
            return result
            
        except requests.RequestException as e:
            return {'code': -1, 'msg': f'网络请求失败: {str(e)}'}
        except Exception as e:
            return {'code': -1, 'msg': f'查询失败: {str(e)}'}

    def get_balance(self):
        """
        查询商户余额
        :return: 余额查询结果
        """
        params = {
            'act': 'balance',
            'pid': self.config.pid,
            'key': self.config.key,
        }
        
        try:
            response = requests.get(self.config.api_url_path, params=params, timeout=30)
            response.raise_for_status()
            
            result = response.json()
            return result
            
        except requests.RequestException as e:
            return {'code': -1, 'msg': f'网络请求失败: {str(e)}'}
        except Exception as e:
            return {'code': -1, 'msg': f'查询失败: {str(e)}'}

    def is_valid_payment_type(self, pay_type):
        """
        验证支付方式是否有效
        :param pay_type: 支付方式
        :return: 验证结果
        """
        return pay_type in self.config.payment_types.values()

    def create_order(self, 
                    amount: Union[int, float, str], 
                    pay_type: str, 
                    product_name: Optional[str] = None, 
                    order_id: Optional[str] = None) -> Optional[Dict[str, Any]]:
        """
        创建易支付订单
        :param amount: 支付金额（元）
        :param pay_type: 支付方式 (alipay, wxpay, qqpay, bank)
        :param product_name: 商品名称
        :param order_id: 自定义订单号（可选）
        :return: 支付数据字典或None
        """
        # 验证支付方式
        if pay_type not in self.config.payment_types:
            return None

        # 验证金额
        try:
            amount = float(amount)
            if amount <= 0:
                return None
        except (ValueError, TypeError):
            return None

        # 生成订单号
        out_trade_no = order_id or self.generate_trade_no()
        
        # 格式化金额
        formatted_amount = self.format_money(amount)
        
        # 商品名称
        name = product_name or self.config.default_name
        
        # 获取支付方式代码
        epay_type = self.config.payment_types[pay_type]
        
        # 创建支付链接
        payment_url = self.create_payment_url(
            out_trade_no=out_trade_no,
            name=name,
            money=formatted_amount,
            pay_type=epay_type
        )
        
        # 创建二维码支付（适用于PC端扫码支付）
        qr_result = self.create_qr_payment(
            out_trade_no=out_trade_no,
            name=name,
            money=formatted_amount,
            pay_type=epay_type
        )
        
        # 封装返回数据
        data = {
            "out_trade_no": out_trade_no,
            "amount": formatted_amount,
            "pay_type": pay_type,
            "payment_url": payment_url,
            "product_name": name,
            "qr_code": qr_result.get('qrcode') if qr_result.get('code') == 1 else None,
            "qr_url": qr_result.get('payurl') if qr_result.get('code') == 1 else None
        }
        
        return data

    def create_mobile_order(self, amount, pay_type, product_name=None, order_id=None):
        """
        创建移动端支付订单（返回支付表单数据）
        :param amount: 支付金额（元）
        :param pay_type: 支付方式
        :param product_name: 商品名称
        :param order_id: 自定义订单号（可选）
        :return: 支付表单数据或None
        """
        # 验证支付方式
        if pay_type not in self.config.payment_types:
            return None

        # 验证金额
        try:
            amount = float(amount)
            if amount <= 0:
                return None
        except (ValueError, TypeError):
            return None

        # 生成订单号
        out_trade_no = order_id or self.generate_trade_no()
        
        # 格式化金额
        formatted_amount = self.format_money(amount)
        
        # 商品名称
        name = product_name or self.config.default_name
        
        # 获取支付方式代码
        epay_type = self.config.payment_types[pay_type]
        
        # 创建支付表单数据
        form_data = self.create_payment_form(
            out_trade_no=out_trade_no,
            name=name,
            money=formatted_amount,
            pay_type=epay_type
        )
        
        # 封装返回数据
        data = {
            "out_trade_no": out_trade_no,
            "amount": formatted_amount,
            "pay_type": pay_type,
            "form_data": form_data,
            "submit_url": self.config.submit_url,
            "product_name": name
        }
        
        return data

    def query_order(self, out_trade_no):
        """
        查询易支付订单状态
        :param out_trade_no: 商户订单号
        :return: 订单状态信息或None
        """
        result = self.query_order_status(out_trade_no)
        
        if result.get('code') == 1:
            # 查询成功
            order_info = {
                "out_trade_no": out_trade_no,
                "trade_no": result.get('trade_no'),  # 易支付订单号
                "money": result.get('money'),
                "name": result.get('name'),
                "status": result.get('status'),  # 订单状态
                "addtime": result.get('addtime'),  # 创建时间
                "endtime": result.get('endtime'),  # 完成时间
            }
            
            # 转换状态描述
            status_map = {
                '0': 'pending',    # 未支付
                '1': 'success',    # 支付成功
                '2': 'failed',     # 支付失败
            }
            order_info['status_desc'] = status_map.get(str(result.get('status')), 'unknown')
            
            return order_info
        else:
            return None

    def get_merchant_balance(self):
        """
        查询易支付商户余额
        :return: 余额信息或None
        """
        result = self.get_balance()
        
        if result.get('code') == 1:
            balance_info = {
                "balance": result.get('money', '0.00'),
                "frozen": result.get('frozen', '0.00'),
                "total": result.get('total', '0.00'),
            }
            return balance_info
        else:
            return None

    def get_payment_types(self):
        """
        获取支持的支付方式列表
        :return: 支付方式列表
        """
        payment_types = []
        for key, value in self.config.payment_types.items():
            payment_types.append({
                "code": key,
                "name": self.get_payment_type_name(key),
                "epay_code": value
            })
        
        return payment_types

    def get_payment_type_name(self, pay_type):
        """
        获取支付方式中文名称
        :param pay_type: 支付方式代码
        :return: 中文名称
        """
        names = {
            'alipay': '支付宝',
            'wxpay': '微信支付',
            'qqpay': 'QQ钱包',
            'bank': '网银支付'
        }
        return names.get(pay_type, pay_type)

    def handle_notify(self, params: Dict[str, Any]) -> str:
        """
        处理易支付异步回调通知
        :param params: 回调参数字典
        :return: 处理结果
        """
        # 验证必要参数
        required_params = ['pid', 'trade_no', 'out_trade_no', 'type', 'name', 'money', 'trade_status', 'sign']
        for param in required_params:
            if param not in params:
                raise ValueError(f"缺少必要参数: {param}")
        
        # 验证签名
        if not self.verify_sign(params):
            raise ValueError("签名验证失败")
        
        # 获取订单信息
        out_trade_no = params.get('out_trade_no')
        trade_no = params.get('trade_no')
        trade_status = params.get('trade_status')
        money = params.get('money')
        pay_type = params.get('type')
        product_name = params.get('name')
        
        # 验证通过，返回成功
        return "success"

    def handle_return(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        处理易支付同步回调通知（用户支付完成后跳转）
        :param params: 回调参数字典
        :return: 处理结果
        """
        # 验证必要参数
        required_params = ['pid', 'trade_no', 'out_trade_no', 'type', 'name', 'money', 'trade_status', 'sign']
        for param in required_params:
            if param not in params:
                raise ValueError(f"缺少必要参数: {param}")
        
        # 验证签名
        if not self.verify_sign(params):
            raise ValueError("签名验证失败")
        
        # 获取订单信息
        out_trade_no = params.get('out_trade_no')
        trade_no = params.get('trade_no')
        trade_status = params.get('trade_status')
        money = params.get('money')
        
        # 构建返回数据
        data = {
            "out_trade_no": out_trade_no,
            "trade_no": trade_no,
            "trade_status": trade_status,
            "money": money,
            "status_desc": self.get_trade_status_desc(trade_status)
        }
        
        return data

    def get_trade_status_desc(self, trade_status):
        """
        获取交易状态描述
        :param trade_status: 交易状态
        :return: 状态描述
        """
        status_map = {
            'TRADE_SUCCESS': '支付成功',
            'TRADE_FINISHED': '交易完成',
            'WAIT_BUYER_PAY': '等待买家付款',
            'TRADE_CLOSED': '交易关闭',
        }
        return status_map.get(trade_status, '未知状态')

    def verify_notify_params(self, params: Dict[str, Any]) -> Tuple[bool, str]:
        """
        验证回调参数的完整性和有效性
        :param params: 回调参数
        :return: 验证结果和错误信息
        """
        # 验证必要参数
        required_params = ['pid', 'trade_no', 'out_trade_no', 'type', 'name', 'money', 'trade_status', 'sign']
        
        for param in required_params:
            if param not in params or not params[param]:
                return False, f"缺少必要参数: {param}"
        
        # 验证金额格式
        try:
            money = float(params.get('money', 0))
            if money <= 0:
                return False, "支付金额无效"
        except (ValueError, TypeError):
            return False, "支付金额格式错误"
        
        # 验证订单号格式
        out_trade_no = params.get('out_trade_no', '')
        if not out_trade_no or len(out_trade_no) < 10:
            return False, "商户订单号格式错误"
        
        return True, "验证通过"

    def create_notify_response(self, success: bool = True, message: str = "") -> str:
        """
        创建回调响应
        :param success: 是否成功
        :param message: 响应消息
        :return: 响应内容
        """
        if success:
            return "success"
        else:
            return "fail"