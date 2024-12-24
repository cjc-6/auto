<template>
  <div class="template-manage">
    <h3>命令模板管理</h3>

    <!-- 操作按钮 -->
    <div class="operation-bar" style="margin-bottom: 20px">
      <a-space>
        <a-button type="primary" @click="showAddModal">
          <template #icon><plus-outlined /></template>
          新建模板
        </a-button>
        <a-button @click="handleBatchDelete" danger>
          <template #icon><delete-outlined /></template>
          批量删除
        </a-button>
      </a-space>
    </div>

    <!-- 筛选条件 -->
    <a-card style="margin-bottom: 20px">
      <a-form layout="inline">
        <a-form-item label="模板名称">
          <a-input v-model:value="searchForm.name" placeholder="请输入模板名称" />
        </a-form-item>
        <a-form-item label="模板类型">
          <a-select v-model:value="searchForm.category" style="width: 160px" placeholder="请选择类型">
            <a-select-option value="system">系统管理</a-select-option>
            <a-select-option value="service">服务管理</a-select-option>
            <a-select-option value="network">网络管理</a-select-option>
            <a-select-option value="monitor">监控管理</a-select-option>
            <a-select-option value="security">安全管理</a-select-option>
          </a-select>
        </a-form-item>
        <a-form-item>
          <a-button type="primary" @click="handleSearch">查询</a-button>
          <a-button style="margin-left: 8px" @click="resetSearch">重置</a-button>
        </a-form-item>
      </a-form>
    </a-card>

    <!-- 模板列表 -->
    <a-card>
      <a-table 
        :columns="columns" 
        :data-source="tableData"
        :row-selection="{ selectedRowKeys: selectedRowKeys, onChange: onSelectChange }"
        :pagination="{ pageSize: 10 }"
      >
        <template #bodyCell="{ column, record }">
          <template v-if="column.key === 'category'">
            <a-tag :color="getCategoryColor(record.category)">
              {{ getCategoryText(record.category) }}
            </a-tag>
          </template>
          <template v-if="column.key === 'action'">
            <a-space>
              <a @click="showEditModal(record)">编辑</a>
              <a @click="handleCopy(record)">复制</a>
              <a-popconfirm
                title="确定要删除这条模板吗？"
                ok-text="确定"
                cancel-text="取消"
                @confirm="handleDelete(record)"
              >
                <a style="color: #ff4d4f">删除</a>
              </a-popconfirm>
            </a-space>
          </template>
        </template>
      </a-table>
    </a-card>

    <!-- 新建/编辑模板弹窗 -->
    <a-modal
      v-model:visible="modalVisible"
      :title="modalTitle"
      @ok="handleModalOk"
      width="800px"
    >
      <a-form :label-col="{ span: 4 }" :wrapper-col="{ span: 20 }">
        <a-form-item label="模板名称" required>
          <a-input v-model:value="formData.name" placeholder="请输入模板名称" />
        </a-form-item>
        <a-form-item label="模板类型" required>
          <a-select v-model:value="formData.category" placeholder="请选择类型">
            <a-select-option value="system">系统管理</a-select-option>
            <a-select-option value="service">服务管理</a-select-option>
            <a-select-option value="network">网络管理</a-select-option>
            <a-select-option value="monitor">监控管理</a-select-option>
            <a-select-option value="security">安全管理</a-select-option>
          </a-select>
        </a-form-item>
        <a-form-item label="命令内容" required>
          <a-textarea 
            v-model:value="formData.command" 
            :rows="6" 
            placeholder="请输入命令内容"
          />
        </a-form-item>
        <a-form-item label="描述">
          <a-textarea 
            v-model:value="formData.description" 
            :rows="4" 
            placeholder="请输入模板描述"
          />
        </a-form-item>
      </a-form>
    </a-modal>
  </div>
</template>

<script>
import { defineComponent, ref, reactive } from 'vue';
import { message } from 'ant-design-vue';
import {
  PlusOutlined,
  DeleteOutlined
} from '@ant-design/icons-vue';

