<template>
  <div class="menu-management">
    <!-- 搜索栏和操作栏 -->
    <div class="search-and-action-bar">
      <a-form layout="inline" :model="searchForm" @submit="handleSearch" class="search-form">
        <a-form-item label="菜单名称">
          <a-input
              v-model:value="searchForm.keyword"
              placeholder="请输入菜单名称"
              style="width: 200px;"
          />
        </a-form-item>
        <a-form-item>
          <a-button type="primary" html-type="submit">搜索</a-button>
          <a-button style="margin-left: 8px;" @click="resetSearch">重置</a-button>
        </a-form-item>
      </a-form>
      
      <div class="action-buttons">
        <a-button type="primary" @click="showAddModal">
          <template #icon>
            <PlusOutlined/>
          </template>
          添加菜单
        </a-button>
      </div>
    </div>

    <!-- 菜单列表 -->
    <a-table
        :columns="columns"
        :data-source="menus"
        :loading="loading"
        :pagination="pagination"
        @change="handleTableChange"
        row-key="id"
        :scroll="{ x: 1200 }"
        :childrenColumnName="'children'"
        :defaultExpandAllRows="false"
        :expandRowByClick="false"
    >

      <template #bodyCell="{ column, record }">
        <template v-if="column.key === 'name'">
          <div class="menu-name" :style="{ paddingLeft: (record.level - 1) * 20 + 'px' }">
            <span class="menu-name-text">{{ record.name }}</span>
            <a-tag 
              v-if="record.level > 1" 
              size="small" 
              color="blue" 
              style="margin-left: 8px; font-size: 10px;"
            >
              L{{ record.level }}
            </a-tag>
          </div>
        </template>
        
        <template v-else-if="column.key === 'icon'">
          <div class="menu-icon">
            <span v-if="record.icon" class="icon-preview">
              <component :is="getIconComponent(record.icon)"/>
              <span class="icon-text">{{ record.icon }}</span>
            </span>
            <span v-else class="no-icon">-</span>
          </div>
        </template>

        <template v-else-if="column.key === 'menu_type'">
          <a-tag :color="getMenuTypeColor(record.menu_type)">
            {{ getMenuTypeText(record.menu_type) }}
          </a-tag>
        </template>

        <template v-else-if="column.key === 'status'">
          <a-tag :color="record.status === 1 ? 'green' : 'red'">
            {{ record.status === 1 ? '启用' : '禁用' }}
          </a-tag>
        </template>

        <template v-else-if="column.key === 'is_visible'">
          <a-tag :color="record.is_visible === 1 ? 'blue' : 'orange'">
            {{ record.is_visible === 1 ? '显示' : '隐藏' }}
          </a-tag>
        </template>

        <template v-else-if="column.key === 'path'">
          <div class="path-cell">
            <span class="path-text">{{ record.path || '-' }}</span>
          </div>
        </template>

        <template v-else-if="column.key === 'component'">
          <div class="component-cell">
            <span class="component-text">{{ record.component || '-' }}</span>
          </div>
        </template>

        <template v-else-if="column.key === 'permission'">
          <div class="permission-cell">
            <span class="permission-text">{{ record.permission || '-' }}</span>
          </div>
        </template>

        <template v-else-if="column.key === 'action'">
          <a-space>
            <a-button type="link" size="small" @click="editMenu(record)">
              编辑
            </a-button>
            <a-button type="link" size="small" @click="viewMenu(record)">
              查看
            </a-button>
            
            <!-- 快捷添加按钮 -->
            <a-button 
              v-if="canAddChildren(record)" 
              type="link" 
              size="small" 
              style="color: #52c41a;"
              @click="handleQuickAdd(record)"
            >
              添加
            </a-button>
            
            <a-popconfirm
                title="确定要删除这个菜单吗？"
                @confirm="deleteMenu(record.id)"
            >
              <a-button type="link" size="small" danger>
                删除
              </a-button>
            </a-popconfirm>
          </a-space>
        </template>
      </template>
    </a-table>

    <!-- 添加/编辑菜单弹窗 -->
    <a-modal
        v-model:open="modalVisible"
        :title="modalTitle"
        @ok="handleModalOk"
        @cancel="handleModalCancel"
        width="800px"
    >
      <a-form
          ref="menuFormRef"
          :model="menuForm"
          :rules="menuFormRules"
          layout="vertical"
      >
        <a-row :gutter="16">
          <a-col :span="12">
            <a-form-item label="菜单名称" name="name">
              <a-input v-model:value="menuForm.name" placeholder="请输入菜单名称"/>
            </a-form-item>
          </a-col>
          <a-col :span="12">
            <a-form-item label="菜单图标" name="icon">
              <a-input v-model:value="menuForm.icon" placeholder="请输入菜单图标"/>
            </a-form-item>
          </a-col>
        </a-row>

        <a-row :gutter="16">
          <a-col :span="12">
            <a-form-item label="路由路径" name="path">
              <a-input v-model:value="menuForm.path" placeholder="请输入路由路径"/>
            </a-form-item>
          </a-col>
          <a-col :span="12">
            <a-form-item label="组件路径" name="component">
              <a-input v-model:value="menuForm.component" placeholder="请输入组件路径"/>
            </a-form-item>
          </a-col>
        </a-row>

        <a-row :gutter="16">
          <a-col :span="12">
            <a-form-item label="上级菜单" name="parent_id">
              <a-select
                  v-model:value="menuForm.parent_id"
                  placeholder="请选择上级菜单"
                  allow-clear
              >
                <a-select-option value="">无 (顶级菜单)</a-select-option>
                <a-select-option v-for="item in parentMenus" :key="item.id" :value="item.id">
                  {{ item.name }}
                </a-select-option>
              </a-select>
            </a-form-item>
          </a-col>
          <a-col :span="12">
            <a-form-item label="菜单类型" name="menu_type">
              <a-select 
                v-model:value="menuForm.menu_type" 
                placeholder="请选择菜单类型"
                @change="updateFormRules"
              >
                <a-select-option :value="0">目录</a-select-option>
                <a-select-option :value="1">菜单</a-select-option>
                <a-select-option :value="2">按钮</a-select-option>
              </a-select>
            </a-form-item>
          </a-col>
        </a-row>

        <a-row :gutter="16">
          <a-col :span="8">
            <a-form-item label="排序" name="sort_order">
              <a-input-number
                  v-model:value="menuForm.sort_order"
                  placeholder="请输入排序值"
                  style="width: 100%;"
                  :min="0"
              />
            </a-form-item>
          </a-col>
          <a-col :span="8">
            <a-form-item label="权限标识" name="permission">
              <a-input v-model:value="menuForm.permission" placeholder="请输入权限标识"/>
            </a-form-item>
          </a-col>
          <a-col :span="8">
            <a-form-item label="菜单层级" name="level">
              <a-input-number
                  v-model:value="menuForm.level"
                  placeholder="请输入菜单层级"
                  style="width: 100%;"
                  :min="1"
                  :max="3"
              />
            </a-form-item>
          </a-col>
        </a-row>

        <a-row :gutter="16">
          <a-col :span="8">
            <a-form-item label="是否显示" name="is_visible">
              <a-switch
                  v-model:checked="menuForm.is_visible"
                  :checked-value="1"
                  :un-checked-value="0"
                  checked-children="显示"
                  un-checked-children="隐藏"
              />
            </a-form-item>
          </a-col>
          <a-col :span="8">
            <a-form-item label="是否缓存" name="is_cache">
              <a-switch
                  v-model:checked="menuForm.is_cache"
                  :checked-value="1"
                  :un-checked-value="0"
                  checked-children="是"
                  un-checked-children="否"
              />
            </a-form-item>
          </a-col>
          <a-col :span="8">
            <a-form-item label="是否外链" name="is_external">
              <a-switch
                  v-model:checked="menuForm.is_external"
                  :checked-value="1"
                  :un-checked-value="0"
                  checked-children="是"
                  un-checked-children="否"
              />
            </a-form-item>
          </a-col>
        </a-row>

        <a-form-item label="状态" name="status">
          <a-radio-group v-model:value="menuForm.status">
            <a-radio :value="1">启用</a-radio>
            <a-radio :value="0">禁用</a-radio>
          </a-radio-group>
        </a-form-item>

        <a-form-item label="备注" name="remark">
          <a-textarea
              v-model:value="menuForm.remark"
              placeholder="请输入备注信息（可选）"
              :rows="3"
          />
        </a-form-item>

        <!-- 菜单类型提示 -->
        <a-alert 
          v-if="menuForm.menu_type === 2" 
          message="按钮类型菜单" 
          description="按钮类型菜单需要填写权限标识，用于权限控制。按钮不能再添加子菜单。" 
          type="info" 
          show-icon 
          style="margin-bottom: 16px;"
        />
        <a-alert 
          v-else-if="menuForm.menu_type === 0" 
          message="目录类型菜单" 
          description="目录类型菜单主要用于分组，可以在其下添加子菜单。" 
          type="info" 
          show-icon 
          style="margin-bottom: 16px;"
        />
        <a-alert 
          v-else-if="menuForm.menu_type === 1" 
          message="菜单类型" 
          description="菜单类型可以配置路由和组件，可以在其下添加按钮。" 
          type="info" 
          show-icon 
          style="margin-bottom: 16px;"
        />
      </a-form>
    </a-modal>

    <!-- 查看菜单详情弹窗 -->
    <a-modal
        v-model:open="viewModalVisible"
        title="菜单详情"
        :footer="null"
        width="600px"
    >
      <div v-if="currentMenu" class="menu-detail">
        <div class="detail-header">
          <h3>{{ currentMenu.name || '' }}</h3>
          <div class="meta-info">
            <a-tag :color="getMenuTypeColor(currentMenu.menu_type)">
              {{ getMenuTypeText(currentMenu.menu_type) }}
            </a-tag>
            <a-tag :color="currentMenu.status === 1 ? 'green' : 'red'">
              {{ currentMenu.status === 1 ? '启用' : '禁用' }}
            </a-tag>
            <a-tag :color="currentMenu.is_visible === 1 ? 'blue' : 'orange'">
              {{ currentMenu.is_visible === 1 ? '显示' : '隐藏' }}
            </a-tag>
          </div>
        </div>

        <a-divider/>

        <div class="detail-section">
          <a-descriptions bordered :column="2">
            <a-descriptions-item label="菜单名称">{{ currentMenu.name || '-' }}</a-descriptions-item>
            <a-descriptions-item label="菜单图标">
              <span v-if="currentMenu.icon">
                <component :is="getIconComponent(currentMenu.icon)"/>
                {{ currentMenu.icon }}
              </span>
              <span v-else>-</span>
            </a-descriptions-item>
            <a-descriptions-item label="路由路径">{{ currentMenu.path || '-' }}</a-descriptions-item>
            <a-descriptions-item label="组件路径">{{ currentMenu.component || '-' }}</a-descriptions-item>
            <a-descriptions-item label="权限标识">{{ currentMenu.permission || '-' }}</a-descriptions-item>
            <a-descriptions-item label="排序">{{ currentMenu.sort_order || '0' }}</a-descriptions-item>
            <a-descriptions-item label="菜单层级">{{ currentMenu.level || '1' }}</a-descriptions-item>
            <a-descriptions-item label="是否缓存">{{ currentMenu.is_cache === 1 ? '是' : '否' }}</a-descriptions-item>
            <a-descriptions-item label="是否外链">{{
                currentMenu.is_external === 1 ? '是' : '否'
              }}
            </a-descriptions-item>
            <a-descriptions-item label="备注" :span="2">{{ currentMenu.remark || '-' }}</a-descriptions-item>
          </a-descriptions>
        </div>
      </div>
    </a-modal>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted, computed } from 'vue'
