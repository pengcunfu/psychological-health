/**
 * uni-app Promise 适配器
 * 用于将不支持 Promise 的 API 转换为支持 Promise 的形式
 */

// 添加全局拦截器
uni.addInterceptor({
  // 拦截并处理 API 的返回值
  returnValue (res) {
    // 检查返回值是否已经是 Promise
    // 1. 确保 res 存在且是对象或函数
    // 2. 检查是否具有 then 方法（是否是 thenable）
    if (!(!!res && (typeof res === "object" || typeof res === "function") && typeof res.then === "function")) {
      return res; // 如果不是 Promise，直接返回原始值
    }

    // 如果是 Promise，返回一个新的 Promise
    return new Promise((resolve, reject) => {
      res.then((res) => {
        // 处理空值情况
        if (!res) return resolve(res);
        
        // 处理返回数组的情况
        // res[0] 表示错误信息，res[1] 表示成功结果
        // 如果 res[0] 存在则表示有错误，调用 reject
        // 否则返回 res[1] 作为成功结果
        return res[0] ? reject(res[0]) : resolve(res[1]);
      });
    });
  },
});