from sqlalchemy import Column, String, Integer
from pcf_flask_helper.model.base import BaseModel


class Menu(BaseModel):
    """菜单实体"""
    __tablename__ = 'menus'
    
    id = Column(String(50), primary_key=True)  # 菜单ID
    name = Column(String(100), nullable=False)  # 菜单名称
    path = Column(String(255))  # 菜单路径
    icon = Column(String(100))  # 菜单图标
    parent_id = Column(String(50), default='')  # 父菜单ID（顶级菜单为空字符串）
    level = Column(Integer, default=1)  # 菜单层级（1-顶级菜单，2-二级菜单，以此类推）
    sort_order = Column(Integer, default=0)  # 排序顺序
    menu_type = Column(Integer, default=2)  # 菜单类型（1-目录，2-菜单，3-按钮）
    permission = Column(String(100))  # 权限标识
    component = Column(String(255))  # 组件路径
    is_external = Column(Integer, default=0)  # 是否外链（0-否，1-是）
    is_visible = Column(Integer, default=1)  # 是否显示（0-隐藏，1-显示）
    is_cache = Column(Integer, default=0)  # 是否缓存（0-否，1-是）
    status = Column(Integer, default=1)  # 状态（0-禁用，1-启用）
    remark = Column(String(500))  # 备注

    def is_directory(self) -> bool:
        """是否为目录"""
        return self.menu_type == 1

    def is_menu(self) -> bool:
        """是否为菜单"""
        return self.menu_type == 2

    def is_button(self) -> bool:
        """是否为按钮"""
        return self.menu_type == 3

    def is_top_level(self) -> bool:
        """是否为顶级菜单"""
        return self.level == 1 and self.parent_id == ""
    
    def to_dict(self):
        """转换为字典"""
        return {
            'id': self.id,
            'name': self.name,
            'path': self.path,
            'icon': self.icon,
            'parent_id': self.parent_id,
            'level': self.level,
            'sort_order': self.sort_order,
            'menu_type': self.menu_type,
            'permission': self.permission,
            'component': self.component,
            'is_external': self.is_external,
            'is_visible': self.is_visible,
            'is_cache': self.is_cache,
            'status': self.status,
            'remark': self.remark,
            'create_time': self.create_time.isoformat() if self.create_time else None,
            'update_time': self.update_time.isoformat() if self.update_time else None
        }