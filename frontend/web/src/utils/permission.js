/**
 * 权限控制工具类
 * 提供角色检查、权限验证、路由守卫等功能
 */

// 角色常量定义
export const ROLES = {
    ADMIN: 'admin',
    MANAGER: 'manager',
    USER: 'user',
    COUNSELOR: 'counselor',
    CONSULTANT: 'consultant'
}

// 权限常量定义
export const PERMISSIONS = {
    // 用户管理
    USER_VIEW: 'user:view',
    USER_CREATE: 'user:create',
    USER_EDIT: 'user:edit',
    USER_DELETE: 'user:delete',
    
    // 咨询师管理
    COUNSELOR_VIEW: 'counselor:view',
    COUNSELOR_CREATE: 'counselor:create',
    COUNSELOR_EDIT: 'counselor:edit',
    COUNSELOR_DELETE: 'counselor:delete',
    
    // 咨询人管理
    CONSULTANT_VIEW: 'consultant:view',
    CONSULTANT_CREATE: 'consultant:create',
    CONSULTANT_EDIT: 'consultant:edit',
    CONSULTANT_DELETE: 'consultant:delete',
    
    // 预约管理
    APPOINTMENT_VIEW: 'appointment:view',
    APPOINTMENT_CREATE: 'appointment:create',
    APPOINTMENT_EDIT: 'appointment:edit',
    APPOINTMENT_DELETE: 'appointment:delete',
    
    // 课程管理
    COURSE_VIEW: 'course:view',
    COURSE_CREATE: 'course:create',
    COURSE_EDIT: 'course:edit',
    COURSE_DELETE: 'course:delete',
    
    // 订单管理
    ORDER_VIEW: 'order:view',
    ORDER_CREATE: 'order:create',
    ORDER_EDIT: 'order:edit',
    ORDER_DELETE: 'order:delete',
    
    // 系统管理
    SYSTEM_CONFIG: 'system:config',
    SYSTEM_LOG: 'system:log',
    SYSTEM_BACKUP: 'system:backup'
}

// 角色权限映射
const ROLE_PERMISSIONS = {
    [ROLES.ADMIN]: [
        // 管理员拥有所有权限
        ...Object.values(PERMISSIONS)
    ],
    [ROLES.MANAGER]: [
        // 管理者权限
        PERMISSIONS.USER_VIEW,
        PERMISSIONS.USER_CREATE,
        PERMISSIONS.USER_EDIT,
        PERMISSIONS.COUNSELOR_VIEW,
        PERMISSIONS.COUNSELOR_CREATE,
        PERMISSIONS.COUNSELOR_EDIT,
        PERMISSIONS.CONSULTANT_VIEW,
        PERMISSIONS.CONSULTANT_CREATE,
        PERMISSIONS.CONSULTANT_EDIT,
        PERMISSIONS.APPOINTMENT_VIEW,
        PERMISSIONS.APPOINTMENT_CREATE,
        PERMISSIONS.APPOINTMENT_EDIT,
        PERMISSIONS.COURSE_VIEW,
        PERMISSIONS.COURSE_CREATE,
        PERMISSIONS.COURSE_EDIT,
        PERMISSIONS.ORDER_VIEW,
        PERMISSIONS.ORDER_CREATE,
        PERMISSIONS.ORDER_EDIT
    ],
    [ROLES.USER]: [
        // 普通用户权限
        PERMISSIONS.CONSULTANT_VIEW,
        PERMISSIONS.CONSULTANT_CREATE,
        PERMISSIONS.CONSULTANT_EDIT,
        PERMISSIONS.APPOINTMENT_VIEW,
        PERMISSIONS.APPOINTMENT_CREATE,
        PERMISSIONS.COURSE_VIEW,
        PERMISSIONS.ORDER_VIEW,
        PERMISSIONS.ORDER_CREATE
    ],
    [ROLES.COUNSELOR]: [
        // 咨询师权限
        PERMISSIONS.COUNSELOR_VIEW,
        PERMISSIONS.APPOINTMENT_VIEW,
        PERMISSIONS.APPOINTMENT_EDIT,
        PERMISSIONS.CONSULTANT_VIEW,
        PERMISSIONS.COURSE_VIEW
    ],
    [ROLES.CONSULTANT]: [
        // 咨询人权限（基本查看权限）
        PERMISSIONS.APPOINTMENT_VIEW,
        PERMISSIONS.COURSE_VIEW
    ]
}

/**
 * 权限管理类
 */
class PermissionManager {
    constructor() {
        this.user = null
        this.roles = []
        this.permissions = []
        this.init()
    }

    /**
     * 初始化用户信息
     */
    init() {
        this.loadUserInfo()
    }

    /**
     * 从localStorage加载用户信息
     */
    loadUserInfo() {
        try {
            const userStr = localStorage.getItem('user')
            if (userStr) {
                this.user = JSON.parse(userStr)
                this.roles = this.user.roles || this.user.role ? [this.user.role] : []
                this.permissions = this.calculatePermissions()
            }
        } catch (error) {
            console.error('加载用户信息失败:', error)
            this.clearUserInfo()
        }
    }

    /**
     * 设置用户信息
     * @param {Object} user 用户信息
     */
    setUser(user) {
        this.user = user
        this.roles = user.roles || (user.role ? [user.role] : [])
        this.permissions = this.calculatePermissions()
        localStorage.setItem('user', JSON.stringify(user))
    }

    /**
     * 清除用户信息
     */
    clearUserInfo() {
        this.user = null
        this.roles = []
        this.permissions = []
        localStorage.removeItem('user')
        localStorage.removeItem('token')
    }

