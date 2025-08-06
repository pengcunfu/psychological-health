from wtforms import StringField, IntegerField, FloatField, TextAreaField, BooleanField, SelectField, FieldList, FormField
from wtforms.validators import DataRequired, Optional, Length, NumberRange, ValidationError
from .base import BaseForm


class AssessmentQueryForm(BaseForm):
    """测评查询表单"""
    page = IntegerField('页码', [Optional()], default=1)
    per_page = IntegerField('每页数量', [Optional()], default=10)
    name = StringField('测评名称', [Optional()])
    category = StringField('测评分类', [Optional()])
    difficulty = SelectField('难度', [Optional()], choices=[
        ('', '全部'),
        ('easy', '简单'),
        ('medium', '中等'),
        ('hard', '困难')
    ], default='')
    is_free = BooleanField('是否免费', [Optional()])
    status = SelectField('状态', [Optional()], choices=[
        ('', '全部'),
        ('draft', '草稿'),
        ('published', '已发布'),
        ('archived', '已归档')
    ], default='')
    keyword = StringField('搜索关键词', [Optional()])
    sort_by = StringField('排序字段', [Optional()], default='create_time')
    sort_order = StringField('排序方向', [Optional()], default='desc')


class AssessmentCreateForm(BaseForm):
    """创建测评表单"""
    name = StringField('测评名称', [DataRequired(), Length(1, 200)])
    subtitle = StringField('测评副标题', [Optional(), Length(0, 300)])
    description = TextAreaField('测评描述', [Optional()])
    cover_image = StringField('封面图片', [Optional(), Length(0, 255)])
    price = FloatField('价格', [Optional(), NumberRange(min=0)], default=0.0)
    original_price = FloatField('原价', [Optional(), NumberRange(min=0)], default=0.0)
    duration = IntegerField('预计时长(分钟)', [Optional(), NumberRange(min=1, max=1440)], default=30)
    difficulty = SelectField('难度', [Optional()], choices=[
        ('easy', '简单'),
        ('medium', '中等'),
        ('hard', '困难')
    ], default='medium')
    category = StringField('测评分类', [Optional(), Length(0, 50)])
    status = SelectField('状态', [Optional()], choices=[
        ('draft', '草稿'),
        ('published', '已发布'),
        ('archived', '已归档')
    ], default='draft')
    tags = StringField('标签', [Optional()])  # 逗号分隔的字符串
    instructions = TextAreaField('测评说明', [Optional()])
    is_free = BooleanField('是否免费', [Optional()], default=True)
    sort_order = IntegerField('排序', [Optional()], default=0)


class AssessmentUpdateForm(BaseForm):
    """更新测评表单"""
    name = StringField('测评名称', [Optional(), Length(1, 200)])
    subtitle = StringField('测评副标题', [Optional(), Length(0, 300)])
    description = TextAreaField('测评描述', [Optional()])
    cover_image = StringField('封面图片', [Optional(), Length(0, 255)])
    price = FloatField('价格', [Optional(), NumberRange(min=0)])
    original_price = FloatField('原价', [Optional(), NumberRange(min=0)])
    duration = IntegerField('预计时长(分钟)', [Optional(), NumberRange(min=1, max=1440)])
    difficulty = SelectField('难度', [Optional()], choices=[
        ('easy', '简单'),
        ('medium', '中等'),
        ('hard', '困难')
    ])
    category = StringField('测评分类', [Optional(), Length(0, 50)])
    status = SelectField('状态', [Optional()], choices=[
        ('draft', '草稿'),
        ('published', '已发布'),
        ('archived', '已归档')
    ])
    tags = StringField('标签', [Optional()])  # 逗号分隔的字符串
    instructions = TextAreaField('测评说明', [Optional()])
    is_free = BooleanField('是否免费', [Optional()])
    sort_order = IntegerField('排序', [Optional()])


class AssessmentOptionForm(BaseForm):
    """测评选项表单"""
    option_text = StringField('选项内容', [DataRequired(), Length(1, 500)])
    option_value = StringField('选项值', [Optional(), Length(0, 50)])
    score = FloatField('选项分值', [Optional()], default=0.0)
    option_order = IntegerField('选项序号', [Optional()], default=0)