import { message } from 'ant-design-vue'
import { PlusOutlined } from '@ant-design/icons-vue'
import { menuAPI } from '@/api'

// 响应式数据
const loading = ref(false)
const menus = ref([])
const parentMenus = ref([]) // 用于存储可选的父级菜单
const modalVisible = ref(false)
const viewModalVisible = ref(false)
const isEdit = ref(false)
const currentMenu = ref(null)
const menuFormRef = ref()

const searchForm = reactive({
  keyword: ''
})

const menuForm = reactive({
  name: '',
  path: '',
  icon: '',
  parent_id: '',
  level: 1,
  sort_order: 0,
  menu_type: 1,
  permission: '',
  component: '',
  is_external: 0,
  is_visible: 1,
  is_cache: 0,
  status: 1,
  remark: ''
})

const pagination = reactive({
  current: 1,
  pageSize: 10,
  total: 0,
  showSizeChanger: true,
  showQuickJumper: true,
  showTotal: (total) => `共 ${total} 条记录`
})

const columns = [
  {
    title: '菜单名称',
    dataIndex: 'name',
    key: 'name',
    width: 280,
    fixed: 'left'
  },
  {
    title: '图标',
    dataIndex: 'icon',
    key: 'icon',
    width: 120
  },
  {
    title: '排序',
    dataIndex: 'sort_order',
    key: 'sort_order',
    width: 80
  },
  {
    title: '权限标识',
    dataIndex: 'permission',
    key: 'permission',
    width: 150
  },
  {
    title: '路由路径',
    dataIndex: 'path',
    key: 'path',
    width: 150
  },
  {
    title: '组件路径',
    dataIndex: 'component',
    key: 'component',
    width: 150
  },
  {
    title: '类型',
    dataIndex: 'menu_type',
    key: 'menu_type',
    width: 80
  },
  {
    title: '状态',
    dataIndex: 'status',
    key: 'status',
    width: 80
  },
  {
    title: '可见',
    dataIndex: 'is_visible',
    key: 'is_visible',
    width: 80
  },
  {
    title: '操作',
    key: 'action',
    width: 210,
    fixed: 'right'
  }
]

