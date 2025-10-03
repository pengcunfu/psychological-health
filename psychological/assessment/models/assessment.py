from typing import List
import json
from sqlalchemy import Column, String, Integer, DateTime, Float, Text, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from pcf_flask_helper.model.base import BaseModel
from pcf_flask_helper.common import process_image_url


class Assessment(BaseModel):
    """测评模板"""
    __tablename__ = 'assessments'
    
    id = Column(String(50), primary_key=True)  # 测评ID
    name = Column(String(200), nullable=False)  # 测评名称
    subtitle = Column(String(300))  # 测评副标题
    description = Column(Text)  # 测评描述
    cover_image = Column(String(255))  # 测评封面图片URL
    price = Column(Float, default=0.0)  # 测评价格
    original_price = Column(Float, default=0.0)  # 测评原价
    duration = Column(Integer, default=30)  # 预计完成时间（分钟）
    question_count = Column(Integer, default=0)  # 题目数量
    participant_count = Column(Integer, default=0)  # 参与人数
    rating = Column(Float, default=0.0)  # 测评评分
    difficulty = Column(String(20), default='medium')  # 难度：easy简单，medium中等，hard困难
    category = Column(String(50))  # 测评分类
    status = Column(String(20), default='draft')  # 状态：draft草稿，published已发布，archived已归档
    _tags = Column('tags', Text)  # 测评标签列表（JSON存储）
    instructions = Column(Text)  # 测评说明
    result_template = Column(Text)  # 结果模板（JSON存储）
    is_free = Column(Boolean, default=True)  # 是否免费
    sort_order = Column(Integer, default=0)  # 排序
    
    # 关系
    questions = relationship("AssessmentQuestion", back_populates="assessment", cascade="all, delete-orphan")
    records = relationship("AssessmentRecord", back_populates="assessment")

    @property
    def tags(self) -> List[str]:
        """获取标签列表"""
        if self._tags:
            return json.loads(self._tags)
        return []
    
    @tags.setter
    def tags(self, value: List[str]):
        """设置标签列表"""
        self._tags = json.dumps(value) if value else None
    
    def to_dict(self):
        """转换为字典"""
        return {
            'id': self.id,
            'name': self.name,
            'subtitle': self.subtitle,
            'description': self.description,
            'cover_image': process_image_url(self.cover_image),
            'price': self.price,
            'original_price': self.original_price,
            'duration': self.duration,
            'question_count': self.question_count,
            'participant_count': self.participant_count,
            'rating': self.rating,
            'difficulty': self.difficulty,
            'category': self.category,
            'status': self.status,
            'tags': self.tags,
            'instructions': self.instructions,
            'is_free': self.is_free,
            'sort_order': self.sort_order,
            'create_time': self.create_time.isoformat() if self.create_time else None,
            'update_time': self.update_time.isoformat() if self.update_time else None
        }


class AssessmentQuestion(BaseModel):
    """测评题目"""
    __tablename__ = 'assessment_questions'
    
    id = Column(String(50), primary_key=True)  # 题目ID
    assessment_id = Column(String(50), ForeignKey('assessments.id'), nullable=False)  # 测评ID
    question_text = Column(Text, nullable=False)  # 题目内容
    question_type = Column(String(20), default='single')  # 题目类型：single单选，multiple多选，text文本，scale量表
    question_order = Column(Integer, default=0)  # 题目序号
    is_required = Column(Boolean, default=True)  # 是否必答
    score_weight = Column(Float, default=1.0)  # 分值权重
    dimension = Column(String(50))  # 维度标识
    description = Column(Text)  # 题目说明
    
    # 关系
    assessment = relationship("Assessment", back_populates="questions")
    options = relationship("AssessmentOption", back_populates="question", cascade="all, delete-orphan")
    answers = relationship("AssessmentAnswer", back_populates="question")
    
    def to_dict(self):
        """转换为字典"""
        return {
            'id': self.id,
            'assessment_id': self.assessment_id,
            'question_text': self.question_text,
            'question_type': self.question_type,
            'question_order': self.question_order,
            'is_required': self.is_required,
            'score_weight': self.score_weight,
            'dimension': self.dimension,
            'description': self.description,
            'options': [option.to_dict() for option in self.options],
            'create_time': self.create_time.isoformat() if self.create_time else None
        }