class AssessmentQuestionForm(BaseForm):
    """测评题目表单"""
    question_text = TextAreaField('题目内容', [DataRequired()])
    question_type = SelectField('题目类型', [DataRequired()], choices=[
        ('single', '单选'),
        ('multiple', '多选'),
        ('text', '文本'),
        ('scale', '量表')
    ], default='single')
    question_order = IntegerField('题目序号', [Optional()], default=0)
    is_required = BooleanField('是否必答', [Optional()], default=True)
    score_weight = FloatField('分值权重', [Optional(), NumberRange(min=0)], default=1.0)
    dimension = StringField('维度标识', [Optional(), Length(0, 50)])
    description = TextAreaField('题目说明', [Optional()])
    options = FieldList(FormField(AssessmentOptionForm), min_entries=0)


class AssessmentQuestionCreateForm(BaseForm):
    """创建测评题目表单"""
    assessment_id = StringField('测评ID', [DataRequired(), Length(1, 50)])
    question_text = TextAreaField('题目内容', [DataRequired()])
    question_type = SelectField('题目类型', [DataRequired()], choices=[
        ('single', '单选'),
        ('multiple', '多选'),
        ('text', '文本'),
        ('scale', '量表')
    ], default='single')
    question_order = IntegerField('题目序号', [Optional()], default=0)
    is_required = BooleanField('是否必答', [Optional()], default=True)
    score_weight = FloatField('分值权重', [Optional(), NumberRange(min=0)], default=1.0)
    dimension = StringField('维度标识', [Optional(), Length(0, 50)])
    description = TextAreaField('题目说明', [Optional()])


class AssessmentQuestionUpdateForm(BaseForm):
    """更新测评题目表单"""
    question_text = TextAreaField('题目内容', [Optional()])
    question_type = SelectField('题目类型', [Optional()], choices=[
        ('single', '单选'),
        ('multiple', '多选'),
        ('text', '文本'),
        ('scale', '量表')
    ])
    question_order = IntegerField('题目序号', [Optional()])
    is_required = BooleanField('是否必答', [Optional()])
    score_weight = FloatField('分值权重', [Optional(), NumberRange(min=0)])
    dimension = StringField('维度标识', [Optional(), Length(0, 50)])
    description = TextAreaField('题目说明', [Optional()])


class AssessmentAnswerForm(BaseForm):
    """测评答案表单"""
    question_id = StringField('题目ID', [DataRequired(), Length(1, 50)])
    option_ids = StringField('选项ID列表', [Optional()])  # JSON字符串
    answer_text = TextAreaField('文本答案', [Optional()])


class AssessmentSubmitForm(BaseForm):
    """提交测评表单"""
    assessment_id = StringField('测评ID', [DataRequired(), Length(1, 50)])
    answers = FieldList(FormField(AssessmentAnswerForm), min_entries=1)
    is_anonymous = BooleanField('是否匿名', [Optional()], default=False)


class AssessmentRecordQueryForm(BaseForm):
    """测评记录查询表单"""
    page = IntegerField('页码', [Optional()], default=1)
    per_page = IntegerField('每页数量', [Optional()], default=10)
    user_id = StringField('用户ID', [Optional()])
    assessment_id = StringField('测评ID', [Optional()])
    status = SelectField('状态', [Optional()], choices=[
        ('', '全部'),
        ('in_progress', '进行中'),
        ('completed', '已完成'),
        ('expired', '已过期')
    ], default='')
    start_date = StringField('开始日期', [Optional()])  # YYYY-MM-DD格式
    end_date = StringField('结束日期', [Optional()])  # YYYY-MM-DD格式
    sort_by = StringField('排序字段', [Optional()], default='create_time')
    sort_order = StringField('排序方向', [Optional()], default='desc')


class AssessmentStartForm(BaseForm):
    """开始测评表单"""
    assessment_id = StringField('测评ID', [DataRequired(), Length(1, 50)])
    is_anonymous = BooleanField('是否匿名', [Optional()], default=False) 