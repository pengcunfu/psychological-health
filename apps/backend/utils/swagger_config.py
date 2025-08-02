from flask_restx import Api
from flask import Blueprint

# 创建API文档蓝图
api_bp = Blueprint('api_docs', __name__, url_prefix='/api')

# 配置Swagger API文档
api = Api(
    api_bp,
    version='1.0',
    title='心理健康服务API',
    description='心理健康服务后端API文档，提供用户管理、咨询师管理、课程管理、预约管理等功能',
    doc='/docs/',  # Swagger UI访问路径
    contact='开发团队',
    contact_email='dev@mentalhealth.com',
    license='MIT',
    license_url='https://opensource.org/licenses/MIT',
    authorizations={
        'Bearer': {
            'type': 'apiKey',
            'in': 'header',
            'name': 'Authorization',
            'description': 'JWT Token认证，格式: Bearer <token>'
        }
    },
    security='Bearer'
)

# 定义通用的响应模型
from flask_restx import fields

# 成功响应模型
success_response = api.model('SuccessResponse', {
    'code': fields.Integer(description='响应状态码', example=200),
    'message': fields.String(description='响应消息', example='操作成功'),
    'data': fields.Raw(description='响应数据')
})

# 错误响应模型
error_response = api.model('ErrorResponse', {
    'code': fields.Integer(description='错误状态码', example=400),
    'message': fields.String(description='错误消息', example='请求参数错误'),
    'data': fields.Raw(description='错误详情', default=None)
})

# 分页响应模型
pagination_response = api.model('PaginationResponse', {
    'code': fields.Integer(description='响应状态码', example=200),
    'message': fields.String(description='响应消息', example='获取成功'),
    'data': fields.Nested(api.model('PaginationData', {
        'total': fields.Integer(description='总记录数', example=100),
        'page': fields.Integer(description='当前页码', example=1),
        'per_page': fields.Integer(description='每页记录数', example=10),
        'pages': fields.Integer(description='总页数', example=10),
        'items': fields.List(fields.Raw, description='数据列表')
    }))
})

# 用户模型
user_model = api.model('User', {
    'id': fields.String(description='用户ID', example='uuid-string'),
    'username': fields.String(description='用户名', example='张三'),
    'avatar': fields.String(description='头像URL', example='https://example.com/avatar.jpg'),
    'phone': fields.String(description='手机号', example='13800138000'),
    'email': fields.String(description='邮箱', example='user@example.com'),
    'create_time': fields.DateTime(description='创建时间'),
    'update_time': fields.DateTime(description='更新时间')
})

# 咨询师模型
counselor_model = api.model('Counselor', {
    'id': fields.String(description='咨询师ID', example='uuid-string'),
    'name': fields.String(description='姓名', example='李医生'),
    'avatar': fields.String(description='头像URL', example='https://example.com/avatar.jpg'),
    'title': fields.String(description='职称', example='主任医师'),
    'price': fields.Float(description='咨询价格', example=200.0),
    'rating': fields.Float(description='评分', example=4.8),
    'consultation_count': fields.Integer(description='咨询次数', example=100),
    'introduction': fields.String(description='简介', example='专业心理咨询师'),
    'tags': fields.List(fields.String, description='标签列表', example=['焦虑', '抑郁'])
})

# 课程模型
course_model = api.model('Course', {
    'id': fields.String(description='课程ID', example='uuid-string'),
    'title': fields.String(description='课程标题', example='心理健康基础课程'),
    'description': fields.String(description='课程描述'),
    'cover_image': fields.String(description='封面图片URL'),
    'price': fields.Float(description='课程价格', example=99.0),
    'duration': fields.Integer(description='课程时长(分钟)', example=60),
    'category_id': fields.String(description='分类ID'),
    'instructor_id': fields.String(description='讲师ID'),
    'status': fields.Integer(description='状态(1:启用 0:禁用)', example=1)
})

# 订单模型
order_model = api.model('Order', {
    'id': fields.String(description='订单ID', example='uuid-string'),
    'user_id': fields.String(description='用户ID'),
    'product_id': fields.String(description='产品ID'),
    'type': fields.String(description='订单类型', example='course'),
    'amount': fields.Float(description='订单金额', example=99.0),
    'status': fields.String(description='订单状态', example='paid'),
    'create_time': fields.DateTime(description='创建时间'),
    'pay_time': fields.DateTime(description='支付时间')
})

# 预约模型
appointment_model = api.model('Appointment', {
    'id': fields.String(description='预约ID', example='uuid-string'),
    'user_id': fields.String(description='用户ID'),
    'counselor_id': fields.String(description='咨询师ID'),
    'appointment_time': fields.DateTime(description='预约时间'),
    'duration': fields.Integer(description='预约时长(分钟)', example=60),
    'status': fields.String(description='预约状态', example='confirmed'),
    'notes': fields.String(description='备注信息')
})

# 评价模型
review_model = api.model('Review', {
    'review_id': fields.String(description='评价ID', example='uuid-string'),
    'counselor_id': fields.String(description='咨询师ID'),
    'order_id': fields.String(description='订单ID'),
    'content': fields.String(description='评价内容', example='服务很好'),
    'rating': fields.Integer(description='评分(1-5)', example=5),
    'create_time': fields.DateTime(description='创建时间')
})

# 导入命名空间
# from api.user import user_ns
# from api.review import review_ns
# from api.swagger_counselor import counselor_ns
# from api.swagger_order import order_ns

# 注册命名空间
# api.add_namespace(user_ns)
# api.add_namespace(review_ns)
# api.add_namespace(counselor_ns)
# api.add_namespace(order_ns)

# 收藏模型
favorite_model = api.model('UserFavorite', {
    'id': fields.String(description='收藏ID', example='uuid-string'),
    'user_id': fields.String(description='用户ID'),
    'item_id': fields.String(description='收藏项目ID'),
    'item_type': fields.String(description='收藏类型', example='course'),
    'create_time': fields.DateTime(description='创建时间')
})
