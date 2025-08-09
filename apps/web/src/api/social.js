import api from '@/utils/api'

// 话题管理API
export const socialTopicAPI = {
  // 获取话题列表
  getSocialTopics: (params) => api.get('/social-topic', { params }),
  // 获取热门话题
  getHotTopics: (params) => api.get('/social-topic/hot', { params }),
  // 获取话题详情
  getSocialTopic: (id) => api.get(`/social-topic/${id}`),
  // 创建话题
  createSocialTopic: (data) => api.post('/social-topic', data),
  // 更新话题
  updateSocialTopic: (id, data) => api.put(`/social-topic/${id}`, data),
  // 删除话题
  deleteSocialTopic: (id) => api.delete(`/social-topic/${id}`),
  // 获取话题统计
  getTopicStats: () => api.get('/social-topic/stats')
}

// 帖子管理API
export const socialPostAPI = {
  // 获取帖子列表
  getSocialPosts: (params) => api.get('/social-post', { params }),
  // 获取推荐帖子
  getRecommendPosts: (params) => api.get('/social-post/recommend', { params }),
  // 获取关注用户的帖子
  getFollowingPosts: (params) => api.get('/social-post/following', { params }),
  // 获取帖子详情
  getSocialPost: (id) => api.get(`/social-post/${id}`),
  // 创建帖子
  createSocialPost: (data) => api.post('/social-post', data),
  // 更新帖子
  updateSocialPost: (id, data) => api.put(`/social-post/${id}`, data),
  // 删除帖子
  deleteSocialPost: (id) => api.delete(`/social-post/${id}`),
  // 获取我的帖子
  getMySocialPosts: (params) => api.get('/social-post/my', { params }),
  // 获取帖子统计
  getPostStats: () => api.get('/social-post/stats')
}

// 评论管理API
export const socialCommentAPI = {
  // 获取评论列表
  getSocialComments: (params) => api.get('/social-comment', { params }),
  // 创建评论
  createSocialComment: (data) => api.post('/social-comment', data),
  // 删除评论
  deleteSocialComment: (id) => api.delete(`/social-comment/${id}`)
}

// 点赞管理API
export const socialLikeAPI = {
  // 切换点赞状态
  toggleLike: (data) => api.post('/social-like/toggle', data),
  // 检查点赞状态
  checkLike: (data) => api.post('/social-like/check', data),
  // 获取我的点赞记录
  getMyLikes: (params) => api.get('/social-like/my', { params }),
  // 获取收到的点赞
  getReceivedLikes: (params) => api.get('/social-like/received', { params }),
  // 获取特定目标的点赞列表
  getTargetLikes: (targetType, targetId, params) => api.get(`/social-like/target/${targetType}/${targetId}`, { params })
}

// 关注管理API
export const socialFollowAPI = {
  // 切换关注状态
  toggleFollow: (data) => api.post('/social-follow/toggle', data),
  // 检查关注状态
  checkFollow: (data) => api.post('/social-follow/check', data),
  // 获取粉丝列表
  getFollowers: (params) => api.get('/social-follow/followers', { params }),
  // 获取关注列表
  getFollowing: (params) => api.get('/social-follow/following', { params }),
  // 获取用户社区统计
  getUserSocialStats: (userId) => api.get(`/social-follow/stats/${userId}`)
} 