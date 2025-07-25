/**
 * 网络请求工具类
 * 基于uni.request的二次封装，使用类似axios的API风格
 */
import config from './config';
import { getToken } from './auth';

// 基础URL配置
const BASE_URL = config.api.baseUrl;

// 请求默认超时时间
const TIMEOUT = config.api.timeout;

// 请求队列，用于取消请求
let requestQueue = [];

// token存储
let accessToken = getToken();

/**
 * 刷新token方法
 */
const refreshToken = () => {
    return new Promise((resolve, reject) => {
        const refreshTokenValue = uni.getStorageSync(config.storage.refreshTokenKey);
        if (!refreshTokenValue) {
            reject(new Error('refreshToken不存在，请重新登录'));
            return;
        }

        uni.request({
            url: `${BASE_URL}/user/refresh-token`,
            method: 'POST',
            data: { refreshToken: refreshTokenValue },
            success: (res) => {
                if (res.statusCode === 200 && res.data.code === 0) {
                    const { accessToken: newToken, refreshToken: newRefreshToken } = res.data.data;
                    // 存储新token
                    uni.setStorageSync(config.storage.tokenKey, newToken);
                    uni.setStorageSync(config.storage.refreshTokenKey, newRefreshToken);
                    accessToken = newToken;
                    resolve(newToken);
                } else {
                    reject(new Error('刷新Token失败，请重新登录'));
                }
            },
            fail: () => {
                reject(new Error('刷新Token请求失败，请检查网络'));
            }
        });
    });
};

/**
 * 请求拦截器
 * @param {Object} options 请求配置
 * @returns {Object} 修改后的请求配置
 */
const requestInterceptor = (options) => {
    // 处理请求地址
    if (!options.url.startsWith('http')) {
        options.url = BASE_URL + options.url;
    }

    // 处理请求头
    options.header = options.headers || options.header || {};
    if (!options.header['Content-Type'] && !options.header['content-type']) {
        options.header['Content-Type'] = 'application/json';
    }

    // 添加token
    const token = accessToken || uni.getStorageSync(config.storage.tokenKey);
    if (token) {
        options.header['Authorization'] = `Bearer ${token}`;
    }

    // 设置请求方法，默认为GET
    options.method = options.method || 'GET';

    // 处理请求参数，GET请求参数放在data，其他请求类型放在params
    if (options.method.toUpperCase() === 'GET' && options.params) {
        options.data = options.params;
    } else if (options.data === undefined) {
        options.data = {};
    }

    // 设置超时时间
    options.timeout = options.timeout || TIMEOUT;

    return options;
};

/**
 * 响应拦截器
 * @param {Object} response 响应对象
 * @param {Object} options 请求配置
 * @returns {Promise} 处理后的响应
 */
