"""
文件上传API
"""
import os
import uuid
from flask import Blueprint, request, jsonify, current_app
from werkzeug.exceptions import RequestEntityTooLarge
from werkzeug.utils import secure_filename
from psychological.utils.file_upload import FileUploader
from psychological.utils.json_result import JsonResult

# 创建蓝图
file_upload_bp = Blueprint('upload', __name__, url_prefix='/upload')


@file_upload_bp.route('', methods=['POST'])
def upload_file():
    """
    文件上传接口
    支持的参数:
    - file: 上传的文件
    - file_type: 文件类型限制 (image, document, audio, video, archive)
    - use_unique_name: 是否使用唯一文件名 (默认true)
    """
    try:
        # 检查是否有文件
        if 'file' not in request.files:
            return JsonResult.error('没有选择文件')

        file = request.files['file']
        if file.filename == '':
            return JsonResult.error('没有选择文件')

        # 获取参数
        file_type = request.form.get('file_type')
        use_unique_name = request.form.get(
            'use_unique_name', 'true').lower() == 'true'

        # 保存文件
        uploader = FileUploader(
            upload_dir=os.path.join(current_app.root_path, 'uploads'),
            static_dir=os.path.join(current_app.root_path, 'static')
        )
        file_info = uploader.save(
            file=file,
            file_type=file_type,
            use_unique_name=use_unique_name
        )

        return JsonResult.success(file_info, '文件上传成功')

    except ValueError as e:
        return JsonResult.error(str(e))
    except RequestEntityTooLarge:
        return JsonResult.error('文件大小超过限制')
    except Exception as e:
        return JsonResult.error(f'上传失败: {str(e)}')


@file_upload_bp.route('/avatar', methods=['POST'])
def upload_avatar():
    """
    上传头像接口
    将头像保存到 static/uploads/avatar 目录
    使用 UUID + 原文件后缀名作为文件名
    支持的图片格式: jpg, jpeg, png, gif, webp
    """
    try:
        # 检查是否有文件
        if 'file' not in request.files:
            return JsonResult.error('没有选择文件')

        file = request.files['file']
        if file.filename == '':
            return JsonResult.error('没有选择文件')

        # 获取原文件名和后缀
        # original_filename = secure_filename(file.filename)
        original_filename = file.filename
        if '.' not in original_filename:
            return JsonResult.error('文件必须包含后缀名')

        file_ext = original_filename.rsplit('.', 1)[1].lower()

        # 检查文件类型（仅允许图片）
        allowed_extensions = {'jpg', 'jpeg', 'png', 'gif', 'webp'}
        if file_ext not in allowed_extensions:
            return JsonResult.error(f'不支持的文件格式，仅支持: {", ".join(allowed_extensions)}')

        # 生成唯一文件名：UUID + 后缀
        unique_filename = f"{str(uuid.uuid4())}.{file_ext}"

        # 确保目录存在
        avatar_dir = os.path.join(
            current_app.root_path, 'static', 'uploads', 'avatar')
        os.makedirs(avatar_dir, exist_ok=True)

        # 保存文件
        file_path = os.path.join(avatar_dir, unique_filename)
        file.save(file_path)

        # 生成可访问的URL路径
        url_path = f"/static/uploads/avatar/{unique_filename}"

        # 返回文件信息
        file_info = {
            'filename': unique_filename,
            'original_filename': original_filename,
            'url': url_path,
            'file_size': os.path.getsize(file_path),
            'file_type': file_ext,
            'upload_path': f"uploads/avatar/{unique_filename}"
        }

        return JsonResult.success(file_info, '头像上传成功')

    except ValueError as e:
        return JsonResult.error(str(e))
    except RequestEntityTooLarge:
        return JsonResult.error('文件大小超过限制')
    except Exception as e:
        return JsonResult.error(f'上传失败: {str(e)}')