const menuFormRules = reactive({
  name: [
    { required: true, message: '请输入菜单名称', trigger: 'blur' }
  ],
  menu_type: [
    { required: true, message: '请选择菜单类型', trigger: 'change' }
  ],
  status: [
    { required: true, message: '请选择状态', trigger: 'change' }
  ],
  permission: [
    { required: false, message: '请输入权限标识', trigger: 'blur' }
  ]
})

// 计算属性
const modalTitle = computed(() => isEdit.value ? '编辑菜单' : '添加菜单')

// 获取菜单列表
const fetchMenus = async () => {
  loading.value = true
  try {
    const params = {
      page: pagination.current,
      per_page: pagination.pageSize,
      keyword: searchForm.keyword
    }

    const result = await menuAPI.getMenus(params)
    if (result.code === 200) {
      menus.value = result.data.list || []
      pagination.total = result.data.total || 0
      
      // 如果是树形结构，调整分页显示
      if (result.data.is_tree) {
        // 树形结构时显示总的菜单项数量
        pagination.showTotal = (total) => `共 ${result.data.total_items || total} 条记录`
      } else {
        // 搜索时显示搜索结果数量
        pagination.showTotal = (total) => `共 ${total} 条搜索结果`
      }
    }
  } catch (error) {
    console.error('获取菜单列表失败:', error)
    message.error('获取菜单列表失败')
  } finally {
    loading.value = false
  }
}

