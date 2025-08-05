"""
图片路径处理工具
用于处理API响应中的图片路径，自动添加域名前缀

# 处理单个图片URL
image_url = process_image_url('/static/images/avatar.jpg')
# 结果: 'http://localhost:5000/static/images/avatar.jpg'

# 处理字典中的图片字段
counselor_data = {
    'id': 1,
    'name': '张医生',
    'avatar': '/static/images/avatar.jpg'
}
processed_counselor = process_image_urls_in_dict(counselor_data, 'avatar')

# 处理列表中的图片字段
counselors_list = [
    {'id': 1, 'name': '张医生', 'avatar': '/static/images/avatar1.jpg'},
    {'id': 2, 'name': '李医生', 'avatar': '/static/images/avatar2.jpg'}
]
processed_list = process_image_urls_in_list(counselors_list, 'avatar')

# 使用专门的处理函数
processed_counselors = process_counselor_images(counselors_list)
"""

from flask import request
from typing import List, Dict, Any, Union, Optional


def get_base_url() -> str:
    """
    获取当前应用的基础URL
    
    Returns:
        str: 基础URL，例如 'http://localhost:5000'
    """
    # return request.url_root.rstrip('/')
    return 'http://192.168.185.4:5000'


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
        base_url = get_base_url()
    
    # 确保路径以/开头
    if not image_url.startswith('/'):
        image_url = '/' + image_url
    
    return base_url + image_url


def process_image_urls_in_dict(data: Dict[str, Any], image_fields: Union[str, List[str]], 
                              base_url: Optional[str] = None) -> Dict[str, Any]:
    """
    处理字典中指定字段的图片URL
    
    Args:
        data (dict): 包含图片字段的字典
        image_fields (str or list): 需要处理的图片字段名，可以是单个字段名或字段名列表
        base_url (str, optional): 基础URL，如果不提供则自动获取
        
    Returns:
        dict: 处理后的字典
    """
    if not isinstance(data, dict):
        return data
    
    # 统一处理为列表
    if isinstance(image_fields, str):
        image_fields = [image_fields]
    
    # 获取基础URL
    if base_url is None:
        base_url = get_base_url()
    
    # 复制数据避免修改原始数据
    processed_data = data.copy()
    
    # 处理每个指定的图片字段
    for field in image_fields:
        if field in processed_data:
            processed_data[field] = process_image_url(processed_data[field], base_url)
    
    return processed_data


def process_image_urls_in_list(data_list: List[Dict[str, Any]], image_fields: Union[str, List[str]], 
                              base_url: Optional[str] = None) -> List[Dict[str, Any]]:
    """
    处理列表中每个字典的指定图片字段
    
    Args:
        data_list (list): 包含字典的列表
        image_fields (str or list): 需要处理的图片字段名，可以是单个字段名或字段名列表
        base_url (str, optional): 基础URL，如果不提供则自动获取
        
    Returns:
        list: 处理后的列表
    """
    if not isinstance(data_list, list):
        return data_list
    
    # 获取基础URL
    if base_url is None:
        base_url = get_base_url()
    
    # 处理列表中的每个项目
    processed_list = []
    for item in data_list:
        if isinstance(item, dict):
            processed_item = process_image_urls_in_dict(item, image_fields, base_url)
            processed_list.append(processed_item)
        else:
            processed_list.append(item)
    
    return processed_list


def process_counselor_images(data: Union[Dict[str, Any], List[Dict[str, Any]]], 
                           base_url: Optional[str] = None) -> Union[Dict[str, Any], List[Dict[str, Any]]]:
    """
    专门处理咨询师数据中的图片字段
    
    Args:
        data (dict or list): 咨询师数据，可以是单个字典或字典列表
        base_url (str, optional): 基础URL，如果不提供则自动获取
        
    Returns:
        dict or list: 处理后的咨询师数据
    """
    image_fields = ['avatar']  # 咨询师的图片字段
    
    if isinstance(data, list):
        return process_image_urls_in_list(data, image_fields, base_url)
    elif isinstance(data, dict):
        return process_image_urls_in_dict(data, image_fields, base_url)
    else:
        return data


def process_course_images(data: Union[Dict[str, Any], List[Dict[str, Any]]], 
                         base_url: Optional[str] = None) -> Union[Dict[str, Any], List[Dict[str, Any]]]:
    """
    专门处理课程数据中的图片字段
    
    Args:
        data (dict or list): 课程数据，可以是单个字典或字典列表
        base_url (str, optional): 基础URL，如果不提供则自动获取
        
    Returns:
        dict or list: 处理后的课程数据
    """
    image_fields = ['cover', 'thumbnail']  # 课程的图片字段
    
    if isinstance(data, list):
        return process_image_urls_in_list(data, image_fields, base_url)
    elif isinstance(data, dict):
        return process_image_urls_in_dict(data, image_fields, base_url)
    else:
        return data


def process_banner_images(data: Union[Dict[str, Any], List[Dict[str, Any]]], 
                         base_url: Optional[str] = None) -> Union[Dict[str, Any], List[Dict[str, Any]]]:
    """
    专门处理轮播图数据中的图片字段
    
    Args:
        data (dict or list): 轮播图数据，可以是单个字典或字典列表
        base_url (str, optional): 基础URL，如果不提供则自动获取
        
    Returns:
        dict or list: 处理后的轮播图数据
    """
    image_fields = ['image_url']  # 轮播图的图片字段
    
    if isinstance(data, list):
        return process_image_urls_in_list(data, image_fields, base_url)
    elif isinstance(data, dict):
        return process_image_urls_in_dict(data, image_fields, base_url)
    else:
        return data