@file_upload_bp.route('/banner', methods=['POST'])
def upload_banner():
    """
    上传横幅图接口
    将横幅图保存到 static/uploads/banner 目录
    使用 UUID + 原文件后缀名作为文件名
    支持的图片格式: jpg, jpeg, png, gif, webp
    """
    try:
        # 检查是否有文件
        if 'file' not in request.files:
            return JsonResult.error('没有选择文件')

        file = request.files['file']
        if file.filename == '':
            return JsonResult.error('没有选择文件')

        # 获取原文件名和后缀
        # original_filename = secure_filename(file.filename)
        original_filename = file.filename
        if '.' not in original_filename:
            return JsonResult.error('文件必须包含后缀名')

        file_ext = original_filename.rsplit('.', 1)[1].lower()

        # 检查文件类型（仅允许图片）
        allowed_extensions = {'jpg', 'jpeg', 'png', 'gif', 'webp'}
        if file_ext not in allowed_extensions:
            return JsonResult.error(f'不支持的文件格式，仅支持: {", ".join(allowed_extensions)}')

        # 生成唯一文件名：UUID + 后缀
        unique_filename = f"{str(uuid.uuid4())}.{file_ext}"

        # 确保目录存在
        banner_dir = os.path.join(
            current_app.root_path, 'static', 'uploads', 'banner')
        os.makedirs(banner_dir, exist_ok=True)

        # 保存文件
        file_path = os.path.join(banner_dir, unique_filename)
        file.save(file_path)

        # 生成可访问的URL路径
        url_path = f"/static/uploads/banner/{unique_filename}"

        # 返回文件信息
        file_info = {
            'filename': unique_filename,
            'original_filename': original_filename,
            'url': url_path,
            'file_size': os.path.getsize(file_path),
            'file_type': file_ext,
            'upload_path': f"uploads/banner/{unique_filename}"
        }

        return JsonResult.success(file_info, '横幅图上传成功')

    except ValueError as e:
        return JsonResult.error(str(e))
    except RequestEntityTooLarge:
        return JsonResult.error('文件大小超过限制')
    except Exception as e:
        return JsonResult.error(f'上传失败: {str(e)}')


@file_upload_bp.route('/course-cover', methods=['POST'])
def upload_course_cover():
    """
    上传课程封面接口
    将课程封面保存到 static/uploads/course_cover 目录
    使用 UUID + 原文件后缀名作为文件名
    支持的图片格式: jpg, jpeg, png, gif, webp
    """
    try:
        # 检查是否有文件
        if 'file' not in request.files:
            return JsonResult.error('没有选择文件')

        file = request.files['file']
        if file.filename == '':
            return JsonResult.error('没有选择文件')

        # 获取原文件名和后缀
        original_filename = file.filename
        if '.' not in original_filename:
            return JsonResult.error('文件必须包含后缀名')

        file_ext = original_filename.rsplit('.', 1)[1].lower()

        # 检查文件类型（仅允许图片）
        allowed_extensions = {'jpg', 'jpeg', 'png', 'gif', 'webp'}
        if file_ext not in allowed_extensions:
            return JsonResult.error(f'不支持的文件格式，仅支持: {", ".join(allowed_extensions)}')

        # 生成唯一文件名：UUID + 后缀
        unique_filename = f"{str(uuid.uuid4())}.{file_ext}"

        # 确保目录存在
        course_cover_dir = os.path.join(
            current_app.root_path, 'static', 'uploads', 'course_cover')
        os.makedirs(course_cover_dir, exist_ok=True)

        # 保存文件
        file_path = os.path.join(course_cover_dir, unique_filename)
        file.save(file_path)

        # 生成可访问的URL路径
        url_path = f"/static/uploads/course_cover/{unique_filename}"

        # 返回文件信息
        file_info = {
            'filename': unique_filename,
            'original_filename': original_filename,
            'url': url_path,
            'file_size': os.path.getsize(file_path),
            'file_type': file_ext,
            'upload_path': f"uploads/course_cover/{unique_filename}"
        }

        return JsonResult.success(file_info, '课程封面上传成功')

    except ValueError as e:
        return JsonResult.error(str(e))
    except RequestEntityTooLarge:
        return JsonResult.error('文件大小超过限制')
    except Exception as e:
        return JsonResult.error(f'上传失败: {str(e)}')