const responseInterceptor = (response, options) => {
    return new Promise((resolve, reject) => {
        // 从队列中移除请求
        removeRequest(options);

        // 判断日志是否启用
        const shouldLog = config.api.enableLog;

        // 请求日志记录
        if (shouldLog) {
            console.info(`请求URL: ${options.url}`, `状态码: ${response.statusCode}`);
        }

        // 请求成功
        if (response.statusCode >= 200 && response.statusCode < 300) {
            // 检查业务状态码
            if (response.data && response.data.code === 200) {
                resolve(response.data.data);
            } else {
                // 业务错误
                const message = response.data?.message || '服务器返回错误数据';
                uni.showToast({
                    title: message,
                    icon: 'none'
                });

                // 创建类似axios的错误对象
                const error = new Error(message);
                error.response = response;
                error.config = options;
                error.status = response.statusCode;
                error.data = response.data;

                reject(error);
            }
        }
        // token过期(401)
        else if (response.statusCode === 401) {
            // 判断是否是刷新token的请求
            if (options.url.includes('/refresh-token')) {
                // 刷新token也失败，需要重新登录
                uni.clearStorageSync();
                uni.showToast({
                    title: '登录已过期，请重新登录',
                    icon: 'none'
                });

                // 跳转到登录页
                setTimeout(() => {
                    uni.reLaunch({
                        url: '/pages/login/index'
                    });
                }, 1500);

                const error = new Error('登录已过期，请重新登录');
                error.response = response;
                error.config = options;
                error.status = 401;

                reject(error);
            } else {
                // 尝试刷新token
                refreshToken().then(newToken => {
                    // 重新发起原请求
                    const newOptions = { ...options };
                    newOptions.header['Authorization'] = `Bearer ${newToken}`;
                    return request(newOptions);
                }).then(res => {
                    resolve(res);
                }).catch(err => {
                    reject(err);
                });
            }
        }
        // 服务器错误(500等)
        else if (response.statusCode >= 500) {
            const message = '服务器开小差了，请稍后再试';
            uni.showToast({
                title: message,
                icon: 'none'
            });

            const error = new Error(message);
            error.response = response;
            error.config = options;
            error.status = response.statusCode;

            reject(error);
        }
        // 其他错误
        else {
            let message;
            switch (response.statusCode) {
                case 400:
                    message = response.data?.message || '请求参数错误';
                    break;
                case 403:
                    message = '没有权限访问该资源';
                    break;
                case 404:
                    message = '请求的资源不存在';
                    break;
                case 429:
                    message = '请求过于频繁，请稍后再试';
                    break;
                default:
                    console.log(response);

                    message = `请求失败(${response.statusCode})`;
            }

            uni.showToast({
                title: message,
                icon: 'none'
            });

            const error = new Error(message);
            error.response = response;
            error.config = options;
            error.status = response.statusCode;

            reject(error);
        }
    });
};

/**
 * 将请求添加到队列
 * @param {Object} options 请求配置
 */
const addRequest = (options) => {
    const requestId = generateRequestId(options);
    options.requestId = requestId;
    requestQueue.push({ requestId, task: null });
    return options;
};

/**
 * 从队列中移除请求
 * @param {Object} options 请求配置
 */
const removeRequest = (options) => {
    const index = requestQueue.findIndex(item => item.requestId === options.requestId);
    if (index !== -1) {
        requestQueue.splice(index, 1);
    }
};

/**
 * 生成请求ID
 * @param {Object} options 请求配置
 * @returns {String} 请求ID
 */
const generateRequestId = (options) => {
    return `${options.method}-${options.url}-${JSON.stringify(options.data || {})}-${Date.now()}`;
};

/**
 * 主请求方法，类似axios的调用方式
 * @param {Object|String} options 请求配置或URL
 * @returns {Promise} 请求Promise
 */
const request = (options) => {
    // 支持直接传入URL字符串
    if (typeof options === 'string') {
        options = {
            url: options
        };
    }

    return new Promise((resolve, reject) => {
        try {
            // 添加到请求队列
            options = addRequest(options);

            // 请求拦截器处理
            options = requestInterceptor(options);

            // 判断日志是否启用
            const shouldLog = config.api.enableLog;

            // 打印请求日志
            if (shouldLog) {
                console.debug('发起请求:', options.method, options.url, options.data);
            }

            // 发起请求
            const task = uni.request({
                url: options.url,
                method: options.method,
                data: options.data,
                header: options.header,
                timeout: options.timeout,
                success: (response) => {
                    responseInterceptor(response, options)
                        .then(resolve)
                        .catch(reject);
                },
                fail: (error) => {
                    removeRequest(options);

                    // 判断日志是否启用
                    const shouldLog = config.api.enableLog;

                    // 请求日志记录
                    if (shouldLog) {
                        console.error('请求失败:', options.url, error);
                    }

                    // 网络错误处理
                    if (error.errMsg.includes('timeout')) {
                        uni.showToast({
                            title: '请求超时，请检查网络',
                            icon: 'none'
                        });
                    } else if (error.errMsg.includes('fail')) {
                        uni.showToast({
                            title: '网络连接失败，请检查网络设置',
                            icon: 'none'
                        });
                    }

                    // 创建类似axios的错误对象
                    const axiosError = new Error(error.errMsg || '请求失败');
                    axiosError.config = options;
                    axiosError.isNetworkError = true;
                    axiosError.request = task;

                    reject(axiosError);
                }
            });

            // 存储task引用，用于可能的取消操作
            const index = requestQueue.findIndex(item => item.requestId === options.requestId);
            if (index !== -1) {
                requestQueue[index].task = task;
            }
        } catch (error) {
            // 判断日志是否启用
            const shouldLog = config.api.enableLog;

            if (shouldLog) {
                console.error('请求异常:', error);
            }
            reject(error);
        }
    });
};

