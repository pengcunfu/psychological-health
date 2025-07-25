import os
import uuid
import mimetypes
from datetime import datetime
from werkzeug.datastructures import FileStorage
from flask import send_file, abort, current_app
from typing import Optional, Tuple


class FileUploader:
    def __init__(self, upload_dir: str = 'uploads', static_dir: str = 'static'):
        self.upload_dir = upload_dir
        self.static_dir = static_dir

        # 确保上传目录存在
        if not os.path.exists(self.upload_dir):
            os.makedirs(self.upload_dir)

        # 确保静态文件目录存在
        if not os.path.exists(self.static_dir):
            os.makedirs(self.static_dir)

        # 支持的文件类型
        self.allowed_extensions = {
            'image': {'jpg', 'jpeg', 'png', 'gif', 'bmp', 'webp', 'svg'},
            'document': {'pdf', 'doc', 'docx', 'txt', 'rtf'},
            'audio': {'mp3', 'wav', 'ogg', 'aac'},
            'video': {'mp4', 'avi', 'mov', 'wmv', 'flv'},
            'archive': {'zip', 'rar', '7z', 'tar', 'gz'}
        }

        # 最大文件大小 (默认10MB)
        self.max_file_size = 10 * 1024 * 1024

    def is_allowed_file(self, filename: str, file_type: str = None) -> bool:
        """
        检查文件是否允许上传
        :param filename: 文件名
        :param file_type: 文件类型 ('image', 'document', 'audio', 'video', 'archive')
        :return: 是否允许
        """
        if not filename or '.' not in filename:
            return False

        extension = filename.rsplit('.', 1)[1].lower()

        if file_type:
            return extension in self.allowed_extensions.get(file_type, set())
        else:
            # 检查所有类型
            all_extensions = set()
            for exts in self.allowed_extensions.values():
                all_extensions.update(exts)
            return extension in all_extensions

    def generate_unique_filename(self, original_filename: str) -> str:
        """
        生成唯一的文件名
        :param original_filename: 原始文件名
        :return: 唯一文件名
        """
        if not original_filename or '.' not in original_filename:
            return f"{uuid.uuid4().hex}.bin"

        name, ext = original_filename.rsplit('.', 1)
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        unique_id = uuid.uuid4().hex[:8]
        return f"{timestamp}_{unique_id}.{ext.lower()}"

    def save(self, file: FileStorage, filename: str = None, file_type: str = None,
             use_unique_name: bool = True) -> dict:
        """
        保存上传的文件到本地目录
        :param file: werkzeug.datastructures.FileStorage 对象
        :param filename: 保存的文件名，默认为原文件名
        :param file_type: 文件类型限制
        :param use_unique_name: 是否使用唯一文件名
        :return: 文件信息字典
        """
        if not file or not file.filename:
            raise ValueError("无效的文件")

        # 检查文件类型
        if not self.is_allowed_file(file.filename, file_type):
            raise ValueError(f"不支持的文件类型: {file.filename}")

        # 检查文件大小
        file.seek(0, 2)  # 移动到文件末尾
        file_size = file.tell()
        file.seek(0)  # 重置到文件开头

        if file_size > self.max_file_size:
            raise ValueError(f"文件大小超过限制 ({self.max_file_size / 1024 / 1024:.1f}MB)")

        # 确定文件名
        if use_unique_name:
            save_filename = self.generate_unique_filename(file.filename)
        else:
            save_filename = filename or file.filename

        # 保存文件
        save_path = os.path.join(self.upload_dir, save_filename)
        file.save(save_path)

        # 获取文件信息
        file_info = {
            'original_name': file.filename,
            'saved_name': save_filename,
            'file_path': save_path,
            'relative_path': os.path.join(self.upload_dir, save_filename).replace('\\', '/'),
            'file_size': file_size,
            'mime_type': mimetypes.guess_type(file.filename)[0],
            'upload_time': datetime.now().isoformat()
        }

        return file_info

    def save_to_static(self, file: FileStorage, subfolder: str = 'uploads',
                       filename: str = None, use_unique_name: bool = True) -> dict:
        """
        保存文件到static目录，可直接通过URL访问
        :param file: 文件对象
        :param subfolder: 子文件夹名称
        :param filename: 文件名
        :param use_unique_name: 是否使用唯一文件名
        :return: 文件信息字典
        """
        if not file or not file.filename:
            raise ValueError("无效的文件")

        # 检查文件类型
        if not self.is_allowed_file(file.filename):
            raise ValueError(f"不支持的文件类型: {file.filename}")

        # 检查文件大小
        file.seek(0, 2)  # 移动到文件末尾
        file_size = file.tell()
        file.seek(0)  # 重置到文件开头

        if file_size > self.max_file_size:
            raise ValueError(f"文件大小超过限制 ({self.max_file_size / 1024 / 1024:.1f}MB)")

        # 创建子目录
        target_dir = os.path.join(self.static_dir, subfolder)
        if not os.path.exists(target_dir):
            os.makedirs(target_dir)

        # 确定文件名
        if use_unique_name:
            save_filename = self.generate_unique_filename(file.filename)
        else:
            save_filename = filename or file.filename

        # 保存文件
        save_path = os.path.join(target_dir, save_filename)
        file.save(save_path)

        # 生成访问URL
        url_path = f"/static/{subfolder}/{save_filename}".replace('\\', '/')

        file_info = {
            'original_name': file.filename,
            'saved_name': save_filename,
            'file_path': save_path,
            'url': url_path,
            'cdn_url': url_path,  # 可以配置为CDN域名
            'file_size': file_size,
            'mime_type': mimetypes.guess_type(file.filename)[0],
            'upload_time': datetime.now().isoformat()
        }

        return file_info

    def download_file(self, file_path: str, as_attachment: bool = True,
                      download_name: str = None):
        """
        下载文件
        :param file_path: 文件路径
        :param as_attachment: 是否作为附件下载
        :param download_name: 下载时的文件名
        :return: Flask响应对象
        """
        if not os.path.exists(file_path):
            abort(404, "文件不存在")

        return send_file(
            file_path,
            as_attachment=as_attachment,
            download_name=download_name
        )

    def delete_file(self, file_path: str) -> bool:
        """
        删除文件
        :param file_path: 文件路径
        :return: 是否删除成功
        """
        try:
            if os.path.exists(file_path):
                os.remove(file_path)
                return True
            return False
        except Exception:
            return False

    def get_file_info(self, file_path: str) -> Optional[dict]:
        """
        获取文件信息
        :param file_path: 文件路径
        :return: 文件信息字典
        """
        if not os.path.exists(file_path):
            return None

        stat = os.stat(file_path)
        filename = os.path.basename(file_path)

        return {
            'filename': filename,
            'file_path': file_path,
            'file_size': stat.st_size,
            'mime_type': mimetypes.guess_type(filename)[0],
            'created_time': datetime.fromtimestamp(stat.st_ctime).isoformat(),
            'modified_time': datetime.fromtimestamp(stat.st_mtime).isoformat()
        }

    def list_files(self, directory: str = None) -> list:
        """
        列出目录中的文件
        :param directory: 目录路径，默认为上传目录
        :return: 文件列表
        """
        target_dir = directory or self.upload_dir
        if not os.path.exists(target_dir):
            return []

        files = []
        for filename in os.listdir(target_dir):
            file_path = os.path.join(target_dir, filename)
            if os.path.isfile(file_path):
                file_info = self.get_file_info(file_path)
                if file_info:
                    files.append(file_info)

        return files

    def set_max_file_size(self, size_mb: int):
        """
        设置最大文件大小
        :param size_mb: 大小(MB)
        """
        self.max_file_size = size_mb * 1024 * 1024

    def add_allowed_extension(self, file_type: str, extension: str):
        """
        添加允许的文件扩展名
        :param file_type: 文件类型
        :param extension: 扩展名
        """
        if file_type not in self.allowed_extensions:
            self.allowed_extensions[file_type] = set()
        self.allowed_extensions[file_type].add(extension.lower())

    def get_cdn_url(self, file_path: str, base_url: str = None) -> str:
        """
        获取文件的CDN访问URL
        :param file_path: 文件路径（相对于static目录）
        :param base_url: CDN基础URL，默认使用相对路径
        :return: CDN URL
        """
        # 确保路径使用正斜杠
        clean_path = file_path.replace('\\', '/').lstrip('/')

        if base_url:
            return f"{base_url.rstrip('/')}/static/{clean_path}"
        else:
            return f"/static/{clean_path}"

    def list_static_files(self, subfolder: str = None) -> list:
        """
        列出static目录中的文件
        :param subfolder: 子文件夹名称，为None时列出所有文件
        :return: 文件列表，包含CDN URL
        """
        if subfolder:
            target_dir = os.path.join(self.static_dir, subfolder)
        else:
            target_dir = self.static_dir

        if not os.path.exists(target_dir):
            return []

        files = []

        # 递归遍历目录
        for root, dirs, filenames in os.walk(target_dir):
            for filename in filenames:
                file_path = os.path.join(root, filename)
                # 计算相对于static目录的路径
                rel_path = os.path.relpath(file_path, self.static_dir)

                file_info = self.get_file_info(file_path)
                if file_info:
                    file_info['relative_path'] = rel_path.replace('\\', '/')
                    file_info['cdn_url'] = self.get_cdn_url(rel_path)
                    files.append(file_info)

        return files

    def delete_static_file(self, file_path: str) -> bool:
        """
        删除static目录中的文件
        :param file_path: 文件路径（相对于static目录）
        :return: 是否删除成功
        """
        full_path = os.path.join(self.static_dir, file_path.lstrip('/'))
        return self.delete_file(full_path)

    def get_static_file_info(self, file_path: str) -> Optional[dict]:
        """
        获取static目录中文件的信息
        :param file_path: 文件路径（相对于static目录）
        :return: 文件信息字典，包含CDN URL
        """
        full_path = os.path.join(self.static_dir, file_path.lstrip('/'))
        file_info = self.get_file_info(full_path)

        if file_info:
            file_info['relative_path'] = file_path.replace('\\', '/').lstrip('/')
            file_info['cdn_url'] = self.get_cdn_url(file_path)

        return file_info
