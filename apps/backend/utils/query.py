"""
查询构造器工具类
提供简化的查询条件构建功能
"""
from datetime import datetime
from typing import Any, Dict, List, Optional, Union
from sqlalchemy.orm import Query
from sqlalchemy import and_, or_, func
from models.base import db


class QueryBuilder:
    """查询构造器类"""

    def __init__(self, model_class):
        """
        初始化查询构造器
        
        Args:
            model_class: SQLAlchemy模型类
        """
        self.model_class = model_class
        self.query = model_class.query
        self._conditions = []
        self._joins = []
        self._order_by = []
        self._group_by = []
        self._having = []

    def filter(self, *conditions) -> 'QueryBuilder':
        """
        添加一个或多个过滤条件（SQLAlchemy条件表达式）
        
        Args:
            *conditions: SQLAlchemy条件表达式
        
        Examples:
            builder.filter(User.age > 18)
            builder.filter(User.age > 18, User.status == 'active')
            builder.filter(User.name.like('%admin%'))
        """
        for condition in conditions:
            if condition is not None:
                self._conditions.append(condition)
        return self

    def filter_if(self, condition, check: bool = True) -> 'QueryBuilder':
        """
        条件性过滤
        
        Args:
            condition: SQLAlchemy条件表达式
            check: 是否应用此条件
        
        Examples:
            builder.filter_if(User.age > 18, age_filter_enabled)
        """
        if check and condition is not None:
            self._conditions.append(condition)
        return self

    def when(self, condition: bool, *sql_conditions) -> 'QueryBuilder':
        """
        条件性执行 - 支持直接传递条件或回调函数
        
        Args:
            condition: 检查条件
            *sql_conditions: SQLAlchemy条件表达式 或 回调函数
        
        Examples:
            # 直接传递SQL条件
            builder.when(not is_manager, User.id == current_user_id)
            
            # 传递回调函数
            builder.when(not is_manager, lambda q: q.filter(User.id == current_user_id))
            
            # 传递多个条件
            builder.when(is_admin, User.role == 'admin', User.status == 'active')
        """
        if condition:
            for sql_condition in sql_conditions:
                if callable(sql_condition):
                    sql_condition(self)
                else:
                    self._conditions.append(sql_condition)
        return self

    def unless(self, condition: bool, *sql_conditions) -> 'QueryBuilder':
        """
        条件性执行（条件为False时执行）
        
        Args:
            condition: 检查条件
            *sql_conditions: SQLAlchemy条件表达式 或 回调函数
        """
        if not condition:
            for sql_condition in sql_conditions:
                if callable(sql_condition):
                    sql_condition(self)
                else:
                    self._conditions.append(sql_condition)
        return self

    def order_by_dynamic(self, sort_field: Optional[str] = None, sort_direction: Optional[str] = None,
                         default_field: str = 'create_time', default_direction: str = 'desc',
                         valid_fields: Optional[Dict[str, Any]] = None) -> 'QueryBuilder':
        """
        动态排序
        
        Args:
            sort_field: 排序字段
            sort_direction: 排序方向
            default_field: 默认排序字段
            default_direction: 默认排序方向
            valid_fields: 有效字段映射字典
        """
        # 确定排序字段
        field_to_use = sort_field or default_field
        direction_to_use = sort_direction or default_direction

        # 验证字段是否有效
        if valid_fields and field_to_use not in valid_fields:
            field_to_use = default_field

        # 应用排序
        self.order_by(field_to_use, direction_to_use)
        return self

    def join(self, *models) -> 'QueryBuilder':
        """
        添加INNER JOIN
        
        Args:
            *models: 要JOIN的模型或JOIN表达式
            
        Examples:
            builder.join(User)
            builder.join(User, Role)
        """
        for model in models:
            self._joins.append(('join', model))
        return self
    
    def outerjoin(self, *models) -> 'QueryBuilder':
        """
        添加LEFT OUTER JOIN
        
        Args:
            *models: 要OUTER JOIN的模型或JOIN表达式
            
        Examples:
            builder.outerjoin(User)
            builder.outerjoin(User, User.id == Consultant.user_id)
        """
        for model in models:
            self._joins.append(('outerjoin', model))
        return self
    
    def leftjoin(self, *models) -> 'QueryBuilder':
        """
        添加LEFT JOIN（outerjoin的别名）
        
        Args:
            *models: 要LEFT JOIN的模型或JOIN表达式
            
        Examples:
            builder.leftjoin(User)
            builder.leftjoin(User, User.id == Consultant.user_id)
        """
        return self.outerjoin(*models)

    def order_by(self, *order_expressions) -> 'QueryBuilder':
        """
        添加排序表达式
        
        Args:
            *order_expressions: SQLAlchemy排序表达式
        
        Examples:
            builder.order_by(User.create_time.desc())
            builder.order_by(User.name.asc(), User.create_time.desc())
        """
        for expr in order_expressions:
            if expr is not None:
                self._order_by.append(expr)
        return self

    def group_by(self, *group_expressions) -> 'QueryBuilder':
        """
        添加GROUP BY表达式
        
        Args:
            *group_expressions: SQLAlchemy分组表达式
        
        Examples:
            builder.group_by(User.department)
            builder.group_by(User.department, User.role)
        """
        for expr in group_expressions:
            if expr is not None:
                self._group_by.append(expr)
        return self

    def having(self, *having_expressions) -> 'QueryBuilder':
        """
        添加HAVING条件
        
        Args:
            *having_expressions: SQLAlchemy HAVING表达式
        
        Examples:
            builder.having(func.count(User.id) > 5)
        """
        for expr in having_expressions:
            if expr is not None:
                self._having.append(expr)
        return self

    def build(self) -> Query:
        """构建并返回查询对象"""
        query = self.query

        # 添加JOIN
        for join_info in self._joins:
            if isinstance(join_info, tuple) and len(join_info) == 2:
                join_type, model = join_info
                if join_type == 'join':
                    query = query.join(model)
                elif join_type == 'outerjoin':
                    query = query.outerjoin(model)
            else:
                # 兼容旧的格式，默认为inner join
                query = query.join(join_info)

        # 添加WHERE条件
        if self._conditions:
            query = query.filter(and_(*self._conditions))

        # 添加GROUP BY
        if self._group_by:
            query = query.group_by(*self._group_by)

        # 添加HAVING
        if self._having:
            query = query.having(and_(*self._having))

        # 添加ORDER BY
        if self._order_by:
            query = query.order_by(*self._order_by)

        return query

    def paginate(self, page: int = 1, per_page: int = 10, max_per_page: int = 100) -> dict:
        """
        分页查询
        
        Args:
            page: 页码
            per_page: 每页数量
            max_per_page: 每页最大数量
        
        Returns:
            分页结果字典
        """
        per_page = min(per_page, max_per_page)
        query = self.build()
        pagination = query.paginate(page=page, per_page=per_page, error_out=False)

        return {
            'items': pagination.items,
            'total': pagination.total,
            'page': page,
            'per_page': per_page,
            'pages': pagination.pages,
            'has_prev': pagination.has_prev,
            'has_next': pagination.has_next
        }

    def count(self) -> int:
        """获取记录数量"""
        return self.build().count()

    def first(self):
        """获取第一条记录"""
        return self.build().first()

    def all(self) -> List:
        """获取所有记录"""
        return self.build().all()

    def exists(self) -> bool:
        """检查是否存在记录"""
        return db.session.query(self.build().exists()).scalar()