/**
 * 创建请求方法别名
 */
['get', 'delete', 'head', 'options'].forEach(method => {
    request[method] = (url, options = {}) => {
        return request({
            ...options,
            method: method.toUpperCase(),
            url
        });
    };
});

['post', 'put', 'patch'].forEach(method => {
    request[method] = (url, data, options = {}) => {
        return request({
            ...options,
            method: method.toUpperCase(),
            url,
            data
        });
    };
});

/**
 * 上传文件
 * @param {String} url 上传地址
 * @param {String} filePath 文件路径
 * @param {String} name 文件对应的key
 * @param {Object} formData 额外的表单数据
 * @param {Object} options 请求配置
 * @returns {Promise} 上传Promise
 */
request.upload = (url, filePath, name = 'file', formData = {}, options = {}) => {
    return new Promise((resolve, reject) => {
        // 处理请求地址
        if (!url.startsWith('http')) {
            url = BASE_URL + url;
        }

        // 处理请求头
        const token = accessToken || uni.getStorageSync(config.storage.tokenKey);
        const headers = options.headers || options.header || {};

        if (token) {
            headers['Authorization'] = `Bearer ${token}`;
        }

        // 显示上传进度
        uni.showLoading({
            title: '上传中...',
            mask: true
        });

        // 判断日志是否启用
        const shouldLog = config.api.enableLog;

        // 打印上传日志
        if (shouldLog) {
            console.debug('开始上传文件:', url, filePath);
        }

        // 开始上传
        const uploadTask = uni.uploadFile({
            url,
            filePath,
            name,
            formData,
            header: headers,
            success: (res) => {
                uni.hideLoading();

                if (res.statusCode >= 200 && res.statusCode < 300) {
                    // 解析响应数据
                    try {
                        const data = JSON.parse(res.data);
                        if (data.code === 0) {
                            if (shouldLog) {
                                console.info('文件上传成功:', url);
                            }
                            resolve(data.data);
                        } else {
                            uni.showToast({
                                title: data.message || '上传失败',
                                icon: 'none'
                            });
                            reject(new Error(data.message || '上传失败'));
                        }
                    } catch (error) {
                        uni.showToast({
                            title: '上传响应解析失败',
                            icon: 'none'
                        });
                        reject(error);
                    }
                } else if (res.statusCode === 401) {
                    uni.hideLoading();

                    // 尝试刷新token
                    refreshToken().then(newToken => {
                        headers['Authorization'] = `Bearer ${newToken}`;
                        // 重新上传
                        return request.upload(url, filePath, name, formData, { ...options, headers });
                    }).then(result => {
                        resolve(result);
                    }).catch(err => {
                        reject(err);
                    });
                } else {
                    uni.showToast({
                        title: `上传失败(${res.statusCode})`,
                        icon: 'none'
                    });
                    reject(new Error(`上传失败(${res.statusCode})`));
                }
            },
            fail: (err) => {
                uni.hideLoading();

                if (shouldLog) {
                    console.error('文件上传失败:', url, err);
                }

                uni.showToast({
                    title: '上传失败，请检查网络',
                    icon: 'none'
                });
                reject(err);
            }
        });

        // 监听上传进度
        uploadTask.onProgressUpdate((res) => {
            if (res.progress > 0) {
                uni.showLoading({
                    title: `上传中(${res.progress}%)`,
                    mask: true
                });

                // 如果提供了进度回调，则调用
                if (typeof options.onProgress === 'function') {
                    options.onProgress(res);
                }
            }
        });

        // 返回取消上传的方法
        if (typeof options.getTask === 'function') {
            options.getTask(uploadTask);
        }
    });
};