// 获取父级菜单列表（用于下拉选择）
const fetchParentMenus = async () => {
  try {
    const result = await menuAPI.getMenuTree()
    if (result.code === 200) {
      // 扁平化菜单树，只获取目录和菜单类型作为父级菜单选项
      const flattenMenus = (menus, level = 1) => {
        let result = []
        menus.forEach(menu => {
          if (menu.menu_type === 0 || menu.menu_type === 1) { // 目录或菜单
            result.push({
              id: menu.id,
              name: '　'.repeat(level - 1) + menu.name, // 使用全角空格缩进
              level: level,
              menu_type: menu.menu_type
            })
          }
          if (menu.children && menu.children.length > 0) {
            result = result.concat(flattenMenus(menu.children, level + 1))
          }
        })
        return result
      }
      
      parentMenus.value = flattenMenus(result.data)
    }
  } catch (error) {
    console.error('获取父级菜单列表失败:', error)
    message.error('获取父级菜单列表失败')
  }
}

// 搜索
const handleSearch = () => {
  pagination.current = 1
  fetchMenus()
}

// 重置搜索
const resetSearch = () => {
  Object.assign(searchForm, {
    keyword: ''
  })
  pagination.current = 1
  fetchMenus()
}

// 表格分页改变
const handleTableChange = (pag) => {
  pagination.current = pag.current
  pagination.pageSize = pag.pageSize
  fetchMenus()
}