def create_query_builder(model_class) -> QueryBuilder:
    """创建查询构造器的快捷函数"""
    return QueryBuilder(model_class)


def check_exists(model_class, conditions, error_message: str = "记录不存在", error_code: int = 404):
    """
    检查记录是否存在的快捷方法
    
    Args:
        model_class: SQLAlchemy模型类
        conditions: 查询条件（可以是单个条件或条件列表）
        error_message: 错误消息
        error_code: 错误代码
    
    Returns:
        记录对象或JsonResult错误响应
        
    Examples:
        # 检查用户是否存在
        user = check_exists(User, User.id == user_id, "用户不存在")
        if hasattr(user, 'error'):
            return user  # 直接返回错误响应
        
        # 检查多个条件
        order = check_exists(Order, [Order.id == order_id, Order.user_id == current_user_id], "订单不存在或无权限访问")
        
        # 自定义错误代码
        admin = check_exists(User, User.role == 'admin', "管理员不存在", 403)
    """
    from utils.json_result import JsonResult

    builder = create_query_builder(model_class)

    # 处理条件参数
    if isinstance(conditions, (list, tuple)):
        builder.filter(*conditions)
    else:
        builder.filter(conditions)

    record = builder.first()

    if not record:
        return JsonResult.error(error_message, error_code)

    return record


