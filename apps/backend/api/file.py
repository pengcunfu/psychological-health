"""
文件上传API
提供文件上传、下载和管理功能

接口列表：
- POST /upload - 上传文件
- POST /upload/image - 上传图片
- POST /upload/avatar - 上传头像
- POST /upload/document - 上传文档
- GET /file/<file_id> - 获取文件信息
- GET /file/download/<file_id> - 下载文件
- DELETE /file/<file_id> - 删除文件
- GET /file/list - 获取文件列表
"""
from flask import Blueprint, request, jsonify, current_app
from werkzeug.exceptions import RequestEntityTooLarge
from utils.file_upload import FileUploader
from utils.json_result import JsonResult
import os

# 创建蓝图
file_upload_bp = Blueprint('file_upload', __name__, url_prefix='/file')


# 文件上传器将在请求中动态创建
def get_file_uploader():
    """获取文件上传器实例"""
    return FileUploader(
        upload_dir=os.path.join(current_app.root_path, 'uploads'),
        static_dir=os.path.join(current_app.root_path, 'static')
    )


@file_upload_bp.route('/upload', methods=['POST'])
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
        use_unique_name = request.form.get('use_unique_name', 'true').lower() == 'true'

        # 保存文件
        uploader = get_file_uploader()
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


@file_upload_bp.route('/upload-to-static', methods=['POST'])
def upload_to_static():
    """
    上传文件到static目录，可直接通过URL访问
    支持的参数:
    - file: 上传的文件
    - subfolder: 子文件夹名称 (默认uploads)
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
        subfolder = request.form.get('subfolder', 'uploads')
        use_unique_name = request.form.get('use_unique_name', 'true').lower() == 'true'

        # 保存文件到static目录
        uploader = get_file_uploader()
        file_info = uploader.save_to_static(
            file=file,
            subfolder=subfolder,
            use_unique_name=use_unique_name
        )

        return JsonResult.success(file_info, '文件上传成功')

    except ValueError as e:
        return JsonResult.error(str(e))
    except Exception as e:
        return JsonResult.error(f'上传失败: {str(e)}')


@file_upload_bp.route('/download/<path:file_path>')
def download_file(file_path):
    """
    文件下载接口
    :param file_path: 文件相对路径
    """
    try:
        # 构建完整文件路径
        full_path = os.path.join(current_app.root_path, 'uploads', file_path)

        # 获取下载名称
        download_name = request.args.get('name')
        as_attachment = request.args.get('attachment', 'true').lower() == 'true'

        uploader = get_file_uploader()
        return uploader.download_file(
            file_path=full_path,
            as_attachment=as_attachment,
            download_name=download_name
        )

    except Exception as e:
        return JsonResult.error(f'下载失败: {str(e)}')


@file_upload_bp.route('/info/<path:file_path>')
def get_file_info(file_path):
    """
    获取文件信息
    :param file_path: 文件相对路径
    """
    try:
        # 构建完整文件路径
        full_path = os.path.join(current_app.root_path, 'uploads', file_path)

        uploader = get_file_uploader()
        file_info = uploader.get_file_info(full_path)
        if file_info:
            return JsonResult.success(file_info)
        else:
            return JsonResult.error('文件不存在')

    except Exception as e:
        return JsonResult.error(f'获取文件信息失败: {str(e)}')


@file_upload_bp.route('/list')
def list_files():
    """
    列出上传目录中的文件
    """
    try:
        directory = request.args.get('directory')
        if directory:
            directory = os.path.join(current_app.root_path, directory)

        uploader = get_file_uploader()
        files = uploader.list_files(directory)
        return JsonResult.success(files)

    except Exception as e:
        return JsonResult.error(f'获取文件列表失败: {str(e)}')


@file_upload_bp.route('/delete', methods=['DELETE'])
def delete_file():
    """
    删除文件
    请求体: {"file_path": "相对文件路径"}
    """
    try:
        data = request.get_json()
        if not data or 'file_path' not in data:
            return JsonResult.error('缺少文件路径参数')

        file_path = data['file_path']
        full_path = os.path.join(current_app.root_path, 'uploads', file_path)

        uploader = get_file_uploader()
        if uploader.delete_file(full_path):
            return JsonResult.success(None, '文件删除成功')
        else:
            return JsonResult.error('文件删除失败或文件不存在')

    except Exception as e:
        return JsonResult.error(f'删除文件失败: {str(e)}')


@file_upload_bp.route('/config', methods=['GET', 'PUT'])
def manage_config():
    """配置管理"""
    uploader = get_file_uploader()

    if request.method == 'GET':
        # 获取当前配置
        config = {
            'max_file_size_mb': uploader.max_file_size // (1024 * 1024),
            'allowed_extensions': uploader.allowed_extensions,
            'upload_dir': uploader.upload_dir,
            'static_dir': uploader.static_dir
        }
        return JsonResult.success(config)

    elif request.method == 'PUT':
        # 更新配置
        data = request.get_json()

        if 'max_file_size_mb' in data:
            uploader.set_max_file_size(data['max_file_size_mb'])

        if 'allowed_extensions' in data:
            for file_type, extensions in data['allowed_extensions'].items():
                for ext in extensions:
                    uploader.add_allowed_extension(file_type, ext)

        return JsonResult.success({'message': '配置更新成功'})


@file_upload_bp.route('/static/list', methods=['GET'])
def list_static_files():
    """列出static目录中的文件"""
    uploader = get_file_uploader()
    subfolder = request.args.get('subfolder')

    try:
        files = uploader.list_static_files(subfolder)
        return JsonResult.success({
            'files': files,
            'total': len(files),
            'subfolder': subfolder
        })
    except Exception as e:
        return JsonResult.error(f'获取文件列表失败: {str(e)}')


@file_upload_bp.route('/static/info/<path:file_path>', methods=['GET'])
def get_static_file_info(file_path):
    """获取static目录中文件的信息"""
    uploader = get_file_uploader()

    try:
        file_info = uploader.get_static_file_info(file_path)
        if file_info:
            return JsonResult.success(file_info)
        else:
            return JsonResult.error('文件不存在', 404)
    except Exception as e:
        return JsonResult.error(f'获取文件信息失败: {str(e)}')


@file_upload_bp.route('/static/delete', methods=['DELETE'])
def delete_static_file():
    """删除static目录中的文件"""
    uploader = get_file_uploader()
    data = request.get_json()

    if not data or 'file_path' not in data:
        return JsonResult.error('请提供文件路径')

    file_path = data['file_path']

    try:
        success = uploader.delete_static_file(file_path)
        if success:
            return JsonResult.success({'message': '文件删除成功'})
        else:
            return JsonResult.error('文件删除失败或文件不存在')
    except Exception as e:
        return JsonResult.error(f'删除文件失败: {str(e)}')


@file_upload_bp.route('/cdn/url', methods=['POST'])
def get_cdn_url():
    """获取文件的CDN访问URL"""
    uploader = get_file_uploader()
    data = request.get_json()

    if not data or 'file_path' not in data:
        return JsonResult.error('请提供文件路径')

    file_path = data['file_path']
    base_url = data.get('base_url')

    try:
        cdn_url = uploader.get_cdn_url(file_path, base_url)
        return JsonResult.success({
            'file_path': file_path,
            'cdn_url': cdn_url,
            'base_url': base_url
        })
    except Exception as e:
        return JsonResult.error(f'生成CDN URL失败: {str(e)}')


# 错误处理
@file_upload_bp.errorhandler(RequestEntityTooLarge)
def handle_file_too_large(e):
    return JsonResult.error('文件大小超过限制')


@file_upload_bp.errorhandler(413)
def handle_payload_too_large(e):
    return JsonResult.error('请求数据过大')
