from datetime import datetime
import uuid
from sqlalchemy import Column, String, Integer, DateTime, Float, Text
from pcf_flask_helper.model.base import BaseModel


class CourseSubscription(BaseModel):
    """课程订阅记录模型"""
    __tablename__ = 'course_subscriptions'

    # 基本字段
    id = Column(String(50), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String(50), nullable=False, comment='用户ID')
    course_id = Column(String(50), nullable=False, comment='课程ID')

    # 订阅信息
    subscription_type = Column(String(20), default='standard', comment='订阅类型：standard标准，premium高级')
    status = Column(String(20), default='active', comment='订阅状态：active有效，expired过期，cancelled取消')

    # 价格信息
    paid_price = Column(Float, nullable=False, comment='实际支付价格')
    original_price = Column(Float, nullable=False, comment='课程原价')
    discount_amount = Column(Float, default=0.0, comment='折扣金额')

    # 时间信息
    subscription_date = Column(DateTime, default=datetime.utcnow, comment='订阅时间')
    expiry_date = Column(DateTime, comment='过期时间（如果有的话）')
    last_accessed = Column(DateTime, comment='最后访问时间')

    # 学习进度
    progress_percentage = Column(Float, default=0.0, comment='学习进度百分比（0-100）')
    completed_lessons = Column(Integer, default=0, comment='已完成课时数')
    total_study_time = Column(Integer, default=0, comment='总学习时间（分钟）')

    # 订单信息
    order_id = Column(String(50), comment='关联订单ID')
    payment_method = Column(String(50), comment='支付方式')
    payment_transaction_id = Column(String(100), comment='支付交易ID')

    # 备注信息
    notes = Column(Text, comment='备注信息')

    def is_active(self):
        """检查订阅是否有效"""
        if self.status != 'active':
            return False

        # 如果有过期时间，检查是否过期
        if self.expiry_date and self.expiry_date < datetime.utcnow():
            return False

        return True

    def is_expired(self):
        """检查订阅是否过期"""
        if self.expiry_date and self.expiry_date < datetime.utcnow():
            return True
        return False

    def update_progress(self, completed_lessons=None, study_time_minutes=None):
        """更新学习进度"""
        if completed_lessons is not None:
            self.completed_lessons = completed_lessons
            # 简化的进度计算，避免依赖course关系
            if completed_lessons > 0:
                self.progress_percentage = min(completed_lessons * 10, 100)  # 简单估算

        if study_time_minutes is not None:
            self.total_study_time += study_time_minutes

        self.last_accessed = datetime.utcnow()

    def extend_subscription(self, days=30):
        """延长订阅时间"""
        if not self.expiry_date:
            self.expiry_date = datetime.utcnow()

        from datetime import timedelta
        self.expiry_date += timedelta(days=days)

        if self.status == 'expired':
            self.status = 'active'

    def cancel_subscription(self, reason=None):
        """取消订阅"""
        self.status = 'cancelled'
        if reason:
            self.notes = f"取消原因: {reason}" + (f"\n{self.notes}" if self.notes else "")

    def to_dict(self):
        """转换为字典"""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'course_id': self.course_id,
            'subscription_type': self.subscription_type,
            'status': self.status,
            'status_text': self.get_status_text(),
            'paid_price': self.paid_price,
            'original_price': self.original_price,
            'discount_amount': self.discount_amount,
            'subscription_date': self.subscription_date.isoformat() if self.subscription_date else None,
            'expiry_date': self.expiry_date.isoformat() if self.expiry_date else None,
            'last_accessed': self.last_accessed.isoformat() if self.last_accessed else None,
            'progress_percentage': self.progress_percentage,
            'completed_lessons': self.completed_lessons,
            'total_study_time': self.total_study_time,
            'order_id': self.order_id,
            'payment_method': self.payment_method,
            'payment_transaction_id': self.payment_transaction_id,
            'notes': self.notes,
            'is_active': self.is_active(),
            'is_expired': self.is_expired(),
            'create_time': self.create_time.isoformat() if self.create_time else None,
            'update_time': self.update_time.isoformat() if self.update_time else None
        }

    def get_status_text(self):
        """获取状态文本"""
        status_map = {
            'active': '有效',
            'expired': '已过期',
            'cancelled': '已取消'
        }
        return status_map.get(self.status, '未知')

    def to_simple_dict(self):
        """简化的字典格式（用于列表显示）"""
        return {
            'id': self.id,
            'course_id': self.course_id,
            'subscription_type': self.subscription_type,
            'status': self.status,
            'status_text': self.get_status_text(),
            'progress_percentage': self.progress_percentage,
            'subscription_date': self.subscription_date.isoformat() if self.subscription_date else None,
            'expiry_date': self.expiry_date.isoformat() if self.expiry_date else None,
            'is_active': self.is_active()
        }

    def __repr__(self):
        return f'<CourseSubscription {self.user_id}-{self.course_id}>'
