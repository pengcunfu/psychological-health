# -*- coding: utf-8 -*-
"""
微信支付统一模块
基于配置类和支付类的架构，支持外部配置传入
"""
import hashlib
import datetime
import xml.etree.ElementTree as ET
import random
import time
import requests
from typing import Dict, Optional, Union, Tuple, Any


class WechatPayConfig:
    """微信支付配置类"""
    
    def __init__(self, 
                 appid: str, 
                 secret: str, 
                 mch_id: str, 
                 mch_key: str, 
                 notify_url: str,
                 order_url: str = 'https://api.mch.weixin.qq.com/pay/unifiedorder',
                 trade_type: str = 'JSAPI',
                 body_desc: str = '商品') -> None:
        """
        初始化微信支付配置
        :param appid: 微信小程序AppID
        :param secret: 微信小程序Secret
        :param mch_id: 商户号
        :param mch_key: 商户密钥
        :param notify_url: 支付回调地址
        :param order_url: 统一下单接口地址
        :param trade_type: 交易类型
        :param body_desc: 商品描述
        """
        self.appid: str = appid
        self.secret: str = secret
        self.mch_id: str = mch_id
        self.mch_key: str = mch_key
        self.notify_url: str = notify_url
        self.order_url: str = order_url
        self.trade_type: str = trade_type
        self.body_desc: str = body_desc


