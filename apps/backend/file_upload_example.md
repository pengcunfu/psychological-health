# 文件上传工具使用指南

## 概述

这个增强的文件上传工具支持以下功能：
- 文件上传到普通目录
- 文件上传到static目录（CDN访问）
- 文件下载
- 文件信息查询
- 文件列表获取
- 文件删除
- 配置管理
- CDN功能和静态文件管理
- Web界面管理（views目录）

## 快速开始

### 1. 在Flask应用中注册蓝图

```python
# app.py
from flask import Flask
from api.file import file_upload_bp
from views.file_upload import file_upload_views_bp

app = Flask(__name__)

# 注册文件上传API蓝图
app.register_blueprint(file_upload_bp)

# 注册文件上传Web界面蓝图
app.register_blueprint(file_upload_views_bp)

# 设置最大文件大小（可选）
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB


# 配置静态文件CDN访问
@app.route('/static/<path:filename>')
def static_files(filename):
  """静态文件CDN访问"""
  from flask import send_from_directory
  import os
  static_dir = os.path.join(app.root_path, 'static')
  return send_from_directory(static_dir, filename)
```

### 2. 基本使用

```python
from utils.file_upload import FileUploader

# 创建文件上传器实例
uploader = FileUploader(
    upload_dir='uploads',
    static_dir='static'
)

# 保存文件
file_info = uploader.save(file, file_type='image')
print(file_info)
```

## API接口说明

### 1. 文件上传 - `/api/files/upload`

**方法**: POST  
**Content-Type**: multipart/form-data

**参数**:
- `file`: 上传的文件（必需）
- `file_type`: 文件类型限制（可选）
  - `image`: 图片文件
  - `document`: 文档文件
  - `audio`: 音频文件
  - `video`: 视频文件
  - `archive`: 压缩文件
- `use_unique_name`: 是否使用唯一文件名（默认true）

**响应示例**:
```json
{
  "code": 200,
  "message": "文件上传成功",
  "data": {
    "original_name": "photo.jpg",
    "saved_name": "20240101_120000_abc12345.jpg",
    "file_path": "uploads/20240101_120000_abc12345.jpg",
    "relative_path": "uploads/20240101_120000_abc12345.jpg",
    "file_size": 1024000,
    "mime_type": "image/jpeg",
    "upload_time": "2024-01-01T12:00:00"
  }
}
```

### 2. 上传到Static目录 - `/api/files/upload-to-static`

**方法**: POST  
**Content-Type**: multipart/form-data

**参数**:
- `file`: 上传的文件（必需）
- `subfolder`: 子文件夹名称（默认uploads）
- `use_unique_name`: 是否使用唯一文件名（默认true）

**响应示例**:
```json
{
  "code": 200,
  "message": "文件上传成功",
  "data": {
    "original_name": "avatar.png",
    "saved_name": "20240101_120000_def67890.png",
    "file_path": "static/uploads/20240101_120000_def67890.png",
    "url": "/static/uploads/20240101_120000_def67890.png",
    "cdn_url": "/static/uploads/20240101_120000_def67890.png",
    "file_size": 512000,
    "mime_type": "image/png",
    "upload_time": "2024-01-01T12:00:00"
  }
}
```

### 3. 文件下载 - `/api/files/download/<path:file_path>`

**方法**: GET

**参数**:
- `file_path`: 文件相对路径（URL路径参数）
- `name`: 下载时的文件名（查询参数，可选）
- `attachment`: 是否作为附件下载（查询参数，默认true）

**示例**:
```
GET /api/files/download/20240101_120000_abc12345.jpg?name=my_photo.jpg&attachment=true
```

### 4. 获取文件信息 - `/api/files/info/<path:file_path>`

**方法**: GET

**响应示例**:
```json
{
  "code": 200,
  "data": {
    "filename": "20240101_120000_abc12345.jpg",
    "file_path": "uploads/20240101_120000_abc12345.jpg",
    "file_size": 1024000,
    "mime_type": "image/jpeg",
    "created_time": "2024-01-01T12:00:00",
    "modified_time": "2024-01-01T12:00:00"
  }
}
```

### 5. 文件列表 - `/api/files/list`

**方法**: GET

**参数**:
- `directory`: 目录路径（查询参数，可选）

**响应示例**:
```json
{
  "code": 200,
  "data": [
    {
      "filename": "file1.jpg",
      "file_path": "uploads/file1.jpg",
      "file_size": 1024000,
      "mime_type": "image/jpeg",
      "created_time": "2024-01-01T12:00:00",
      "modified_time": "2024-01-01T12:00:00"
    }
  ]
}
```

### 6. 删除文件 - `/api/files/delete`

**方法**: DELETE  
**Content-Type**: application/json

**请求体**:
```json
{
  "file_path": "20240101_120000_abc12345.jpg"
}
```

### 7. 配置管理 - `/api/files/config`

**获取配置** - GET:
```json
{
  "code": 200,
  "data": {
    "max_file_size_mb": 10,
    "allowed_extensions": {
      "image": ["jpg", "jpeg", "png", "gif"],
      "document": ["pdf", "doc", "docx"]
    },
    "upload_dir": "uploads",
    "static_dir": "static"
  }
}
```

**更新配置** - PUT:
```json
{
  "max_file_size_mb": 20,
  "allowed_extensions": {
    "image": ["jpg", "jpeg", "png", "gif", "webp"],
    "document": ["pdf", "doc", "docx", "txt"]
  }
}
```

### 8. CDN功能

