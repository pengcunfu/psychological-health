"""
微信支付订单处理模块
"""
import time
import requests
from flask import request, jsonify
from . import pay
from .config import WECHAT_ORDER_URL
from ..models.user import User
from ..utils.json_result import JsonResult


def create_pay_order(user_id, price, client_ip=None):
    """
    创建支付订单
    :param user_id: 用户ID
    :param price: 价格（元）
    :param client_ip: 客户端IP
    :return: 支付参数或错误信息
    """
    try:
        # 获取用户信息
        user = User.query.get(user_id)
        if not user:
            return JsonResult.error("用户不存在")

        # 获取用户openid（需要在用户表中添加openid字段）
        openid = getattr(user, 'openid', None)
        if not openid:
            return JsonResult.error("用户未绑定微信")

        # 获取客户端IP
        if not client_ip:
            client_ip = request.remote_addr or '127.0.0.1'

        # 拿到封装好的xml数据
        body_data = pay.get_bodyData(openid, client_ip, price)

        # 获取时间戳
        timeStamp = str(int(time.time()))

        # 请求微信接口下单
        response = requests.post(
            WECHAT_ORDER_URL,
            body_data.encode("utf-8"),
            headers={'Content-Type': 'application/xml'},
            timeout=30
        )

        # 回复数据为xml,将其转为字典
        content = pay.xml_to_dict(response.content)

        if content.get("return_code") == 'SUCCESS' and content.get("result_code") == 'SUCCESS':
            # 获取预支付交易会话标识
            prepay_id = content.get("prepay_id")
            # 获取随机字符串
            nonceStr = content.get("nonce_str")

            # 获取paySign签名
            paySign = pay.get_paysign(prepay_id, timeStamp, nonceStr)

            # 封装返回给前端的数据
            data = {
                "prepay_id": prepay_id,
                "nonceStr": nonceStr,
                "paySign": paySign,
                "timeStamp": timeStamp,
                "appId": pay.WECHAT_APPID,
                "package": f"prepay_id={prepay_id}",
                "signType": "MD5"
            }

            return JsonResult.success("创建支付订单成功", data)

        else:
            error_msg = content.get("return_msg") or content.get("err_code_des") or "请求支付失败"
            return JsonResult.error(f"微信支付失败: {error_msg}")

    except requests.RequestException as e:
        return JsonResult.error(f"网络请求失败: {str(e)}")
    except Exception as e:
        return JsonResult.error(f"创建支付订单失败: {str(e)}")


def handle_pay_notify(xml_data):
    """
    处理微信支付回调通知
    :param xml_data: 微信返回的XML数据
    :return: 处理结果
    """
    try:
        # 解析XML数据
        content = pay.xml_to_dict(xml_data)

        # 验证签名
        # TODO: 实现签名验证逻辑

        if content.get("return_code") == 'SUCCESS' and content.get("result_code") == 'SUCCESS':
            # 支付成功，处理业务逻辑
            out_trade_no = content.get("out_trade_no")  # 商户订单号
            transaction_id = content.get("transaction_id")  # 微信支付订单号
            total_fee = content.get("total_fee")  # 支付金额（分）

            # TODO: 更新订单状态，记录支付信息

            # 返回成功响应给微信
            return "<xml><return_code><![CDATA[SUCCESS]]></return_code><return_msg><![CDATA[OK]]></return_msg></xml>"
        else:
            # 支付失败
            return "<xml><return_code><![CDATA[FAIL]]></return_code><return_msg><![CDATA[支付失败]]></return_msg></xml>"

    except Exception as e:
        # 处理异常
        return "<xml><return_code><![CDATA[FAIL]]></return_code><return_msg><![CDATA[处理异常]]></return_msg></xml>"
