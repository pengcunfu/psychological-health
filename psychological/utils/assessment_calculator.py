import json
from typing import Dict, Tuple
from psychological.models import AssessmentQuestion, AssessmentOption, AssessmentRecord, AssessmentAnswer


class AssessmentCalculator:
    """心理测评结果计算器"""

    @staticmethod
    def calculate_score(record_id: str) -> Dict:
        """
        计算测评得分
        :param record_id: 测评记录ID
        :return: 计算结果字典
        """
        record = AssessmentRecord.query.filter_by(id=record_id).first()
        if not record:
            raise ValueError("测评记录不存在")

        assessment = record.assessment
        if not assessment:
            raise ValueError("测评模板不存在")

        answers = AssessmentAnswer.query.filter_by(record_id=record_id).all()

        total_score = 0.0
        max_possible_score = 0.0
        dimension_scores = {}
        dimension_max_scores = {}
        question_scores = {}

        # 获取所有题目
        questions = AssessmentQuestion.query.filter_by(
            assessment_id=assessment.id).all()
        question_dict = {q.id: q for q in questions}

        # 计算每个题目的最大可能得分
        for question in questions:
            max_options_score = 0.0
            options = AssessmentOption.query.filter_by(
                question_id=question.id).all()

            if question.question_type == 'single':
                # 单选题取最大分值选项
                max_options_score = max(
                    [opt.score for opt in options]) if options else 0.0
            elif question.question_type == 'multiple':
                # 多选题取所有选项分值之和
                max_options_score = sum([opt.score for opt in options])
            elif question.question_type == 'scale':
                # 量表题取最大分值选项
                max_options_score = max(
                    [opt.score for opt in options]) if options else 0.0

            question_max_score = max_options_score * question.score_weight
            max_possible_score += question_max_score

            # 维度最大得分
            if question.dimension:
                if question.dimension not in dimension_max_scores:
                    dimension_max_scores[question.dimension] = 0.0
                dimension_max_scores[question.dimension] += question_max_score

        # 计算实际得分
        for answer in answers:
            question = question_dict.get(answer.question_id)
            if not question:
                continue

            question_score = 0.0

            # 根据选项计算得分
            if answer.selected_options:
                options = AssessmentOption.query.filter(
                    AssessmentOption.id.in_(answer.selected_options)
                ).all()
                question_score = sum(
                    [opt.score for opt in options]) * question.score_weight

            # 更新答案得分
            answer.score = question_score
            total_score += question_score
            question_scores[question.id] = question_score

            # 维度得分统计
            if question.dimension:
                if question.dimension not in dimension_scores:
                    dimension_scores[question.dimension] = 0.0
                dimension_scores[question.dimension] += question_score

        # 计算维度得分百分比
        dimension_percentages = {}
        for dimension, score in dimension_scores.items():
            max_score = dimension_max_scores.get(dimension, 1.0)
            dimension_percentages[dimension] = (
                score / max_score * 100) if max_score > 0 else 0

        return {
            'total_score': total_score,
            'max_score': max_possible_score,
            'percentage': (total_score / max_possible_score * 100) if max_possible_score > 0 else 0,
            'dimension_scores': dimension_scores,
            'dimension_max_scores': dimension_max_scores,
            'dimension_percentages': dimension_percentages,
            'question_scores': question_scores
        }

    @staticmethod
    def get_result_level(score_percentage: float, assessment_type: str = 'general') -> Tuple[str, str, str]:
        """
        根据得分百分比获取结果等级
        :param score_percentage: 得分百分比
        :param assessment_type: 测评类型
        :return: (等级, 描述, 建议)
        """
        if assessment_type == 'depression':
            # 抑郁测评
            if score_percentage <= 25:
                return 'minimal', '无明显抑郁症状', '保持良好的生活习惯，继续关注心理健康。'
            elif score_percentage <= 50:
                return 'mild', '轻度抑郁倾向', '建议适当放松，增加社交活动，如症状持续建议咨询专业人士。'
            elif score_percentage <= 75:
                return 'moderate', '中度抑郁症状', '建议尽快寻求专业心理咨询师的帮助，调整生活方式。'
            else:
                return 'severe', '重度抑郁症状', '强烈建议立即寻求专业医生或心理治疗师的帮助。'

        elif assessment_type == 'anxiety':
            # 焦虑测评
            if score_percentage <= 30:
                return 'minimal', '无明显焦虑症状', '心理状态良好，继续保持积极的生活态度。'
            elif score_percentage <= 55:
                return 'mild', '轻度焦虑', '建议学习放松技巧，如深呼吸、冥想等。'
            elif score_percentage <= 75:
                return 'moderate', '中度焦虑', '建议寻求专业心理咨询，学习应对焦虑的方法。'
            else:
                return 'severe', '重度焦虑', '建议立即咨询心理健康专家，必要时寻求药物治疗。'

        elif assessment_type == 'stress':
            # 压力测评
            if score_percentage <= 35:
                return 'low', '压力水平较低', '当前状态良好，继续保持工作生活平衡。'
            elif score_percentage <= 60:
                return 'moderate', '中等压力水平', '建议合理安排时间，增加休息和娱乐活动。'
            elif score_percentage <= 80:
                return 'high', '较高压力水平', '建议主动寻求支持，调整工作节奏，学习压力管理技巧。'
            else:
                return 'extreme', '极高压力水平', '建议立即采取措施减压，必要时寻求专业帮助。'

        else:
            # 通用测评
            if score_percentage <= 40:
                return 'poor', '需要改善', '建议关注相关方面的发展，寻求适当的帮助和指导。'
            elif score_percentage <= 60:
                return 'fair', '一般水平', '在正常范围内，可以通过努力进一步提升。'
            elif score_percentage <= 80:
                return 'good', '良好水平', '表现不错，继续保持并适当提升。'
            else:
                return 'excellent', '优秀水平', '表现优异，继续保持当前的良好状态。'

    @staticmethod
    def generate_detailed_report(record_id: str) -> Dict:
        """
        生成详细的测评报告
        :param record_id: 测评记录ID
        :return: 详细报告字典
        """
        record = AssessmentRecord.query.filter_by(id=record_id).first()
        if not record:
            raise ValueError("测评记录不存在")

        assessment = record.assessment
        calculation_result = AssessmentCalculator.calculate_score(record_id)

        # 获取结果等级
        level, description, suggestion = AssessmentCalculator.get_result_level(
            calculation_result['percentage'],
            assessment.category or 'general'
        )

        # 生成维度分析
        dimension_analysis = []
        for dimension, percentage in calculation_result['dimension_percentages'].items():
            dim_level, dim_desc, dim_suggestion = AssessmentCalculator.get_result_level(
                percentage, f"{assessment.category}_{dimension}" if assessment.category else dimension
            )

            dimension_analysis.append({
                'dimension': dimension,
                'score': calculation_result['dimension_scores'][dimension],
                'max_score': calculation_result['dimension_max_scores'][dimension],
                'percentage': percentage,
                'level': dim_level,
                'description': dim_desc,
                'suggestion': dim_suggestion
            })

        # 生成改进建议
        improvement_suggestions = []
        for dim in dimension_analysis:
            if dim['percentage'] < 60:  # 低于60%的维度需要改进
                improvement_suggestions.append({
                    'dimension': dim['dimension'],
                    'current_level': dim['level'],
                    'suggestion': dim['suggestion'],
                    'priority': 'high' if dim['percentage'] < 40 else 'medium'
                })

        return {
            'record_id': record_id,
            'assessment_name': assessment.name,
            'total_score': calculation_result['total_score'],
            'max_score': calculation_result['max_score'],
            'percentage': calculation_result['percentage'],
            'overall_level': level,
            'overall_description': description,
            'overall_suggestion': suggestion,
            'dimension_analysis': dimension_analysis,
            'improvement_suggestions': improvement_suggestions,
            'completion_time': record.complete_time.isoformat() if record.complete_time else None,
            'test_duration': None  # 可以根据开始和结束时间计算
        }

    @staticmethod
    def compare_records(record_id1: str, record_id2: str) -> Dict:
        """
        比较两次测评记录
        :param record_id1: 第一次测评记录ID
        :param record_id2: 第二次测评记录ID
        :return: 比较结果
        """
        result1 = AssessmentCalculator.calculate_score(record_id1)
        result2 = AssessmentCalculator.calculate_score(record_id2)

        record1 = AssessmentRecord.query.filter_by(id=record_id1).first()
        record2 = AssessmentRecord.query.filter_by(id=record_id2).first()

        if not record1 or not record2:
            raise ValueError("测评记录不存在")

        if record1.assessment_id != record2.assessment_id:
            raise ValueError("不同测评无法比较")

        # 计算变化
        score_change = result2['total_score'] - result1['total_score']
        percentage_change = result2['percentage'] - result1['percentage']

        # 维度变化
        dimension_changes = {}
        for dimension in result1['dimension_scores']:
            if dimension in result2['dimension_scores']:
                dimension_changes[dimension] = {
                    'score_change': result2['dimension_scores'][dimension] - result1['dimension_scores'][dimension],
                    'percentage_change': result2['dimension_percentages'][dimension] - result1['dimension_percentages'][dimension]
                }

        return {
            'assessment_name': record1.assessment.name,
            'first_test': {
                'date': record1.complete_time.isoformat() if record1.complete_time else None,
                'score': result1['total_score'],
                'percentage': result1['percentage']
            },
            'second_test': {
                'date': record2.complete_time.isoformat() if record2.complete_time else None,
                'score': result2['total_score'],
                'percentage': result2['percentage']
            },
            'overall_change': {
                'score_change': score_change,
                'percentage_change': percentage_change,
                'improvement': percentage_change > 0
            },
            'dimension_changes': dimension_changes
        }
