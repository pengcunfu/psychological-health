/**
 * 配置工具
 * 小程序环境兼容的配置管理
 */

// 判断是否为开发环境（根据平台特性判断）
// 注意：微信开发者工具中会显示为development，真机预览/正式版为production
let ENV = 'development'; // 默认为开发环境

try {
  // 尝试获取当前运行环境
  const sysInfo = uni.getSystemInfoSync();
  if (sysInfo.platform === 'devtools') {
    // 开发者工具中视为开发环境
    ENV = 'development';
  } else {
    // 真机视为生产环境
    ENV = 'production';
  }
} catch (e) {
  console.error('获取系统信息失败', e);
}

// 开发环境配置
const DEV_CONFIG = {
  // API配置
  apiBaseUrl: 'http://127.0.0.1:3000/api',
  cdnBaseUrl: 'http://127.0.0.1:3000/static',
  wsUrl: 'ws://127.0.0.1:3000/ws',
  enableLog: true,
  enableDebug: true
};

// 生产环境配置
const PROD_CONFIG = {
  // API配置
  apiBaseUrl: 'https://api.meiguangxinli.com/api',
  cdnBaseUrl: 'https://cdn.meiguangxinli.com',
  wsUrl: 'wss://api.meiguangxinli.com/ws',
  enableLog: false,
  enableDebug: false
};

// 通用配置（不随环境变化）
const COMMON_CONFIG = {
  // 应用信息
  appName: '美光心理',
  appVersion: '1.0.0',
  
  // 请求超时时间(毫秒)
  timeout: 60000,
  
  // 微信小程序配置
  weappAppId: 'wx123456789',
  
  // 上传文件限制
  upload: {
    imageMaxSize: 10 * 1024 * 1024, // 10MB
    videoMaxSize: 100 * 1024 * 1024, // 100MB
    audioMaxSize: 20 * 1024 * 1024, // 20MB
    imageFormats: ['jpg', 'jpeg', 'png', 'gif', 'webp'],
    videoFormats: ['mp4', 'mov', 'avi', 'wmv'],
    audioFormats: ['mp3', 'wav', 'aac']
  },
  
  // 存储键名
  storage: {
    tokenKey: 'accessToken',
    refreshTokenKey: 'refreshToken',
    userInfoKey: 'userInfo',
    searchHistoryKey: 'searchHistory',
    settingsKey: 'appSettings'
  }
};

// 合并配置
const envConfig = ENV === 'development' ? DEV_CONFIG : PROD_CONFIG;

/**
 * 配置对象，包含所有配置项
 */
const config = {
  // 环境信息
  env: ENV,
  isDev: ENV === 'development',
  isProd: ENV === 'production',
  
  // 应用信息
  appName: COMMON_CONFIG.appName,
  appVersion: COMMON_CONFIG.appVersion,
  
  // API配置
  api: {
    baseUrl: envConfig.apiBaseUrl,
    timeout: COMMON_CONFIG.timeout,
    enableLog: envConfig.enableLog
  },
  
  // CDN配置
  cdn: {
    baseUrl: envConfig.cdnBaseUrl
  },
  
  // WebSocket配置
  ws: {
    url: envConfig.wsUrl
  },
  
  // 微信小程序配置
  weapp: {
    appId: COMMON_CONFIG.weappAppId
  },
  
  // 调试配置
  debug: {
    enabled: envConfig.enableDebug
  },
  
  // 上传文件配置
  upload: COMMON_CONFIG.upload,
  
  // 本地存储键名
  storage: COMMON_CONFIG.storage
};

/**
 * 日志函数，仅在开发环境或启用调试模式时输出
 */
const log = {
  info: (...args) => {
    if (config.debug.enabled) {
      console.info('[INFO]', ...args);
    }
  },
  warn: (...args) => {
    if (config.debug.enabled) {
      console.warn('[WARN]', ...args);
    }
  },
  error: (...args) => {
    if (config.debug.enabled) {
      console.error('[ERROR]', ...args);
    }
  },
  debug: (...args) => {
    if (config.debug.enabled) {
      console.debug('[DEBUG]', ...args);
    }
  }
};

// 添加日志功能到配置对象
config.log = log;

// 输出当前配置信息（仅在开发环境）
if (config.isDev) {
  console.log('[CONFIG] 当前环境:', config.env);
  console.log('[CONFIG] API地址:', config.api.baseUrl);
}

export default config; 