export default defineComponent({
  components: {
    PlusOutlined,
    DeleteOutlined
  },
  setup() {
    const columns = [
      { title: '模板名称', dataIndex: 'name', key: 'name' },
      { title: '类型', dataIndex: 'category', key: 'category' },
      { title: '命令内容', dataIndex: 'command', key: 'command', ellipsis: true },
      { title: '描述', dataIndex: 'description', key: 'description', ellipsis: true },
      { title: '更新时间', dataIndex: 'updateTime', key: 'updateTime' },
      { title: '操作', key: 'action' },
    ];

    // 预设的命令模板数据
    const tableData = [
      {
        key: '1',
        name: '系统资源查看',
        category: 'system',
        command: 'top -bn1 | head -n 20\ndf -h\nfree -h\nw',
        description: '查看系统CPU、内存、磁盘使用情况和在线用户',
        updateTime: '2024-11-28 10:00:00',
      },
      {
        key: '2',
        name: 'Nginx服务管理',
        category: 'service',
        command: 'systemctl status nginx\nsystemctl restart nginx\nnginx -t',
        description: '查看Nginx状态、重启服务和检查配置',
        updateTime: '2024-11-22 09:50:00',
      },
      {
        key: '3',
        name: '网络连接检查',
        category: 'network',
        command: 'netstat -tunlp\nss -tunlp\nping -c 4 www.baidu.com',
        description: '查看网络连接状态和端口占用情况',
        updateTime: '2024-11-22 09:40:00',
      },
      {
        key: '4',
        name: '日志分析',
        category: 'monitor',
        command: 'tail -f /var/log/messages\ngrep -i error /var/log/syslog\njournalctl -xe',
        description: '实时查看系统日志和错误信息',
        updateTime: '2024-11-22 09:30:00',
      },
      {
        key: '5',
        name: '防火墙配置',
        category: 'security',
        command: 'firewall-cmd --list-all\nfirewall-cmd --add-port=80/tcp --permanent\nfirewall-cmd --reload',
        description: '查看和配置防火墙规则',
        updateTime: '2024-11-22 09:20:00',
      },
      {
        key: '6',
        name: '磁盘IO监控',
        category: 'monitor',
        command: 'iostat -xz 1 10\niotop -obn 5',
        description: '监控系统磁盘IO使用情况',
        updateTime: '2024-11-22 09:10:00',
      },
      {
        key: '7',
        name: 'Docker服务管理',
        category: 'service',
        command: 'docker ps -a\ndocker stats\ndocker system df',
        description: '查看Docker容器状态和资源使用情况',
        updateTime: '2024-11-26 09:00:00',
      },
      {
        key: '8',
        name: '系统用户管理',
        category: 'security',
        command: 'cat /etc/passwd\nw\nlast | head -n 10\nwho',
        description: '查看系统用户和登录情况',
        updateTime: '2024-11-25 08:50:00',
      }
    ];

    const searchForm = reactive({
      name: '',
      category: undefined
    });

    const selectedRowKeys = ref([]);
    const modalVisible = ref(false);
    const modalTitle = ref('新建命令模板');
    const formData = reactive({
      name: '',
      category: undefined,
      command: '',
      description: ''
    });

    const getCategoryColor = (category) => {
      const colors = {
        'system': 'blue',
        'service': 'green',
        'network': 'purple',
        'monitor': 'orange',
        'security': 'red'
      };
      return colors[category] || 'default';
    };

    const getCategoryText = (category) => {
      const texts = {
        'system': '系统管理',
        'service': '服务管理',
        'network': '网络管理',
        'monitor': '监控管理',
        'security': '安全管理'
      };
      return texts[category] || category;
    };

    const showAddModal = () => {
      modalTitle.value = '新建命令模板';
      formData.name = '';
      formData.category = undefined;
      formData.command = '';
      formData.description = '';
      modalVisible.value = true;
    };

    const showEditModal = (record) => {
      modalTitle.value = '编辑命令模板';
      Object.assign(formData, record);
      modalVisible.value = true;
    };

    const handleModalOk = () => {
      if (!formData.name || !formData.category || !formData.command) {
        message.error('请填写必填项！');
        return;
      }
      // 这里应该调用API保存数据
      message.success('保存成功！');
      modalVisible.value = false;
    };

    const handleSearch = () => {
      // 这里应该调用API进行搜索
      console.log('搜索条件：', searchForm);
    };

    const resetSearch = () => {
      searchForm.name = '';
      searchForm.category = undefined;
    };

    const onSelectChange = (keys) => {
      selectedRowKeys.value = keys;
    };

    const handleDelete = (record) => {
      // 这里应该调用API删除数据
      message.success('删除成功！');
    };

    const handleBatchDelete = () => {
      if (selectedRowKeys.value.length === 0) {
        message.warning('请选择要删除的项！');
        return;
      }
      // 这里应该调用API批量删除数据
      message.success('批量删除成功！');
      selectedRowKeys.value = [];
    };

    const handleCopy = (record) => {
      // 复制模板
      const newTemplate = { ...record };
      newTemplate.name = `${newTemplate.name} - 副本`;
      message.success('复制成功！');
    };

    return {
      columns,
      tableData,
      searchForm,
      selectedRowKeys,
      modalVisible,
      modalTitle,
      formData,
      getCategoryColor,
      getCategoryText,
      showAddModal,
      showEditModal,
      handleModalOk,
      handleSearch,
      resetSearch,
      onSelectChange,
      handleDelete,
      handleBatchDelete,
      handleCopy
    };
  }
});
</script>

<style scoped>
.template-manage {
  padding: 20px;
}
</style> 