from typing import List

from sqlalchemy import Column, String, Integer, Text, Boolean

from pcf_flask_helper.model.base import BaseModel
import json


class Role(BaseModel):
    """角色实体"""
    __tablename__ = 'roles'

    id = Column(String(50), primary_key=True)  # 角色ID
    name = Column(String(100), nullable=False)  # 角色名称
    code = Column(String(50), nullable=False, unique=True)  # 角色编码
    description = Column(Text)  # 角色描述
    sort_order = Column(Integer, default=0)  # 排序顺序
    data_scope = Column(Integer, default=1)  # 数据权限范围（1-全部数据，2-自定义数据，3-本部门数据，4-本部门及以下数据，5-仅本人数据）
    menu_ids_json = Column(Text)  # 菜单权限ID列表（JSON格式存储）
    status = Column(Integer, default=1)  # 状态（0-禁用，1-启用）
    is_default = Column(Boolean, default=False)  # 是否默认角色
    remark = Column(Text)  # 备注

    @property
    def menu_ids(self) -> List[str]:
        """获取菜单权限ID列表"""
        if self.menu_ids_json:
            return json.loads(self.menu_ids_json)
        return []

    @menu_ids.setter
    def menu_ids(self, value: List[str]):
        """设置菜单权限ID列表"""
        self.menu_ids_json = json.dumps(value) if value else None

    def is_enabled(self) -> bool:
        """是否启用"""
        return self.status == 1

    def has_menu_permission(self, menu_id: str) -> bool:
        """是否有菜单权限"""
        return menu_id in self.menu_ids

    def add_menu_permission(self, menu_id: str):
        """添加菜单权限"""
        current_ids = self.menu_ids
        if menu_id not in current_ids:
            current_ids.append(menu_id)
            self.menu_ids = current_ids

    def remove_menu_permission(self, menu_id: str):
        """移除菜单权限"""
        current_ids = self.menu_ids
        if menu_id in current_ids:
            current_ids.remove(menu_id)
            self.menu_ids = current_ids

    def get_data_scope_name(self) -> str:
        """获取数据权限范围名称"""
        scope_names = {
            1: "全部数据",
            2: "自定义数据",
            3: "本部门数据",
            4: "本部门及以下数据",
            5: "仅本人数据"
        }
        return scope_names.get(self.data_scope, "未知权限")

    def to_dict(self):
        """转换为字典格式"""
        return {
            'id': self.id,
            'name': self.name,
            'code': self.code,
            'description': self.description,
            'sort_order': self.sort_order,
            'data_scope': self.data_scope,
            'menu_ids': self.menu_ids,
            'status': self.status,
            'is_default': self.is_default,
            'remark': self.remark,
            'create_time': self.create_time.isoformat() if self.create_time else None,
            'update_time': self.update_time.isoformat() if self.update_time else None
        }
