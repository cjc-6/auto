<template>
  <div class="alert-rules">
    <h3>告警规则配置</h3>

    <!-- 操作按钮 -->
    <div class="operation-bar" style="margin-bottom: 20px">
      <a-space>
        <a-button type="primary">
          <template #icon><plus-outlined /></template>
          新建规则
        </a-button>
        <a-button>
          <template #icon><import-outlined /></template>
          导入规则
        </a-button>
        <a-button>
          <template #icon><export-outlined /></template>
          导出规则
        </a-button>
      </a-space>
    </div>

    <!-- 规则筛选 -->
    <a-card style="margin-bottom: 20px">
      <a-form layout="inline">
        <a-form-item label="规则名称">
          <a-input placeholder="请输入规则名称" v-model="searchForm.name" />
        </a-form-item>
        <a-form-item label="告警级别">
          <a-select style="width: 120px" placeholder="请选择级别" v-model="searchForm.level">
            <a-select-option value="high">高</a-select-option>
            <a-select-option value="medium">中</a-select-option>
            <a-select-option value="low">低</a-select-option>
          </a-select>
        </a-form-item>
        <a-form-item label="规则状态">
          <a-select style="width: 120px" placeholder="请选择状态" v-model="searchForm.status">
            <a-select-option value="enabled">启用</a-select-option>
            <a-select-option value="disabled">禁用</a-select-option>
          </a-select>
        </a-form-item>
        <a-form-item>
          <a-button type="primary" @click="handleSearch">查询</a-button>
        </a-form-item>
      </a-form>
    </a-card>

    <!-- 规则列表 -->
    <a-card title="告警规则列表">
      <a-table :columns="columns" :data-source="tableData">
        <template #bodyCell="{ column, record }">
          <template v-if="column.key === 'level'">
            <a-tag :color="getLevelColor(record.level)">
              {{ record.level }}
            </a-tag>
          </template>
          <template v-if="column.key === 'status'">
            <a-switch
              :checked="record.status === '启用'"
              :checkedChildren="'启用'"
              :unCheckedChildren="'禁用'"
              @change="handleStatusChange(record, $event)"
            />
          </template>
          <template v-if="column.key === 'action'">
            <a-space>
              <a>编辑</a>
              <a>克隆</a>
              <a-popconfirm
                title="确定要删除这条规则吗？"
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
  </div>
</template>

<script>
import { defineComponent, ref } from 'vue';
import {
  PlusOutlined,
  ImportOutlined,
  ExportOutlined
} from '@ant-design/icons-vue';
import axios from 'axios';
import settings from '@/settings';
import { message } from 'ant-design-vue';

export default defineComponent({
  components: {
    PlusOutlined,
    ImportOutlined,
    ExportOutlined
  },
  setup() {
    const searchForm = ref({
      name: '',
      level: '',
      status: ''
    });

    const columns = [
      { title: '规则名称', dataIndex: 'name', key: 'name' },
      { title: '监控对象', dataIndex: 'target', key: 'target' },
      { title: '告警级别', dataIndex: 'level', key: 'level' },
      { title: '触发条件', dataIndex: 'condition', key: 'condition' },
      { title: '通知方式', dataIndex: 'notification', key: 'notification' },
      { title: '状态', dataIndex: 'status', key: 'status' },
      { title: '最后修改时间', dataIndex: 'updateTime', key: 'updateTime' },
      { title: '操作', key: 'action' },
    ];

    const tableData = ref([]);

    const getLevelColor = (level) => {
      const colors = {
        '高': '#f5222d',
        '中': '#faad14',
        '低': '#52c41a',
      };
      return colors[level] || 'default';
    };

    // 获取告警规则列表
    const fetchRules = async () => {
      try {
        const response = await axios.get(`${settings.host}/monitor/rules/`, {
          params: searchForm.value
        });
        tableData.value = response.data;
      } catch (error) {
        console.error('获取告警规则失败:', error);
        message.error('获取告警规则失败');
      }
    };

    // 切换规则状态
    const handleStatusChange = async (record, checked) => {
      try {
        await axios.post(`${settings.host}/monitor/rules/${record.id}/toggle_status/`);
        message.success(`${checked ? '启用' : '禁用'}成功`);
        fetchRules();
      } catch (error) {
        console.error('切换规则状态失败:', error);
        message.error('切换规则状态失败');
      }
    };

    // 删除规则
    const handleDelete = async (record) => {
      try {
        await axios.delete(`${settings.host}/monitor/rules/${record.id}/`);
        message.success('删除成功');
        fetchRules();
      } catch (error) {
        console.error('删除规则失败:', error);
        message.error('删除规则失败');
      }
    };

    // 搜索规则
    const handleSearch = () => {
      fetchRules();
    };

    // 重置搜索条件
    const handleReset = () => {
      searchForm.value = {
        name: '',
        level: '',
        status: ''
      };
      fetchRules();
    };

    // 初始化加载数据
    fetchRules();

    return {
      columns,
      tableData,
      searchForm,
      getLevelColor,
      handleStatusChange,
      handleDelete,
      handleSearch,
      handleReset
    };
  },
});
</script>

<style scoped>
.alert-rules {
  padding: 20px;
}
</style> 