// 显示添加模态框
const showAddModal = (parentMenu = null, childType = null) => {
  isEdit.value = false
  modalVisible.value = true
  resetMenuForm()
  
  // 如果是快捷添加，设置默认值
  if (parentMenu && childType) {
    menuForm.parent_id = parentMenu.id
    menuForm.level = (parentMenu.level || 1) + 1
    menuForm.menu_type = childType === 'menu' ? 1 : 2 // 1=菜单, 2=按钮
    
    // 根据类型设置必填规则
    updateFormRules(menuForm.menu_type)
  } else {
    // 重置规则为默认
    updateFormRules(1)
  }
  
  // 获取父级菜单选项
  fetchParentMenus()
}

// 编辑菜单
const editMenu = (menu) => {
  isEdit.value = true
  modalVisible.value = true

  // 获取父级菜单选项
  fetchParentMenus()

  // 填充表单数据
  Object.keys(menuForm).forEach(key => {
    if (menu[key] !== undefined) {
      menuForm[key] = menu[key]
    }
  })
  menuForm.id = menu.id
  
  // 根据菜单类型更新验证规则
  updateFormRules(menu.menu_type)
}

// 查看菜单
const viewMenu = (menu) => {
  currentMenu.value = menu
  viewModalVisible.value = true
}

// 删除菜单
const deleteMenu = async (id) => {
  try {
    const result = await menuAPI.deleteMenu(id)
    if (result.code === 200) {
      message.success('删除成功')
      fetchMenus()
    } else {
      message.error(result.message || '删除失败')
    }
  } catch (error) {
    console.error('删除菜单失败:', error)
    message.error('删除菜单失败')
  }
}

// 模态框确定
const handleModalOk = async () => {
  try {
    await menuFormRef.value.validate()

    const data = { ...menuForm }
    delete data.id

    if (isEdit.value) {
      // 编辑菜单
      const result = await menuAPI.updateMenu(menuForm.id, data)
      if (result.code === 200) {
        message.success('更新成功')
        modalVisible.value = false
        fetchMenus()
      } else {
        message.error(result.message || '更新失败')
      }
    } else {
      // 创建菜单
      const result = await menuAPI.createMenu(data)
      if (result.code === 200 || result.code === 201) {
        message.success('创建成功')
        modalVisible.value = false
        fetchMenus()
      } else {
        message.error(result.message || '创建失败')
      }
    }
  } catch (error) {
    console.error('表单验证失败:', error)
  }
}

// 模态框取消
const handleModalCancel = () => {
  modalVisible.value = false
  resetMenuForm()
}

// 重置菜单表单
const resetMenuForm = () => {
  Object.assign(menuForm, {
    name: '',
    path: '',
    icon: '',
    parent_id: '',
    level: 1,
    sort_order: 0,
    menu_type: 1,
    permission: '',
    component: '',
    is_external: 0,
    is_visible: 1,
    is_cache: 0,
    status: 1,
    remark: ''
  })
  menuFormRef.value?.resetFields()
}

// 获取菜单类型颜色
const getMenuTypeColor = (type) => {
  if (type === undefined || type === null) return 'default'
  const colorMap = {
    0: 'blue',   // 目录
    1: 'green',  // 菜单
    2: 'orange'  // 按钮
  }
  return colorMap[type] || 'default'
}

// 获取菜单类型文本
const getMenuTypeText = (type) => {
  if (type === undefined || type === null) return '未知'
  const textMap = {
    0: '目录',
    1: '菜单',
    2: '按钮'
  }
  return textMap[type] || '未知'
}

// 获取图标组件
const getIconComponent = (iconName) => {
  // 这里可以根据实际情况返回对应的图标组件
  // 由于图标可能是字符串，暂时返回null
  return null
}

