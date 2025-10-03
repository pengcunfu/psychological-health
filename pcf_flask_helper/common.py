from flask import jsonify
from flask import request
from typing import Optional


def json_success(data=None, message='success', code=200):
    response = {
        'code': code,
        'message': message,
        'success': True
    }
    if data is not None:
        response['data'] = data
    return jsonify(response)


def json_error(message='fail', code=500, data=None):
    response = {
        'code': code,
        'message': message,
        'success': False
    }
    if data is not None:
        response['data'] = data
    return jsonify(response)


def process_image_url(image_url: Optional[str], base_url: Optional[str] = None) -> Optional[str]:
    """
    处理单个图片URL，如果不是完整URL则添加域名前缀

    Args:
        image_url (str, optional): 图片URL
        base_url (str, optional): 基础URL，如果不提供则自动获取

    Returns:
        str: 处理后的完整图片URL
    """
    if not image_url:
        return image_url

    # 如果已经是完整的URL，直接返回
    if image_url.startswith(('http://', 'https://')):
        return image_url

    # 获取基础URL
    if base_url is None:
        base_url = request.url_root.rstrip('/')

    # 确保路径以/开头
    if not image_url.startswith('/'):
        image_url = '/' + image_url

    return base_url + image_url