def check_not_exists(model_class, conditions, error_message: str = "记录已存在", error_code: int = 400):
    """
    检查记录不存在的快捷方法（用于注册、创建等场景）
    
    Args:
        model_class: SQLAlchemy模型类
        conditions: 查询条件（可以是单个条件或条件列表）
        error_message: 错误消息（当记录存在时返回）
        error_code: 错误代码
    
    Returns:
        None（记录不存在）或JsonResult错误响应（记录已存在）
        
    Examples:
        # 检查用户名是否已存在
        error = check_not_exists(User, User.username == username, "用户名已存在")
        if error:
            return error  # 直接返回错误响应
        
        # 检查手机号是否已存在
        error = check_not_exists(User, User.phone == phone, "手机号已存在")
        if error:
            return error
    """
    from utils.json_result import JsonResult

    builder = create_query_builder(model_class)

    # 处理条件参数
    if isinstance(conditions, (list, tuple)):
        builder.filter(*conditions)
    else:
        builder.filter(conditions)

    record = builder.first()

    if record:
        return JsonResult.error(error_message, error_code)

    return None  # 记录不存在，返回None表示检查通过


def assert_not_exists(model_class, conditions, error_message: str = "记录已存在", error_code: int = 400):
    """
    当记录存在时抛出异常
    
    Args:
        model_class: SQLAlchemy模型类
        conditions: 查询条件（可以是单个条件或条件列表）
        error_message: 错误消息
        error_code: 错误代码
        
    Raises:
        ValueError: 当记录存在时抛出异常
        
    Examples:
        # 检查用户名是否已存在，存在则抛出异常
        when_exists(User, User.username == username, "用户名已存在")
        
        # 检查手机号是否已存在
        when_exists(User, User.phone == phone, "手机号已存在")
    """
    builder = create_query_builder(model_class)

    # 处理条件参数
    if isinstance(conditions, (list, tuple)):
        builder.filter(*conditions)
    else:
        builder.filter(conditions)

    record = builder.first()

    if record:
        # 创建一个包含错误代码的异常
        exception = ValueError(error_message)
        exception.error_code = error_code
        raise exception


def assert_exists(model_class, conditions, error_message: str = "记录不存在", error_code: int = 404):
    """
    当记录不存在时抛出异常，存在时返回记录对象
    
    Args:
        model_class: SQLAlchemy模型类
        conditions: 查询条件（可以是单个条件或条件列表）
        error_message: 错误消息
        error_code: 错误代码
        
    Returns:
        记录对象（当记录存在时）
        
    Raises:
        ValueError: 当记录不存在时抛出异常
        
    Examples:
        # 检查用户是否存在，不存在则抛出异常
        user = when_not_exists(User, User.id == user_id, "用户不存在")
        
        # 检查订单是否存在且属于当前用户
        order = when_not_exists(Order, [Order.id == order_id, Order.user_id == current_user_id], "订单不存在或无权限访问")
    """
    builder = create_query_builder(model_class)

    # 处理条件参数
    if isinstance(conditions, (list, tuple)):
        builder.filter(*conditions)
    else:
        builder.filter(conditions)

    record = builder.first()

    if not record:
        # 创建一个包含错误代码的异常
        exception = ValueError(error_message)
        exception.error_code = error_code
        raise exception

    return record
