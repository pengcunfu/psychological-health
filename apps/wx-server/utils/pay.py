import uuid


class PaymentResult:
    def __init__(self, success: bool, message: str = '', data: dict = None):
        self.success = success
        self.message = message
        self.data = data or {}


class PayUtil:
    """
    支付工具类，支持聚合支付和微信支付接口定义。
    这里只做接口结构，具体实现需对接第三方支付SDK。
    """

    def unified_order(self, amount: float, subject: str, out_trade_no: str = None, pay_type: str = 'wechat',
                      **kwargs) -> PaymentResult:
        """
        创建统一下单接口（聚合支付/微信支付）。
        :param amount: 支付金额
        :param subject: 商品描述
        :param out_trade_no: 商户订单号
        :param pay_type: 支付类型（wechat/alipay/other）
        :param kwargs: 其它支付参数
        :return: PaymentResult
        """
        out_trade_no = out_trade_no or str(uuid.uuid4())
        # 这里只做接口结构，实际应调用第三方支付SDK
        if pay_type == 'wechat':
            # 伪代码：调用微信支付SDK
            # result = wechat_sdk.create_order(...)
            return PaymentResult(True, '微信支付下单成功',
                                 {'out_trade_no': out_trade_no, 'pay_url': 'https://pay.wechat.com/xxx'})
        elif pay_type == 'alipay':
            # 伪代码：调用支付宝SDK
            return PaymentResult(True, '支付宝下单成功',
                                 {'out_trade_no': out_trade_no, 'pay_url': 'https://pay.alipay.com/xxx'})
        else:
            return PaymentResult(False, '暂不支持该支付方式')

    def query_order(self, out_trade_no: str, pay_type: str = 'wechat') -> PaymentResult:
        """
        查询订单支付状态。
        :param out_trade_no: 商户订单号
        :param pay_type: 支付类型
        :return: PaymentResult
        """
        # 这里只做接口结构，实际应调用第三方支付SDK
        return PaymentResult(True, '订单支付成功', {'out_trade_no': out_trade_no, 'status': 'SUCCESS'})
