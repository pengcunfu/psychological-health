"""
通用数据模块
创建咨询师、咨询人等业务数据
"""
import click
import uuid
from pcf_flask_helper.model.base import db
from psychological.appointment.models.counselor import Counselor
from psychological.appointment.models.consultant import Consultant, GenderEnum, RelationshipEnum
from psychological.system.models.user import User


def create_counselors() -> None:
    """创建示例咨询师数据"""
    # 检查是否已有咨询师数据，如果有则跳过
    existing_count = db.session.query(Counselor).count()
    if existing_count > 0:
        click.echo(f'   警告: 系统中已存在 {existing_count} 个咨询师，跳过咨询师创建')
        return
    
    counselors_data = [
        {
            'name': '张心理',
            'title': '主任医师',
            'phone': '13800138001',
            'email': 'zhang@example.com',
            'specialty': '焦虑症、抑郁症、强迫症治疗',
            'bio': '从事心理咨询工作15年，擅长认知行为疗法和心理动力学治疗。具有丰富的临床经验，帮助过数千名患者重获心理健康。',
            'price': 300.0,
            'rating': 4.8,
            'consultation_count': 1250,
            'tags': ['焦虑症', '抑郁症', '强迫症', '认知行为疗法'],
            'introduction': '资深心理咨询师，专业、耐心、负责',
            'status': 1
        },
        {
            'name': '李咨询',
            'title': '副主任医师',
            'phone': '13800138002',
            'email': 'li@example.com',
            'specialty': '婚姻家庭治疗、青少年心理咨询',
            'bio': '心理学博士，专注于家庭治疗和青少年心理健康。擅长处理家庭关系问题、亲子沟通障碍等。温和耐心的咨询风格深受来访者喜爱。',
            'price': 250.0,
            'rating': 4.7,
            'consultation_count': 890,
            'tags': ['婚姻家庭', '青少年心理', '亲子关系', '家庭治疗'],
            'introduction': '家庭治疗专家，关注青少年心理健康',
            'status': 1
        },
        {
            'name': '王医生',
            'title': '主治医师',
            'phone': '13800138003',
            'email': 'wang@example.com',
            'specialty': '创伤后应激障碍、睡眠障碍',
            'bio': '心理创伤治疗专家，在PTSD治疗方面有独特见解。运用EMDR等先进疗法帮助患者走出心理阴霾。同时在睡眠障碍治疗方面经验丰富。',
            'price': 280.0,
            'rating': 4.9,
            'consultation_count': 650,
            'tags': ['PTSD', '创伤治疗', '睡眠障碍', 'EMDR'],
            'introduction': '创伤治疗专家，EMDR认证治疗师',
            'status': 1
        },
        {
            'name': '陈主任',
            'title': '主任医师',
            'phone': '13800138004',
            'email': 'chen@example.com',
            'specialty': '职场心理、压力管理',
            'bio': '企业心理健康顾问，专注于职场心理问题的解决。帮助职场人士处理工作压力、人际关系、职业发展等问题。',
            'price': 320.0,
            'rating': 4.6,
            'consultation_count': 780,
            'tags': ['职场心理', '压力管理', '人际关系', '职业发展'],
            'introduction': '职场心理专家，企业EAP顾问',
            'status': 1
        },
        {
            'name': '刘博士',
            'title': '副主任医师',
            'phone': '13800138005',
            'email': 'liu@example.com',
            'specialty': '儿童心理、学习障碍',
            'bio': '儿童心理学专家，专门从事儿童心理发展和学习障碍的研究与治疗。善于与儿童建立良好的治疗关系。',
            'price': 260.0,
            'rating': 4.8,
            'consultation_count': 520,
            'tags': ['儿童心理', '学习障碍', '注意力缺陷', '自闭症'],
            'introduction': '儿童心理专家，关爱每一个孩子的成长',
            'status': 1
        }
    ]
    
    created_counselors = []
    for counselor_data in counselors_data:
        # 检查是否已存在
        existing = db.session.query(Counselor).filter_by(name=counselor_data['name']).first()
        if existing:
            click.echo(f'   警告: 咨询师 "{counselor_data["name"]}" 已存在，跳过创建')
            continue
            
        counselor = Counselor(
            id=str(uuid.uuid4()),
            name=counselor_data['name'],
            title=counselor_data['title'],
            phone=counselor_data['phone'],
            email=counselor_data['email'],
            specialty=counselor_data['specialty'],
            bio=counselor_data['bio'],
            price=counselor_data['price'],
            rating=counselor_data['rating'],
            consultation_count=counselor_data['consultation_count'],
            introduction=counselor_data['introduction'],
            status=counselor_data['status']
        )
        counselor.tags = counselor_data['tags']
        
        db.session.add(counselor)
        created_counselors.append(counselor)
        click.echo(f'   创建咨询师: {counselor_data["name"]} ({counselor_data["title"]})')
    
    click.echo(f'\n咨询师创建完成！')
    click.echo(f'咨询师: {len(created_counselors)} 个')
    
    # 显示咨询师信息
    if created_counselors:
        click.echo('\n咨询师列表:')
        for counselor in created_counselors:
            click.echo(f'   • {counselor.name} - {counselor.title} (¥{counselor.price}/小时)')
    