class WechatPayClient:
    """微信支付客户端类"""
    
    def __init__(self, config: WechatPayConfig) -> None:
        """
        初始化微信支付客户端
        :param config: WechatPayConfig 配置对象
        """
        self.config: WechatPayConfig = config

    def generate_nonce_str(self) -> str:
        """
        生成随机字符串
        :return: 随机字符串
        """
        data = "123456789zxcvbnmasdfghjklqwertyuiopZXCVBNMASDFGHJKLQWERTYUIOP"
        nonce_str = ''.join(random.sample(data, 30))
        return nonce_str

    def generate_order_id(self) -> str:
        """
        生成商品订单号
        :return: 订单号
        """
        date = datetime.datetime.now()
        # 根据当前系统时间来生成商品订单号。时间精确到微秒
        order_id = date.strftime("%Y%m%d%H%M%S%f")
        return order_id

    def generate_pay_sign(self, 
                         appid: str, 
                         body: str, 
                         mch_id: str, 
                         nonce_str: str, 
                         notify_url: str, 
                         openid: str, 
                         out_trade_no: str, 
                         spbill_create_ip: str, 
                         total_fee: str) -> str:
        """
        生成支付签名
        :param appid: 小程序ID
        :param body: 商品描述
        :param mch_id: 商户号
        :param nonce_str: 随机字符串
        :param notify_url: 回调地址
        :param openid: 用户openid
        :param out_trade_no: 商户订单号
        :param spbill_create_ip: 客户端IP
        :param total_fee: 总金额（分）
        :return: 签名
        """
    ret = {
        "appid": appid,
        "body": body,
        "mch_id": mch_id,
        "nonce_str": nonce_str,
        "notify_url": notify_url,
        "openid": openid,
        "out_trade_no": out_trade_no,
        "spbill_create_ip": spbill_create_ip,
        "total_fee": total_fee,
            "trade_type": self.config.trade_type
    }

    # 处理函数，对参数按照key=value的格式，并按照参数名ASCII字典序排序
    stringA = '&'.join(["{0}={1}".format(k, ret.get(k)) for k in sorted(ret)])
        stringSignTemp = '{0}&key={1}'.format(stringA, self.config.mch_key)
    sign = hashlib.md5(stringSignTemp.encode("utf-8")).hexdigest()
    return sign.upper()

    def get_pay_sign(self, prepay_id: str, time_stamp: str, nonce_str: str) -> str:
        """
        获取返回给小程序的paySign
        :param prepay_id: 预支付交易会话标识
        :param time_stamp: 时间戳
        :param nonce_str: 随机字符串
        :return: 支付签名
        """
        pay_data = {
            'appId': self.config.appid,
            'nonceStr': nonce_str,
            'package': "prepay_id=" + prepay_id,
            'signType': 'MD5',
            'timeStamp': time_stamp
        }
        stringA = '&'.join(["{0}={1}".format(k, pay_data.get(k)) for k in sorted(pay_data)])
        stringSignTemp = '{0}&key={1}'.format(stringA, self.config.mch_key)
        sign = hashlib.md5(stringSignTemp.encode("utf-8")).hexdigest()
        return sign.upper()

    def create_body_data(self, openid: str, client_ip: str, price: Union[int, float, str]) -> str:
        """
        获取全部参数信息，封装成xml
        :param openid: 用户openid
        :param client_ip: 客户端IP
        :param price: 价格（元）
        :return: XML数据
        """
        body = self.config.body_desc  # 商品描述
        notify_url = self.config.notify_url  # 支付成功的回调地址
        nonce_str = self.generate_nonce_str()  # 随机字符串
        out_trade_no = self.generate_order_id()  # 商户订单号
    total_fee = str(int(float(price) * 100))  # 订单价格转换为分

    # 获取签名
        sign = self.generate_pay_sign(
            self.config.appid, body, self.config.mch_id, nonce_str, 
            notify_url, openid, out_trade_no, client_ip, total_fee
        )

    bodyData = '<xml>'
        bodyData += '<appid>' + self.config.appid + '</appid>'  # 小程序ID
    bodyData += '<body>' + body + '</body>'  # 商品描述
        bodyData += '<mch_id>' + self.config.mch_id + '</mch_id>'  # 商户号
    bodyData += '<nonce_str>' + nonce_str + '</nonce_str>'  # 随机字符串
    bodyData += '<notify_url>' + notify_url + '</notify_url>'  # 支付成功的回调地址
    bodyData += '<openid>' + openid + '</openid>'  # 用户标识
    bodyData += '<out_trade_no>' + out_trade_no + '</out_trade_no>'  # 商户订单号
    bodyData += '<spbill_create_ip>' + client_ip + '</spbill_create_ip>'  # 客户端终端IP
    bodyData += '<total_fee>' + total_fee + '</total_fee>'  # 总金额 单位为分
        bodyData += '<trade_type>' + self.config.trade_type + '</trade_type>'  # 交易类型
    bodyData += '<sign>' + sign + '</sign>'
    bodyData += '</xml>'

    return bodyData

    def xml_to_dict(self, xml_data: Union[str, bytes]) -> Dict[str, str]:
        """
        xml转字典
        :param xml_data: XML数据
        :return: 字典
        """
    xml_dict = {}
    root = ET.fromstring(xml_data)
    for child in root:
        xml_dict[child.tag] = child.text
    return xml_dict

    def dict_to_xml(self, dict_data: Dict[str, str]) -> str:
        """
        字典转xml
        :param dict_data: 字典数据
        :return: XML字符串
        """
    xml = ["<xml>"]
        for k, v in dict_data.items():
        xml.append("<{0}>{1}</{0}>".format(k, v))
    xml.append("</xml>")
    return "".join(xml)

    def create_order(self, openid: str, price: Union[int, float, str], client_ip: str = '127.0.0.1') -> Optional[Dict[str, Any]]:
        """
        创建支付订单
        :param openid: 用户openid
        :param price: 价格（元）
        :param client_ip: 客户端IP
        :return: 支付参数或None
        """
        try:
            # 验证参数
            if not openid:
                return None
            
            # 验证金额
            try:
                price = float(price)
                if price <= 0:
                    return None
            except (ValueError, TypeError):
                return None

            # 拿到封装好的xml数据
            body_data = self.create_body_data(openid, client_ip, price)

            # 获取时间戳
            time_stamp = str(int(time.time()))

            # 请求微信接口下单
            response = requests.post(
                self.config.order_url,
                body_data.encode("utf-8"),
                headers={'Content-Type': 'application/xml'},
                timeout=30
            )

            # 回复数据为xml,将其转为字典
            content = self.xml_to_dict(response.content)

            if content.get("return_code") == 'SUCCESS' and content.get("result_code") == 'SUCCESS':
                # 获取预支付交易会话标识
                prepay_id = content.get("prepay_id")
                # 获取随机字符串
                nonce_str = content.get("nonce_str")

                # 获取paySign签名
                pay_sign = self.get_pay_sign(prepay_id, time_stamp, nonce_str)

                # 封装返回给前端的数据
                data = {
                    "prepay_id": prepay_id,
                    "nonceStr": nonce_str,
                    "paySign": pay_sign,
                    "timeStamp": time_stamp,
                    "appId": self.config.appid,
                    "package": f"prepay_id={prepay_id}",
                    "signType": "MD5"
                }

                return data
            else:
                return None

        except requests.RequestException:
            return None
        except Exception:
            return None

    def handle_notify(self, xml_data: Union[str, bytes]) -> str:
        """
        处理微信支付回调通知
        :param xml_data: 微信返回的XML数据
        :return: 处理结果
        """
        try:
            # 解析XML数据
            content = self.xml_to_dict(xml_data)

            # 验证签名
            # TODO: 实现签名验证逻辑

            if content.get("return_code") == 'SUCCESS' and content.get("result_code") == 'SUCCESS':
                # 支付成功，处理业务逻辑
                out_trade_no = content.get("out_trade_no")  # 商户订单号
                transaction_id = content.get("transaction_id")  # 微信支付订单号
                total_fee = content.get("total_fee")  # 支付金额（分）

                # 返回成功响应给微信
                return "<xml><return_code><![CDATA[SUCCESS]]></return_code><return_msg><![CDATA[OK]]></return_msg></xml>"
            else:
                # 支付失败
                return "<xml><return_code><![CDATA[FAIL]]></return_code><return_msg><![CDATA[支付失败]]></return_msg></xml>"

        except Exception:
            # 处理异常
            return "<xml><return_code><![CDATA[FAIL]]></return_code><return_msg><![CDATA[处理异常]]></return_msg></xml>"

    def verify_sign(self, params: Dict[str, str]) -> bool:
        """
        验证微信支付签名
        :param params: 参数字典
        :return: 验证结果
        """
        if 'sign' not in params:
            return False
        
        received_sign = params['sign']
        
        # 移除sign参数
        sign_params = {k: v for k, v in params.items() if k != 'sign' and v != ''}
        
        # 按key排序
        stringA = '&'.join(["{0}={1}".format(k, sign_params.get(k)) for k in sorted(sign_params)])
        stringSignTemp = '{0}&key={1}'.format(stringA, self.config.mch_key)
        calculated_sign = hashlib.md5(stringSignTemp.encode("utf-8")).hexdigest().upper()
        
        return received_sign == calculated_sign

    def create_success_response(self) -> str:
        """
        创建成功响应
        :return: 成功响应XML
        """
        return "<xml><return_code><![CDATA[SUCCESS]]></return_code><return_msg><![CDATA[OK]]></return_msg></xml>"

    def create_fail_response(self, message: str = "FAIL") -> str:
        """
        创建失败响应
        :param message: 失败消息
        :return: 失败响应XML
        """
        return f"<xml><return_code><![CDATA[FAIL]]></return_code><return_msg><![CDATA[{message}]]></return_msg></xml>"

    def format_price(self, price: Union[int, float, str]) -> int:
        """
        格式化价格（转换为分）
        :param price: 价格（元）
        :return: 价格（分）
        """
        return int(float(price) * 100)

    def parse_notify_data(self, xml_data: Union[str, bytes]) -> Optional[Dict[str, str]]:
        """
        解析回调通知数据
        :param xml_data: XML数据
        :return: 解析后的数据或None
        """
        try:
            content = self.xml_to_dict(xml_data)
            
            if content.get("return_code") == 'SUCCESS' and content.get("result_code") == 'SUCCESS':
                return {
                    "out_trade_no": content.get("out_trade_no"),
                    "transaction_id": content.get("transaction_id"),
                    "total_fee": content.get("total_fee"),
                    "openid": content.get("openid"),
                    "time_end": content.get("time_end")
                }
            else:
                return None
        except Exception:
            return None

    def get_order_status(self, out_trade_no: str) -> Optional[Dict[str, Any]]:
        """
        查询订单状态
        :param out_trade_no: 商户订单号
        :return: 订单状态信息或None
        """
        # 微信支付查询订单接口
        query_url = "https://api.mch.weixin.qq.com/pay/orderquery"
        
        nonce_str = self.generate_nonce_str()
        
        params = {
            "appid": self.config.appid,
            "mch_id": self.config.mch_id,
            "out_trade_no": out_trade_no,
            "nonce_str": nonce_str
        }
        
        # 生成签名
        stringA = '&'.join(["{0}={1}".format(k, params.get(k)) for k in sorted(params)])
        stringSignTemp = '{0}&key={1}'.format(stringA, self.config.mch_key)
        sign = hashlib.md5(stringSignTemp.encode("utf-8")).hexdigest().upper()
        params['sign'] = sign
        
        # 转换为XML
        xml_data = self.dict_to_xml(params)
        
        try:
            response = requests.post(
                query_url,
                xml_data.encode("utf-8"),
                headers={'Content-Type': 'application/xml'},
                timeout=30
            )
            
            result = self.xml_to_dict(response.content)
            
            if result.get("return_code") == 'SUCCESS' and result.get("result_code") == 'SUCCESS':
                return {
                    "trade_state": result.get("trade_state"),
                    "out_trade_no": result.get("out_trade_no"),
                    "transaction_id": result.get("transaction_id"),
                    "total_fee": result.get("total_fee"),
                    "trade_state_desc": result.get("trade_state_desc")
                }
            else:
                return None
                
        except Exception:
            return None