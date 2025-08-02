
# 心理咨询预约小程序 API 文档

## 目录

- [用户相关](#用户相关)
- [咨询师相关](#咨询师相关)
- [课程相关](#课程相关)
- [订单相关](#订单相关)
- [收藏相关](#收藏相关)
- [评价相关](#评价相关)
- [消息相关](#消息相关)
- [系统相关](#系统相关)

## 用户相关

### 登录注册

#### 手机号验证码登录

- **接口**: `/api/user/login/phone`
- **方法**: POST
- **请求格式**:
```json
{
  "phone": "13800138000",
  "code": "123456"
}
```
- **响应格式**:
```json
{
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "userId": "12345",
  "isNew": false
}
```

#### 发送验证码

- **接口**: `/api/user/send-code`
- **方法**: POST
- **请求格式**:
```json
{
  "phone": "13800138000"
}
```
- **响应格式**:
```json
{
  "success": true,
  "message": "验证码发送成功"
}
```

#### 微信登录

- **接口**: `/api/user/login/wechat`
- **方法**: POST
- **请求格式**:
```json
{
  "code": "wx_auth_code_from_wechat"
}
```
- **响应格式**:
```json
{
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "userId": "12345",
  "isNew": false
}
```

### 用户信息

#### 获取用户信息

- **接口**: `/api/user/profile`
- **方法**: GET
- **响应格式**:
```json
{
  "id": "12345",
  "nickname": "用户昵称",
  "avatar": "https://example.com/avatar.jpg",
  "phone": "138****8000",
  "gender": "female",
  "age": 28,
  "bio": "个人简介内容",
  "createTime": "2023-05-20T08:30:45Z"
}
```

#### 更新用户信息

- **接口**: `/api/user/profile/update`
- **方法**: PUT
- **请求格式**:
```json
{
  "nickname": "新昵称",
  "avatar": "https://example.com/new-avatar.jpg",
  "gender": "male",
  "age": 30,
  "bio": "更新后的个人简介"
}
```
- **响应格式**:
```json
{
  "success": true,
  "message": "用户信息更新成功"
}
```

#### 获取用户统计数据

- **接口**: `/api/user/statistics`
- **方法**: GET
- **响应格式**:
```json
{
  "favoriteCount": 12,
  "orderCount": 8,
  "pendingOrderCount": 2,
  "completedSessionCount": 5,
  "courseCount": 3
}
```

## 咨询师相关

### 咨询师列表

#### 获取咨询师列表

- **接口**: `/api/counselor/list`
- **方法**: GET
- **请求参数**:
```json
{
  "page": 1,
  "pageSize": 10,
  "keyword": "抑郁",
  "categoryId": "2",
  "sortBy": "rating"
}
```
- **响应格式**:
```json
{
  "total": 42,
  "list": [
    {
      "id": "c001",
      "name": "张医生",
      "avatar": "https://example.com/counselor1.jpg",
      "title": "心理咨询师",
      "isVerified": true,
      "tags": ["抑郁症", "焦虑障碍", "青少年心理"],
      "price": 300,
      "rating": 4.8,
      "sessionCount": 256,
      "introduction": "专注于抑郁症和焦虑障碍治疗的心理咨询师..."
    }
  ]
}
```

### 咨询师详情

#### 获取咨询师详情

- **接口**: `/api/counselor/detail`
- **方法**: GET
- **请求参数**:
```json
{
  "id": "c001"
}
```
- **响应格式**:
```json
{
  "id": "c001",
  "name": "张医生",
  "avatar": "https://example.com/counselor1.jpg",
  "title": "心理咨询师",
  "isVerified": true,
  "tags": ["抑郁症", "焦虑障碍", "青少年心理"],
  "price": 300,
  "rating": 4.8,
  "sessionCount": 256,
  "introduction": "15年临床经验，专注于抑郁症和焦虑障碍治疗...",
  "education": "北京大学心理学博士",
  "experience": "曾任某三甲医院心理科主任医师，有丰富的临床经验...",
  "certificates": ["国家二级心理咨询师", "认知行为治疗师资格证"],
  "services": ["个人咨询", "家庭咨询", "青少年咨询"],
  "availability": ["周一至周五: 9:00-18:00", "周六: 10:00-16:00"],
  "reviews": [
    {
      "id": "r001",
      "user": "李**",
      "content": "非常专业的咨询师，帮助我走出了困境",
      "rating": 5,
      "time": "2023-05-15"
    }
  ]
}
```

#### 获取咨询师可预约时间

- **接口**: `/api/counselor/available-slots`
- **方法**: GET
- **请求参数**:
```json
{
  "id": "c001",
  "date": "2023-06-01"
}
```
- **响应格式**:
```json
{
  "date": "2023-06-01",
  "slots": [
    {
      "startTime": "09:00",
      "endTime": "10:00",
      "isAvailable": true
    },
    {
      "startTime": "10:00",
      "endTime": "11:00",
      "isAvailable": false
    }
  ]
}
```

#### 提交预约

- **接口**: `/api/counselor/book`
- **方法**: POST
- **请求格式**:
```json
{
  "counselorId": "c001",
  "serviceId": "s002",
  "date": "2023-06-01",
  "timeSlot": "09:00-10:00",
  "note": "第一次咨询，希望能得到专业帮助"
}
```
- **响应格式**:
```json
{
  "success": true,
  "orderId": "o12345"
}
```

## 课程相关

### 课程列表

#### 获取课程列表

- **接口**: `/api/course/list`
- **方法**: GET
- **请求参数**:
```json
{
  "page": 1,
  "pageSize": 10,
  "keyword": "情绪管理",
  "categoryId": "3",
  "sortBy": "popularity"
}
```
- **响应格式**:
```json
{
  "total": 28,
  "list": [
    {
      "id": "course001",
      "title": "情绪管理入门课程",
      "coverImage": "https://example.com/course1.jpg",
      "teacher": "王教授",
      "price": 99,
      "originalPrice": 199,
      "lessonCount": 12,
      "studentCount": 2560,
      "rating": 4.7,
      "tags": ["情绪管理", "心理健康", "初级"],
      "description": "适合初学者的情绪管理课程，帮助你掌握基本的情绪调节技巧..."
    }
  ]
}
```

### 课程详情

#### 获取课程详情

- **接口**: `/api/course/detail`
- **方法**: GET
- **请求参数**:
```json
{
  "id": "course001"
}
```
- **响应格式**:
```json
{
  "id": "course001",
  "title": "情绪管理入门课程",
  "coverImage": "https://example.com/course1.jpg",
  "teacher": "王教授",
  "teacherTitle": "心理学教授",
  "teacherAvatar": "https://example.com/teacher1.jpg",
  "price": 99,
  "originalPrice": 199,
  "lessonCount": 12,
  "totalDuration": "6小时30分钟",
  "studentCount": 2560,
  "rating": 4.7,
  "tags": ["情绪管理", "心理健康", "初级"],
  "introduction": "本课程从情绪的基本概念出发，系统讲解情绪管理的核心方法...",
  "suitableFor": "职场人士、学生、有情绪困扰的人群",
  "outline": [
    {
      "title": "第一章：认识情绪",
      "lessons": ["什么是情绪", "情绪的生理基础", "常见情绪类型"]
    }
  ],
  "samples": ["https://example.com/sample1.mp4"],
  "isBought": false,
  "expiryDate": null
}
```

#### 获取课程章节

- **接口**: `/api/course/chapters`
- **方法**: GET
- **请求参数**:
```json
{
  "id": "course001"
}
```
- **响应格式**:
```json
{
  "list": [
    {
      "id": "chap001",
      "title": "第一章：认识情绪",
      "duration": "45分钟",
      "isFree": true,
      "isCompleted": false,
      "videoUrl": "https://example.com/course1-chap1.mp4"
    },
    {
      "id": "chap002",
      "title": "第二章：情绪调节基础",
      "duration": "60分钟",
      "isFree": false,
      "isCompleted": false,
      "videoUrl": null
    }
  ]
}
```

#### 记录学习进度

- **接口**: `/api/course/progress`
- **方法**: POST
- **请求格式**:
```json
{
  "courseId": "course001",
  "chapterId": "chap001",
  "progress": 75,
  "duration": 15
}
```
- **响应格式**:
```json
{
  "success": true,
  "isCompleted": false
}
```

## 订单相关

### 订单管理

#### 获取订单列表

- **接口**: `/api/order/list`
- **方法**: GET
- **请求参数**:
```json
{
  "status": "paid",
  "page": 1,
  "pageSize": 10
}
```
- **响应格式**:
```json
{
  "total": 15,
  "list": [
    {
      "id": "o12345",
      "orderNo": "2023060112345",
      "type": "counseling",
      "title": "心理咨询服务",
      "providerName": "张医生",
      "providerTitle": "心理咨询师",
      "appointmentTime": "2023-06-01 10:00-11:00",
      "purchaseTime": null,
      "price": 300,
      "status": "paid",
      "createTime": "2023-05-28T14:30:25Z"
    }
  ]
}
```

#### 获取订单详情

- **接口**: `/api/order/detail`
- **方法**: GET
- **请求参数**:
```json
{
  "id": "o12345"
}
```
- **响应格式**:
```json
{
  "id": "o12345",
  "orderNo": "2023060112345",
  "type": "counseling",
  "title": "心理咨询服务",
  "providerName": "张医生",
  "providerTitle": "心理咨询师",
  "providerAvatar": "https://example.com/counselor1.jpg",
  "serviceInfo": "个人咨询 (50分钟)",
  "appointmentTime": "2023-06-01 10:00-11:00",
  "expiryDate": null,
  "price": 300,
  "discount": 0,
  "actualPaid": 300,
  "paymentMethod": "wechat",
  "paymentTime": "2023-05-28T14:35:10Z",
  "status": "paid",
  "createTime": "2023-05-28T14:30:25Z",
  "note": "第一次咨询，希望能得到专业帮助"
}
```

#### 取消订单

- **接口**: `/api/order/cancel`
- **方法**: POST
- **请求格式**:
```json
{
  "id": "o12345"
}
```
- **响应格式**:
```json
{
  "success": true,
  "message": "订单取消成功"
}
```

### 支付相关

#### 创建支付订单

- **接口**: `/api/payment/create`
- **方法**: POST
- **请求格式**:
```json
{
  "orderId": "o12345",
  "paymentMethod": "wechat"
}
```
- **响应格式**:
```json
{
  "payParams": {
    "appId": "wx123456789",
    "timeStamp": "1622188800",
    "nonceStr": "abcdef123456",
    "package": "prepay_id=wx12345678",
    "signType": "MD5",
    "paySign": "ABCDEF1234567890"
  },
  "orderId": "o12345",
  "orderNo": "2023060112345",
  "amount": 300
}
```

#### 查询支付状态

- **接口**: `/api/payment/status`
- **方法**: GET
- **请求参数**:
```json
{
  "orderId": "o12345"
}
```
- **响应格式**:
```json
{
  "isPaid": true,
  "paymentMethod": "wechat",
  "paymentTime": "2023-05-28T14:35:10Z"
}
```

#### 申请退款

- **接口**: `/api/payment/refund`
- **方法**: POST
- **请求格式**:
```json
{
  "orderId": "o12345",
  "reason": "个人原因无法参加咨询"
}
```
- **响应格式**:
```json
{
  "success": true,
  "message": "退款申请提交成功",
  "refundId": "r5678"
}
```

## 收藏相关

### 收藏管理

#### 获取收藏列表

- **接口**: `/api/favorite/list`
- **方法**: GET
- **请求参数**:
```json
{
  "type": "counselor",
  "page": 1,
  "pageSize": 10
}
```
- **响应格式**:
```json
{
  "total": 8,
  "list": [
    {
      "id": "c001",
      "name": "张医生",
      "avatar": "https://example.com/counselor1.jpg",
      "title": "心理咨询师",
      "isVerified": true,
      "tags": ["抑郁症", "焦虑障碍", "青少年心理"],
      "price": 300
    }
  ]
}
```

#### 添加/取消收藏

- **接口**: `/api/favorite/toggle`
- **方法**: POST
- **请求格式**:
```json
{
  "id": "c001",
  "type": "counselor"
}
```
- **响应格式**:
```json
{
  "success": true,
  "isFavorite": true,
  "message": "收藏成功"
}
```

#### 检查是否收藏

- **接口**: `/api/favorite/check`
- **方法**: GET
- **请求参数**:
```json
{
  "id": "c001",
  "type": "counselor"
}
```
- **响应格式**:
```json
{
  "isFavorite": true
}
```

## 评价相关

### 评价管理

#### 获取评价列表

- **接口**: `/api/review/list`
- **方法**: GET
- **请求参数**:
```json
{
  "targetId": "c001",
  "targetType": "counselor",
  "page": 1,
  "pageSize": 10
}
```
- **响应格式**:
```json
{
  "total": 42,
  "list": [
    {
      "id": "r001",
      "userId": "u123",
      "userName": "李**",
      "userAvatar": "https://example.com/avatar2.jpg",
      "rating": 5,
      "content": "非常专业的咨询师，帮助我走出了困境",
      "createTime": "2023-05-15T10:20:30Z",
      "replyContent": "感谢您的评价，希望您一切顺利",
      "replyTime": "2023-05-15T15:30:45Z"
    }
  ]
}
```

#### 提交评价

- **接口**: `/api/review/submit`
- **方法**: POST
- **请求格式**:
```json
{
  "targetId": "c001",
  "targetType": "counselor",
  "orderId": "o12345",
  "rating": 5,
  "content": "非常专业的咨询师，帮助我走出了困境",
  "isAnonymous": true
}
```
- **响应格式**:
```json
{
  "success": true,
  "message": "评价提交成功",
  "reviewId": "r001"
}
```

## 消息相关

### 消息通知

#### 获取未读消息数量

- **接口**: `/api/message/unread-count`
- **方法**: GET
- **响应格式**:
```json
{
  "count": 5
}
```

#### 获取消息列表

- **接口**: `/api/message/list`
- **方法**: GET
- **请求参数**:
```json
{
  "page": 1,
  "pageSize": 20
}
```
- **响应格式**:
```json
{
  "total": 28,
  "list": [
    {
      "id": "m001",
      "title": "预约提醒",
      "content": "您与张医生的心理咨询预约将在明天10:00开始",
      "type": "appointment",
      "isRead": false,
      "createTime": "2023-05-30T08:00:00Z",
      "relatedId": "o12345",
      "relatedType": "order"
    }
  ]
}
```

#### 标记消息已读

- **接口**: `/api/message/read`
- **方法**: POST
- **请求格式**:
```json
{
  "id": "m001"
}
```
- **响应格式**:
```json
{
  "success": true
}
```

#### 全部标记已读

- **接口**: `/api/message/read-all`
- **方法**: POST
- **响应格式**:
```json
{
  "success": true,
  "count": 5
}
```

## 系统相关

### 配置信息

#### 获取首页配置

- **接口**: `/api/config/home`
- **方法**: GET
- **响应格式**:
```json
{
  "banners": [
    {
      "id": "b001",
      "imageUrl": "https://example.com/banner1.jpg",
      "linkUrl": "/pages/course/detail?id=course001",
      "title": "情绪管理入门课程"
    }
  ],
  "recommends": [
    {
      "id": "c001",
      "name": "张医生",
      "avatar": "https://example.com/counselor1.jpg",
      "title": "心理咨询师",
      "tags": ["抑郁症", "焦虑障碍"]
    }
  ],
  "popularCourses": [
    {
      "id": "course001",
      "title": "情绪管理入门课程",
      "coverImage": "https://example.com/course1.jpg",
      "price": 99
    }
  ],
  "categories": [
    {
      "id": "1",
      "name": "抑郁症",
      "icon": "https://example.com/icon-depression.png"
    }
  ],
  "announcements": [
    {
      "id": "a001",
      "content": "新版小程序上线，体验全新功能",
      "time": "2023-05-20"
    }
  ]
}
```

#### 获取分类列表

- **接口**: `/api/config/categories`
- **方法**: GET
- **请求参数**:
```json
{
  "type": "counselor"
}
```
- **响应格式**:
```json
{
  "list": [
    {
      "id": "1",
      "name": "抑郁症",
      "icon": "https://example.com/icon-depression.png"
    },
    {
      "id": "2",
      "name": "焦虑障碍",
      "icon": "https://example.com/icon-anxiety.png"
    }
  ]
}
```

#### 获取协议内容

- **接口**: `/api/config/agreement`
- **方法**: GET
- **请求参数**:
```json
{
  "type": "user"
}
```
- **响应格式**:
```json
{
  "title": "用户服务协议",
  "content": "一、服务条款\n1.1 本协议是您与平台之间关于使用本平台服务所订立的协议...",
  "updateTime": "2023-01-01"
}
```

### 上传文件

#### 上传图片

- **接口**: `/api/upload/image`
- **方法**: POST
- **请求格式**:
```
// 以表单形式提交
FormData {
  file: [二进制文件数据],
  type: "avatar"
}
```
- **响应格式**:
```json
{
  "url": "https://example.com/uploads/avatar123.jpg",
  "width": 200,
  "height": 200,
  "size": 1024
}
```