class AssessmentOption(BaseModel):
    """测评选项"""
    __tablename__ = 'assessment_options'
    
    id = Column(String(50), primary_key=True)  # 选项ID
    question_id = Column(String(50), ForeignKey('assessment_questions.id'), nullable=False)  # 题目ID
    option_text = Column(String(500), nullable=False)  # 选项内容
    option_value = Column(String(50))  # 选项值
    score = Column(Float, default=0.0)  # 选项分值
    option_order = Column(Integer, default=0)  # 选项序号
    
    # 关系
    question = relationship("AssessmentQuestion", back_populates="options")
    
    def to_dict(self):
        """转换为字典"""
        return {
            'id': self.id,
            'question_id': self.question_id,
            'option_text': self.option_text,
            'option_value': self.option_value,
            'score': self.score,
            'option_order': self.option_order
        }


class AssessmentRecord(BaseModel):
    """测评记录"""
    __tablename__ = 'assessment_records'
    
    id = Column(String(50), primary_key=True)  # 记录ID
    user_id = Column(String(50), nullable=False)  # 用户ID
    assessment_id = Column(String(50), ForeignKey('assessments.id'), nullable=False)  # 测评ID
    status = Column(String(20), default='in_progress')  # 状态：in_progress进行中，completed已完成，expired已过期
    start_time = Column(DateTime)  # 开始时间
    complete_time = Column(DateTime)  # 完成时间
    total_score = Column(Float, default=0.0)  # 总分
    max_score = Column(Float, default=0.0)  # 满分
    result_level = Column(String(50))  # 结果等级
    result_description = Column(Text)  # 结果描述
    result_suggestion = Column(Text)  # 建议
    dimension_scores = Column(Text)  # 各维度得分（JSON存储）
    is_anonymous = Column(Boolean, default=False)  # 是否匿名
    
    # 关系
    assessment = relationship("Assessment", back_populates="records")
    answers = relationship("AssessmentAnswer", back_populates="record", cascade="all, delete-orphan")
    
    @property
    def dimension_score_dict(self):
        """获取维度得分字典"""
        if self.dimension_scores:
            return json.loads(self.dimension_scores)
        return {}
    
    @dimension_score_dict.setter
    def dimension_score_dict(self, value):
        """设置维度得分字典"""
        self.dimension_scores = json.dumps(value) if value else None
    
    def to_dict(self):
        """转换为字典"""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'assessment_id': self.assessment_id,
            'status': self.status,
            'start_time': self.start_time.isoformat() if self.start_time else None,
            'complete_time': self.complete_time.isoformat() if self.complete_time else None,
            'total_score': self.total_score,
            'max_score': self.max_score,
            'result_level': self.result_level,
            'result_description': self.result_description,
            'result_suggestion': self.result_suggestion,
            'dimension_scores': self.dimension_score_dict,
            'is_anonymous': self.is_anonymous,
            'create_time': self.create_time.isoformat() if self.create_time else None,
            'update_time': self.update_time.isoformat() if self.update_time else None
        }


class AssessmentAnswer(BaseModel):
    """测评答案"""
    __tablename__ = 'assessment_answers'
    
    id = Column(String(50), primary_key=True)  # 答案ID
    record_id = Column(String(50), ForeignKey('assessment_records.id'), nullable=False)  # 记录ID
    question_id = Column(String(50), ForeignKey('assessment_questions.id'), nullable=False)  # 题目ID
    option_ids = Column(Text)  # 选择的选项ID列表（JSON存储）
    answer_text = Column(Text)  # 文本答案
    score = Column(Float, default=0.0)  # 得分
    
    # 关系
    record = relationship("AssessmentRecord", back_populates="answers")
    question = relationship("AssessmentQuestion", back_populates="answers")
    
    @property
    def selected_options(self):
        """获取选择的选项ID列表"""
        if self.option_ids:
            return json.loads(self.option_ids)
        return []
    
    @selected_options.setter
    def selected_options(self, value):
        """设置选择的选项ID列表"""
        self.option_ids = json.dumps(value) if value else None
    
    def to_dict(self):
        """转换为字典"""
        return {
            'id': self.id,
            'record_id': self.record_id,
            'question_id': self.question_id,
            'option_ids': self.selected_options,
            'answer_text': self.answer_text,
            'score': self.score,
            'create_time': self.create_time.isoformat() if self.create_time else None
        } 