def create_consultants() -> None:
    """创建示例咨询人数据"""
    # 检查是否已有咨询人数据，如果有则跳过
    existing_count = db.session.query(Consultant).count()
    if existing_count > 0:
        click.echo(f'   警告: 系统中已存在 {existing_count} 个咨询人，跳过咨询人创建')
        return
    
    # 获取一些用户ID作为关联
    users = db.session.query(User).limit(3).all()
    user_ids = [user.id for user in users] if users else [None, None, None]
    
    consultants_data = [
        {
            'user_id': user_ids[0],
            'real_name': '张小明',
            'birth_year': 1990,
            'birth_month': 5,
            'gender': GenderEnum.MALE,
            'phone': '13900139001',
            'emergency_name': '张父',
            'emergency_relationship': RelationshipEnum.PARENT,
            'emergency_phone': '13900139002',
            'notes': '工作压力大，经常失眠',
            'is_default': 1,
            'status': 1
        },
        {
            'user_id': user_ids[1],
            'real_name': '李小红',
            'birth_year': 1985,
            'birth_month': 8,
            'gender': GenderEnum.FEMALE,
            'phone': '13900139003',
            'emergency_name': '李母',
            'emergency_relationship': RelationshipEnum.PARENT,
            'emergency_phone': '13900139004',
            'notes': '婚姻关系问题，需要情感咨询',
            'is_default': 0,
            'status': 1
        },
        {
            'user_id': user_ids[2],
            'real_name': '王小华',
            'birth_year': 1995,
            'birth_month': 12,
            'gender': GenderEnum.MALE,
            'phone': '13900139005',
            'emergency_name': '王朋友',
            'emergency_relationship': RelationshipEnum.FRIEND,
            'emergency_phone': '13900139006',
            'notes': '社交恐惧，希望改善人际关系',
            'is_default': 0,
            'status': 1
        },
        {
            'user_id': None,
            'real_name': '陈小丽',
            'birth_year': 1988,
            'birth_month': 3,
            'gender': GenderEnum.FEMALE,
            'phone': '13900139007',
            'emergency_name': '陈姐姐',
            'emergency_relationship': RelationshipEnum.SIBLING,
            'emergency_phone': '13900139008',
            'notes': '产后抑郁，需要专业帮助',
            'is_default': 0,
            'status': 1
        }
    ]
    
    created_consultants = []
    for consultant_data in consultants_data:
        # 检查是否已存在
        existing = db.session.query(Consultant).filter_by(
            real_name=consultant_data['real_name'],
            phone=consultant_data['phone']
        ).first()
        if existing:
            click.echo(f'   警告: 咨询人 "{consultant_data["real_name"]}" 已存在，跳过创建')
            continue
            
        consultant = Consultant(
            id=str(uuid.uuid4()),
            user_id=consultant_data['user_id'],
            real_name=consultant_data['real_name'],
            birth_year=consultant_data['birth_year'],
            birth_month=consultant_data['birth_month'],
            gender=consultant_data['gender'],
            phone=consultant_data['phone'],
            emergency_name=consultant_data['emergency_name'],
            emergency_relationship=consultant_data['emergency_relationship'],
            emergency_phone=consultant_data['emergency_phone'],
            notes=consultant_data['notes'],
            is_default=consultant_data['is_default'],
            status=consultant_data['status']
        )
        
        db.session.add(consultant)
        created_consultants.append(consultant)
        click.echo(f'   创建咨询人: {consultant_data["real_name"]} ({consultant_data["gender"].value})')
    
    click.echo(f'\n咨询人创建完成！')
    click.echo(f'咨询人: {len(created_consultants)} 个')
    
    # 显示咨询人信息
    if created_consultants:
        click.echo('\n咨询人列表:')
        for consultant in created_consultants:
            click.echo(f'   • {consultant.real_name} - {consultant.gender.value} ({consultant.phone})')
    
