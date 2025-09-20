"""
微信支付配置
"""

# 微信小程序配置
WECHAT_APPID = 'your_wechat_appid'  # 微信小程序AppID
WECHAT_SECRET = 'your_wechat_secret'  # 微信小程序Secret

# 微信支付配置
WECHAT_MCH_ID = 'your_mch_id'  # 商户号
WECHAT_MCH_KEY = 'your_mch_key'  # 商户密钥

# 支付相关URL
WECHAT_ORDER_URL = 'https://api.mch.weixin.qq.com/pay/unifiedorder'  # 统一下单接口
WECHAT_NOTIFY_URL = 'https://your-domain.com/api/pay/notify'  # 支付回调地址

# 支付配置
TRADE_TYPE = 'JSAPI'  # 交易类型：小程序支付
BODY_DESC = '心理咨询服务'  # 商品描述
