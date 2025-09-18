from flask_restx import fields


def create_user_models(api):
    """创建用户相关的 Swagger 模型"""
    # 用户完整信息模型
    user_model = api.model('User', {
        'id': fields.String(required=True, description='用户ID'),
        'username': fields.String(required=True, description='用户名'),
        'avatar': fields.String(description='头像URL'),
        'phone': fields.String(description='手机号'),
        'code': fields.String(description='邮箱'),
        'create_time': fields.DateTime(description='创建时间'),
        'update_time': fields.DateTime(description='更新时间')
    })

    # 用户创建请求模型
    user_create_model = api.model('UserCreate', {
        'username': fields.String(required=True, description='用户名', example='john_doe'),
        'avatar': fields.String(description='头像URL', example='https://example.com/avatar.jpg'),
        'phone': fields.String(description='手机号', example='13800138000'),
        'code': fields.String(description='邮箱', example='john@example.com')
    })

    # 用户更新请求模型
    user_update_model = api.model('UserUpdate', {
        'username': fields.String(description='用户名', example='john_doe_updated'),
        'avatar': fields.String(description='头像URL', example='https://example.com/new_avatar.jpg'),
        'phone': fields.String(description='手机号', example='13900139000'),
        'code': fields.String(description='邮箱', example='john_new@example.com')
    })

    # 用户列表响应模型
    user_list_model = api.model('UserList', {
        'users': fields.List(fields.Nested(user_model), description='用户列表'),
        'total': fields.Integer(description='总数'),
        'page': fields.Integer(description='当前页码'),
        'per_page': fields.Integer(description='每页数量'),
        'pages': fields.Integer(description='总页数')
    })

    # 通用成功响应模型
    success_response = api.model('SuccessResponse', {
        'code': fields.Integer(description='状态码', example=200),
        'message': fields.String(description='响应消息', example='操作成功'),
        'data': fields.Raw(description='响应数据')
    })

    # 通用错误响应模型
    error_response = api.model('ErrorResponse', {
        'code': fields.Integer(description='错误码', example=400),
        'message': fields.String(description='错误消息', example='参数错误'),
        'data': fields.Raw(description='错误详情')
    })

    return {
        'user_model': user_model,
        'user_create_model': user_create_model,
        'user_update_model': user_update_model,
        'user_list_model': user_list_model,
        'success_response': success_response,
        'error_response': error_response
    }


def create_review_models(api):
    """创建评价相关的 Swagger 模型"""
    # 评价完整信息模型
    review_model = api.model('Review', {
        'review_id': fields.String(required=True, description='评价ID'),
        'counselor_id': fields.String(required=True, description='咨询师ID'),
        'order_id': fields.String(required=True, description='订单ID'),
        'content': fields.String(description='评价内容'),
        'rating': fields.Integer(description='评分(1-5)', min=1, max=5),
        'create_time': fields.DateTime(description='创建时间'),
        'update_time': fields.DateTime(description='更新时间')
    })

    # 评价创建请求模型
    review_create_model = api.model('ReviewCreate', {
        'counselor_id': fields.String(required=True, description='咨询师ID', example='counselor-123'),
        'order_id': fields.String(required=True, description='订单ID', example='order-456'),
        'content': fields.String(description='评价内容', example='服务很好，很满意'),
        'rating': fields.Integer(description='评分(1-5)', example=5, min=1, max=5)
    })

    # 评价更新请求模型
    review_update_model = api.model('ReviewUpdate', {
        'content': fields.String(description='评价内容', example='更新后的评价内容'),
        'rating': fields.Integer(description='评分(1-5)', example=4, min=1, max=5)
    })

    # 评价列表响应模型
    review_list_model = api.model('ReviewList', {
        'reviews': fields.List(fields.Nested(review_model), description='评价列表'),
        'total': fields.Integer(description='总数'),
        'page': fields.Integer(description='当前页码'),
        'per_page': fields.Integer(description='每页数量'),
        'pages': fields.Integer(description='总页数')
    })

    # 通用成功响应模型
    success_response = api.model('SuccessResponse', {
        'code': fields.Integer(description='状态码', example=200),
        'message': fields.String(description='响应消息', example='操作成功'),
        'data': fields.Raw(description='响应数据')
    })

    # 通用错误响应模型
    error_response = api.model('ErrorResponse', {
        'code': fields.Integer(description='错误码', example=400),
        'message': fields.String(description='错误消息', example='参数错误'),
        'data': fields.Raw(description='错误详情')
    })

    return {
        'review_model': review_model,
        'review_create_model': review_create_model,
        'review_update_model': review_update_model,
        'review_list_model': review_list_model,
        'success_response': success_response,
        'error_response': error_response
    }


def create_counselor_models(api):
    """创建咨询师相关的 Swagger 模型"""
    # 可以在这里添加咨询师相关的模型定义
    pass


def create_order_models(api):
    """创建订单相关的 Swagger 模型"""
    # 可以在这里添加订单相关的模型定义
    pass