#### 8.1 列出Static文件 - `/api/files/static/list`

**方法**: GET

**参数**:
- `subfolder`: 子文件夹名称（可选）

**响应示例**:
```json
{
  "code": 200,
  "data": {
    "files": [
      {
        "filename": "example.jpg",
        "file_path": "static/images/example.jpg",
        "relative_path": "images/example.jpg",
        "cdn_url": "/static/images/example.jpg",
        "file_size": 1024000,
        "mime_type": "image/jpeg",
        "created_time": "2024-01-01T12:00:00",
        "modified_time": "2024-01-01T12:00:00"
      }
    ],
    "total": 1,
    "subfolder": "images"
  }
}
```

#### 8.2 获取Static文件信息 - `/api/files/static/info/<path:file_path>`

**方法**: GET

**响应示例**:
```json
{
  "code": 200,
  "data": {
    "filename": "example.jpg",
    "file_path": "static/images/example.jpg",
    "relative_path": "images/example.jpg",
    "cdn_url": "/static/images/example.jpg",
    "file_size": 1024000,
    "mime_type": "image/jpeg",
    "created_time": "2024-01-01T12:00:00",
    "modified_time": "2024-01-01T12:00:00"
  }
}
```

#### 8.3 删除Static文件 - `/api/files/static/delete`

**方法**: DELETE
**Content-Type**: application/json

**请求体**:
```json
{
  "file_path": "images/example.jpg"
}
```

#### 8.4 获取CDN URL - `/api/files/cdn/url`

**方法**: POST
**Content-Type**: application/json

**请求体**:
```json
{
  "file_path": "images/example.jpg",
  "base_url": "https://cdn.example.com"
}
```

**响应示例**:
```json
{
  "code": 200,
  "data": {
    "file_path": "images/example.jpg",
    "cdn_url": "https://cdn.example.com/static/images/example.jpg",
    "base_url": "https://cdn.example.com"
  }
}
```

### 9. Web界面管理

#### 9.1 文件管理页面 - `/files/manage`

提供Web界面进行文件管理，包括：
- 文件上传
- 文件列表查看
- 文件删除
- 文件下载
- 配置管理

#### 9.2 CDN管理页面 - `/files/cdn`

提供CDN文件管理界面，包括：
- Static文件列表
- CDN URL生成
- 文件预览
- 批量操作

## 前端使用示例

### JavaScript/Ajax上传

```javascript
// 文件上传
function uploadFile(file, fileType = null) {
    const formData = new FormData();
    formData.append('file', file);
    if (fileType) {
        formData.append('file_type', fileType);
    }
    
    return fetch('/api/files/upload', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        if (data.code === 200) {
            console.log('上传成功:', data.data);
            return data.data;
        } else {
            throw new Error(data.message);
        }
    });
}

// 上传到static目录（CDN）
function uploadToStatic(file, subfolder = 'uploads') {
    const formData = new FormData();
    formData.append('file', file);
    formData.append('subfolder', subfolder);
    
    return fetch('/api/files/upload-to-static', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        if (data.code === 200) {
            console.log('上传成功，CDN地址:', data.data.url);
            return data.data;
        } else {
            throw new Error(data.message);
        }
    });
}

// 使用示例
document.getElementById('fileInput').addEventListener('change', function(e) {
    const file = e.target.files[0];
    if (file) {
        uploadToStatic(file, 'images')
            .then(fileInfo => {
                // 显示图片
                const img = document.createElement('img');
                img.src = fileInfo.url;
                document.body.appendChild(img);
            })
            .catch(error => {
                console.error('上传失败:', error);
            });
    }
});
```

### HTML表单上传

```html
<!-- 普通文件上传 -->
<form action="/api/files/upload" method="post" enctype="multipart/form-data">
    <input type="file" name="file" required>
    <select name="file_type">
        <option value="">所有类型</option>
        <option value="image">图片</option>
        <option value="document">文档</option>
    </select>
    <button type="submit">上传</button>
</form>

<!-- 上传到static目录 -->
<form action="/api/files/upload-to-static" method="post" enctype="multipart/form-data">
    <input type="file" name="file" required>
    <input type="text" name="subfolder" value="uploads" placeholder="子文件夹">
    <button type="submit">上传到CDN</button>
</form>
```

## 配置说明

### 支持的文件类型

- **图片**: jpg, jpeg, png, gif, bmp, webp, svg
- **文档**: pdf, doc, docx, txt, rtf
- **音频**: mp3, wav, ogg, aac
- **视频**: mp4, avi, mov, wmv, flv
- **压缩**: zip, rar, 7z, tar, gz

### 安全特性

1. **文件类型验证**: 基于文件扩展名验证
2. **文件大小限制**: 默认10MB，可配置
3. **唯一文件名**: 防止文件名冲突
4. **路径安全**: 防止目录遍历攻击

### 目录结构

```
wx-server/
├── uploads/          # 普通上传文件
├── static/           # 静态文件（CDN）
│   ├── uploads/      # 上传的静态文件
│   ├── images/       # 图片资源
│   └── libs/         # 库文件
└── api/
    └── file_upload.py # 文件上传API
```

## 注意事项

1. 确保上传目录有写权限
2. 配置合适的文件大小限制
3. 定期清理临时文件
4. 考虑使用真实的CDN服务
5. 在生产环境中添加认证和授权
6. Web界面需要配置模板目录
7. CDN功能需要配置正确的静态文件路径
8. 建议在生产环境中使用专业的CDN服务