// 判断是否可以添加子项
const canAddChildren = (record) => {
  // 目录可以添加菜单，菜单可以添加按钮，按钮不能添加子项
  return record.menu_type === 0 || record.menu_type === 1
}

// 快捷添加处理
const handleQuickAdd = (parentRecord) => {
  // 根据父级菜单类型决定要添加的子项类型
  let childType
  if (parentRecord.menu_type === 0) {
    // 目录下只能添加菜单
    childType = 'menu'
  } else if (parentRecord.menu_type === 1) {
    // 菜单下只能添加按钮
    childType = 'button'
  }
  showAddModal(parentRecord, childType)
}

// 更新表单验证规则
const updateFormRules = (menuType) => {
  // 按钮类型时权限标识必填
  if (menuType === 2) {
    menuFormRules.permission = [
      { required: true, message: '请输入权限标识', trigger: 'blur' }
    ]
  } else {
    menuFormRules.permission = [
      { required: false, message: '请输入权限标识', trigger: 'blur' }
    ]
  }
}

// 生命周期
onMounted(() => {
  fetchMenus()
})
</script>

<style lang="scss" scoped>
.menu-management {
  padding: 0;
}

.search-and-action-bar {
  background: white;
  padding: 12px;
  border-radius: 4px;
  margin-bottom: 12px;
  box-shadow: 0 1px 4px rgba(0, 0, 0, 0.1);
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  flex-wrap: wrap;
  gap: 12px;
}

.search-form {
  flex: 1;
  min-width: 0;

  .ant-form-item {
    margin-bottom: 0;

    &:last-child {
      margin-bottom: 0;
    }
  }
}

.action-buttons {
  flex-shrink: 0;
}

.menu-icon {
  display: flex;
  align-items: center;
  gap: 8px;

  .icon-preview {
    display: flex;
    align-items: center;
    gap: 4px;
    color: #1890ff;

    .icon-text {
      font-size: 12px;
      color: #666;
    }
  }

  .no-icon {
    color: #ccc;
    font-style: italic;
  }
}

.path-cell,
.component-cell,
.permission-cell {
  max-width: 130px;

  .path-text,
  .component-text,
  .permission-text {
    display: -webkit-box;
    -webkit-line-clamp: 1;
    -webkit-box-orient: vertical;
    overflow: hidden;
    font-size: 12px;
    line-height: 1.4;
    color: #666;
  }
}

.menu-name {
  display: flex;
  align-items: center;
  position: relative;

  .menu-name-text {
    font-weight: 500;
  }
}

.menu-detail {
  padding: 12px 0;

  .detail-header {
    margin-bottom: 16px;

    h3 {
      margin: 0 0 12px 0;
      color: #1890ff;
      font-size: 18px;
    }

    .meta-info {
      display: flex;
      align-items: center;
      gap: 8px;
      flex-wrap: wrap;
    }
  }

  .detail-section {
    margin-bottom: 16px;
  }
}



/* 响应式样式 */
@media (max-width: 768px) {
  .menu-management {
    padding: 8px;
  }

  .search-and-action-bar {
    padding: 8px;
    margin-bottom: 8px;
    flex-direction: column;
    align-items: stretch;

    .search-form {
      .ant-form {
        flex-direction: column;
      }

      .ant-form-item {
        margin-bottom: 8px;

        &:last-child {
          margin-bottom: 0;
        }
      }
    }

    .action-buttons {
      width: 100%;

      .ant-btn {
        width: 100%;
      }
    }
  }

  .path-cell,
  .component-cell,
  .permission-cell {
    max-width: 100px;
  }

  .meta-info {
    flex-direction: column !important;
    align-items: flex-start !important;
    gap: 4px !important;
  }
}

@media (max-width: 576px) {
  .search-and-action-bar {
    padding: 6px;

    .search-form {
      .ant-form-item {
        label {
          font-size: 13px;
        }
      }

      .ant-input {
        font-size: 13px;
      }
    }
  }

  .path-cell,
  .component-cell,
  .permission-cell {
    max-width: 80px;
  }

  .icon-text {
    font-size: 11px;
  }
}
</style> 