/**
 * 文件下载
 * @param {String} url 下载地址
 * @param {Object} options 请求配置
 * @returns {Promise} 下载Promise
 */
request.download = (url, options = {}) => {
    return new Promise((resolve, reject) => {
        // 处理请求地址
        if (!url.startsWith('http')) {
            url = BASE_URL + url;
        }

        // 处理请求头
        const token = accessToken || uni.getStorageSync(config.storage.tokenKey);
        const headers = options.headers || options.header || {};

        if (token) {
            headers['Authorization'] = `Bearer ${token}`;
        }

        // 显示下载进度
        uni.showLoading({
            title: '下载中...',
            mask: true
        });

        // 判断日志是否启用
        const shouldLog = config.api.enableLog;

        // 打印下载日志
        if (shouldLog) {
            console.debug('开始下载文件:', url);
        }

        // 开始下载
        const downloadTask = uni.downloadFile({
            url,
            header: headers,
            success: (res) => {
                uni.hideLoading();

                if (res.statusCode >= 200 && res.statusCode < 300) {
                    if (shouldLog) {
                        console.info('文件下载成功:', url);
                    }
                    resolve(res.tempFilePath);
                } else if (res.statusCode === 401) {
                    // 尝试刷新token
                    refreshToken().then(newToken => {
                        headers['Authorization'] = `Bearer ${newToken}`;
                        // 重新下载
                        return request.download(url, { ...options, headers });
                    }).then(result => {
                        resolve(result);
                    }).catch(err => {
                        reject(err);
                    });
                } else {
                    uni.showToast({
                        title: `下载失败(${res.statusCode})`,
                        icon: 'none'
                    });
                    reject(new Error(`下载失败(${res.statusCode})`));
                }
            },
            fail: (err) => {
                uni.hideLoading();

                if (shouldLog) {
                    console.error('文件下载失败:', url, err);
                }

                uni.showToast({
                    title: '下载失败，请检查网络',
                    icon: 'none'
                });
                reject(err);
            }
        });

        // 监听下载进度
        downloadTask.onProgressUpdate((res) => {
            if (res.progress > 0) {
                uni.showLoading({
                    title: `下载中(${res.progress}%)`,
                    mask: true
                });

                // 如果提供了进度回调，则调用
                if (typeof options.onProgress === 'function') {
                    options.onProgress(res);
                }
            }
        });

        // 返回取消下载的方法
        if (typeof options.getTask === 'function') {
            options.getTask(downloadTask);
        }
    });
};

/**
 * 取消所有请求
 */
request.cancelAllRequests = () => {
    requestQueue.forEach(item => {
        if (item.task && typeof item.task.abort === 'function') {
            item.task.abort();
        }
    });
    requestQueue = [];
};

/**
 * 设置token，用于登录后更新token
 * @param {String} token 
 */
request.setToken = (token) => {
    accessToken = token;
    uni.setStorageSync(config.storage.tokenKey, token);
};

/**
 * 清除token，用于退出登录
 */
request.clearToken = () => {
    accessToken = '';
    uni.removeStorageSync(config.storage.tokenKey);
    uni.removeStorageSync(config.storage.refreshTokenKey);
};

/**
 * 创建请求实例，类似axios.create
 * @param {Object} instanceConfig 实例配置
 * @returns {Function} 请求实例
 */
request.create = (instanceConfig = {}) => {
    const instance = (options) => {
        return request({
            ...instanceConfig,
            ...options
        });
    };

    // 复制方法
    for (const key in request) {
        if (Object.prototype.hasOwnProperty.call(request, key)) {
            instance[key] = request[key];
        }
    }

    // 添加method别名
    ['get', 'delete', 'head', 'options'].forEach(method => {
        instance[method] = (url, options = {}) => {
            return instance({
                ...options,
                method: method.toUpperCase(),
                url
            });
        };
    });

    ['post', 'put', 'patch'].forEach(method => {
        instance[method] = (url, data, options = {}) => {
            return instance({
                ...options,
                method: method.toUpperCase(),
                url,
                data
            });
        };
    });

    return instance;
};

export default request;