    /**
     * 计算用户权限
     * @returns {Array} 权限列表
     */
    calculatePermissions() {
        const permissions = new Set()
        
        this.roles.forEach(role => {
            const rolePermissions = ROLE_PERMISSIONS[role.toLowerCase()] || []
            rolePermissions.forEach(permission => permissions.add(permission))
        })

        // 如果用户有自定义权限，也添加进来
        if (this.user && this.user.permissions) {
            this.user.permissions.forEach(permission => permissions.add(permission))
        }

        return Array.from(permissions)
    }

    /**
     * 检查是否有指定角色
     * @param {string|Array} roles 角色或角色数组
     * @returns {boolean}
     */
    hasRole(roles) {
        if (!roles) return true
        if (!this.roles.length) return false

        const roleArray = Array.isArray(roles) ? roles : [roles]
        const userRoles = this.roles.map(role => role.toLowerCase())
        
        return roleArray.some(role => userRoles.includes(role.toLowerCase()))
    }

    /**
     * 检查是否有指定权限
     * @param {string|Array} permissions 权限或权限数组
     * @returns {boolean}
     */
    hasPermission(permissions) {
        if (!permissions) return true
        if (!this.permissions.length) return false

        const permissionArray = Array.isArray(permissions) ? permissions : [permissions]
        return permissionArray.some(permission => this.permissions.includes(permission))
    }

    /**
     * 检查是否为管理员
     * @returns {boolean}
     */
    isAdmin() {
        return this.hasRole(ROLES.ADMIN)
    }

    /**
     * 检查是否为管理者
     * @returns {boolean}
     */
    isManager() {
        return this.hasRole(ROLES.MANAGER)
    }

    /**
     * 检查是否为普通用户
     * @returns {boolean}
     */
    isUser() {
        return this.hasRole(ROLES.USER)
    }

    /**
     * 检查是否为咨询师
     * @returns {boolean}
     */
    isCounselor() {
        return this.hasRole(ROLES.COUNSELOR)
    }

    /**
     * 检查是否为咨询人
     * @returns {boolean}
     */
    isConsultant() {
        return this.hasRole(ROLES.CONSULTANT)
    }

    /**
     * 检查是否有管理权限（管理员或管理者）
     * @returns {boolean}
     */
    hasManagePermission() {
        return this.isAdmin() || this.isManager()
    }

    /**
     * 获取当前用户信息
     * @returns {Object|null}
     */
    getUser() {
        return this.user
    }

    /**
     * 获取当前用户角色
     * @returns {Array}
     */
    getRoles() {
        return this.roles
    }

    /**
     * 获取当前用户权限
     * @returns {Array}
     */
    getPermissions() {
        return this.permissions
    }

    /**
     * 检查是否已登录
     * @returns {boolean}
     */
    isLoggedIn() {
        return !!this.user && !!localStorage.getItem('token')
    }
}

// 创建全局权限管理实例
const permissionManager = new PermissionManager()

// 导出权限检查函数
export const hasRole = (roles) => permissionManager.hasRole(roles)
export const hasPermission = (permissions) => permissionManager.hasPermission(permissions)
export const isAdmin = () => permissionManager.isAdmin()
export const isManager = () => permissionManager.isManager()
export const isUser = () => permissionManager.isUser()
export const isCounselor = () => permissionManager.isCounselor()
export const isConsultant = () => permissionManager.isConsultant()
export const hasManagePermission = () => permissionManager.hasManagePermission()
export const isLoggedIn = () => permissionManager.isLoggedIn()
export const getUser = () => permissionManager.getUser()
export const getRoles = () => permissionManager.getRoles()
export const getPermissions = () => permissionManager.getPermissions()
export const setUser = (user) => permissionManager.setUser(user)
export const clearUserInfo = () => permissionManager.clearUserInfo()

/**
 * 路由守卫函数
 * @param {Object} route 路由对象
 * @param {Array} requiredRoles 需要的角色
 * @param {Array} requiredPermissions 需要的权限
 * @returns {boolean}
 */
export const checkRoutePermission = (route, requiredRoles = [], requiredPermissions = []) => {
    // 检查是否已登录
    if (!isLoggedIn()) {
        return false
    }

    // 检查角色权限
    if (requiredRoles.length > 0 && !hasRole(requiredRoles)) {
        return false
    }

    // 检查功能权限
    if (requiredPermissions.length > 0 && !hasPermission(requiredPermissions)) {
        return false
    }

    return true
}

/**
 * Vue指令：v-permission
 * 用法：v-permission="['admin', 'manager']" 或 v-permission="'admin'"
 */
export const permissionDirective = {
    mounted(el, binding) {
        const requiredPermissions = binding.value
        if (!hasPermission(requiredPermissions)) {
            el.style.display = 'none'
        }
    },
    updated(el, binding) {
        const requiredPermissions = binding.value
        if (!hasPermission(requiredPermissions)) {
            el.style.display = 'none'
        } else {
            el.style.display = ''
        }
    }
}

/**
 * Vue指令：v-role
 * 用法：v-role="['admin', 'manager']" 或 v-role="'admin'"
 */
export const roleDirective = {
    mounted(el, binding) {
        const requiredRoles = binding.value
        if (!hasRole(requiredRoles)) {
            el.style.display = 'none'
        }
    },
    updated(el, binding) {
        const requiredRoles = binding.value
        if (!hasRole(requiredRoles)) {
            el.style.display = 'none'
        } else {
            el.style.display = ''
        }
    }
}

export default permissionManager 