@file_upload_bp.route('/course-video', methods=['POST'])
def upload_course_video():
    """
    上传课程视频接口
    将课程视频保存到 static/uploads/course_video 目录
    使用 UUID + 原文件后缀名作为文件名
    支持的视频格式: mp4, avi, mov, wmv, flv, mkv, webm
    """
    try:
        # 检查是否有文件
        if 'file' not in request.files:
            return JsonResult.error('没有选择文件')

        file = request.files['file']
        if file.filename == '':
            return JsonResult.error('没有选择文件')

        # 获取原文件名和后缀
        original_filename = file.filename
        if '.' not in original_filename:
            return JsonResult.error('文件必须包含后缀名')

        file_ext = original_filename.rsplit('.', 1)[1].lower()

        # 检查文件类型（仅允许视频）
        allowed_extensions = {'mp4', 'avi', 'mov', 'wmv', 'flv', 'mkv', 'webm'}
        if file_ext not in allowed_extensions:
            return JsonResult.error(f'不支持的文件格式，仅支持: {", ".join(allowed_extensions)}')

        # 生成唯一文件名：UUID + 后缀
        unique_filename = f"{str(uuid.uuid4())}.{file_ext}"

        # 确保目录存在
        course_video_dir = os.path.join(
            current_app.root_path, 'static', 'uploads', 'course_video')
        os.makedirs(course_video_dir, exist_ok=True)

        # 保存文件
        file_path = os.path.join(course_video_dir, unique_filename)
        file.save(file_path)

        # 生成可访问的URL路径
        url_path = f"/static/uploads/course_video/{unique_filename}"

        # 返回文件信息
        file_info = {
            'filename': unique_filename,
            'original_filename': original_filename,
            'url': url_path,
            'file_size': os.path.getsize(file_path),
            'file_type': file_ext,
            'upload_path': f"uploads/course_video/{unique_filename}"
        }

        return JsonResult.success(file_info, '课程视频上传成功')

    except ValueError as e:
        return JsonResult.error(str(e))
    except RequestEntityTooLarge:
        return JsonResult.error('文件大小超过限制')
    except Exception as e:
        return JsonResult.error(f'上传失败: {str(e)}')


@file_upload_bp.route('/assessment', methods=['POST'])
def upload_assessment():
    """
    上传测评封面接口
    将测评封面保存到 static/uploads/assessment 目录
    使用 UUID + 原文件后缀名作为文件名
    支持的图片格式: jpg, jpeg, png, gif, webp
    """
    try:
        # 检查是否有文件
        if 'file' not in request.files:
            return JsonResult.error('没有选择文件')

        file = request.files['file']
        if file.filename == '':
            return JsonResult.error('没有选择文件')

        # 获取原文件名和后缀
        original_filename = file.filename
        if '.' not in original_filename:
            return JsonResult.error('文件必须包含后缀名')

        file_ext = original_filename.rsplit('.', 1)[1].lower()

        # 检查文件类型（仅允许图片）
        allowed_extensions = {'jpg', 'jpeg', 'png', 'gif', 'webp'}
        if file_ext not in allowed_extensions:
            return JsonResult.error(f'不支持的文件格式，仅支持: {", ".join(allowed_extensions)}')

        # 生成唯一文件名：UUID + 后缀
        unique_filename = f"{str(uuid.uuid4())}.{file_ext}"

        # 确保目录存在
        assessment_dir = os.path.join(
            current_app.root_path, 'static', 'uploads', 'assessment')
        os.makedirs(assessment_dir, exist_ok=True)

        # 保存文件
        file_path = os.path.join(assessment_dir, unique_filename)
        file.save(file_path)

        # 生成可访问的URL路径
        url_path = f"/static/uploads/assessment/{unique_filename}"

        # 返回文件信息
        file_info = {
            'filename': unique_filename,
            'original_filename': original_filename,
            'url': url_path,
            'file_size': os.path.getsize(file_path),
            'file_type': file_ext,
            'upload_path': f"uploads/assessment/{unique_filename}"
        }

        return JsonResult.success(file_info, '测评封面上传成功')

    except ValueError as e:
        return JsonResult.error(str(e))
    except RequestEntityTooLarge:
        return JsonResult.error('文件大小超过限制')
    except Exception as e:
        return JsonResult.error(f'上传失败: {str(e)}')
