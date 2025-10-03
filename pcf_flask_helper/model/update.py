"""
模型更新工具类
提供简化的模型属性更新功能，避免重复的if判断
"""
from typing import Any, Dict, Optional
from pcf_flask_helper.model.base import db


class UpdateBuilder:
    """模型更新构造器类"""

    def __init__(self, model_instance):
        """
        初始化更新构造器
        
        Args:
            model_instance: SQLAlchemy模型实例
        """
        self.model = model_instance

    def set(self, attr_name: str, value: Any) -> 'UpdateBuilder':
        """
        设置属性值（无条件设置）
        
        Args:
            attr_name: 属性名
            value: 属性值
        
        Examples:
            builder.set('title', 'New Title')
        """
        if hasattr(self.model, attr_name):
            setattr(self.model, attr_name, value)
        return self

    def set_if(self, attr_name: str, value: Any, condition: bool = True) -> 'UpdateBuilder':
        """
        条件性设置属性值
        
        Args:
            attr_name: 属性名
            value: 属性值
            condition: 是否设置的条件
        
        Examples:
            builder.set_if('status', 'published', form.status.data is not None)
        """
        if condition and hasattr(self.model, attr_name):
            setattr(self.model, attr_name, value)
        return self

    def when(self, condition: Any, attr_name: str, value: Any = None) -> 'UpdateBuilder':
        """
        条件性更新 - 当条件为真值时设置属性
        
        Args:
            condition: 检查条件（通常是form.field.data）
            attr_name: 属性名
            value: 属性值（如果为None，则使用condition作为值）
        
        Examples:
            # 使用form数据作为条件和值
            builder.when(form.title.data, 'title')
            
            # 指定不同的值
            builder.when(form.is_active.data, 'status', 'active')
            
            # 使用自定义条件
            builder.when(user_is_admin, 'admin_only_field', True)
        """
        if condition is not None and condition is not False and condition != '':
            actual_value = value if value is not None else condition
            if hasattr(self.model, attr_name):
                setattr(self.model, attr_name, actual_value)
        return self

    def unless(self, condition: Any, attr_name: str, value: Any) -> 'UpdateBuilder':
        """
        条件性更新 - 当条件为假值时设置属性
        
        Args:
            condition: 检查条件
            attr_name: 属性名
            value: 属性值
        """
        if not condition:
            if hasattr(self.model, attr_name):
                setattr(self.model, attr_name, value)
        return self

    def commit(self, session=None) -> 'UpdateBuilder':
        """
        提交更改到数据库
        
        Args:
            session: 数据库会话（默认使用db.session）
        """
        session = session or db.session
        session.commit()
        return self

    def get_model(self):
        """获取更新后的模型实例"""
        return self.model


def create_update_builder(model_instance) -> UpdateBuilder:
    """创建更新构造器的快捷函数"""
    return UpdateBuilder(model_instance)


def update_model_from_form(model_instance, form, field_mapping: Optional[Dict[str, str]] = None,
                           exclude_fields: Optional[list] = None):
    """
    从表单更新模型的便捷函数
    
    Args:
        model_instance: 模型实例
        form: 表单对象
        field_mapping: 字段映射
        exclude_fields: 排除的字段列表
    
    Examples:
        update_model_from_form(announcement, form, 
                             exclude_fields=['id', 'create_time'])
    """
    builder = create_update_builder(model_instance)

    exclude_fields = exclude_fields or []

    # 处理表单字段
    for field in form:
        field_name = field.name
        if field_name in exclude_fields or field.data is None:
            continue

        # 普通字段
        model_attr = field_mapping.get(field_name, field_name) if field_mapping else field_name
        builder.when(field.data, model_attr)

    return builder
