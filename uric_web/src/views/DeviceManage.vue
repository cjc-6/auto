<template>
  <div class="device-manage">
    <h3>设备管理</h3>

    <!-- 设备状态概览 -->
    <a-row :gutter="16" style="margin-bottom: 20px">
      <a-col :span="6">
        <a-card>
          <statistic
            title="设备总数"
            :value="48"
            style="text-align: center"
          >
            <template #suffix>
              <span style="font-size: 14px">台</span>
            </template>
          </statistic>
        </a-card>
      </a-col>
      <a-col :span="6">
        <a-card>
          <statistic
            title="运行中"
            :value="42"
            :value-style="{ color: '#52c41a' }"
            style="text-align: center"
          >
            <template #suffix>
              <span style="font-size: 14px">台</span>
            </template>
          </statistic>
        </a-card>
      </a-col>
      <a-col :span="6">
        <a-card>
          <statistic
            title="已暂停"
            :value="4"
            :value-style="{ color: '#faad14' }"
            style="text-align: center"
          >
            <template #suffix>
              <span style="font-size: 14px">台</span>
            </template>
          </statistic>
        </a-card>
      </a-col>
      <a-col :span="6">
        <a-card>
          <statistic
            title="故障/维护"
            :value="2"
            :value-style="{ color: '#ff4d4f' }"
            style="text-align: center"
          >
            <template #suffix>
              <span style="font-size: 14px">台</span>
            </template>
          </statistic>
        </a-card>
      </a-col>
    </a-row>

    <!-- 操作按钮 -->
    <div class="operation-bar" style="margin-bottom: 20px">
      <a-space>
        <a-button type="primary" @click="showAddModal">
          <template #icon><plus-outlined /></template>
          添加设备
        </a-button>
        <a-button type="primary" danger @click="handleBatchPause" :disabled="selectedRowKeys.length === 0">
          <template #icon><pause-circle-outlined /></template>
          批量暂停
        </a-button>
        <a-button type="primary" @click="handleBatchStart" :disabled="selectedRowKeys.length === 0">
          <template #icon><play-circle-outlined /></template>
          批量启动
        </a-button>
        <a-button @click="handleBatchMaintenance" :disabled="selectedRowKeys.length === 0">
          <template #icon><tool-outlined /></template>
          批量维护
        </a-button>
      </a-space>
    </div>

    <!-- 筛选条件 -->
    <a-card style="margin-bottom: 20px">
      <a-form layout="inline">
        <a-form-item label="设备名称">
          <a-input v-model:value="searchForm.name" placeholder="请输入设备名称" />
        </a-form-item>
        <a-form-item label="设备类型">
          <a-select v-model:value="searchForm.type" style="width: 160px" placeholder="请选择类型">
            <a-select-option value="server">服务器</a-select-option>
            <a-select-option value="network">网络设备</a-select-option>
            <a-select-option value="storage">存储设备</a-select-option>
            <a-select-option value="security">安全设备</a-select-option>
          </a-select>
        </a-form-item>
        <a-form-item label="运行状态">
          <a-select v-model:value="searchForm.status" style="width: 160px" placeholder="请选择状态">
            <a-select-option value="running">运行中</a-select-option>
            <a-select-option value="paused">已暂停</a-select-option>
            <a-select-option value="maintenance">维护中</a-select-option>
            <a-select-option value="fault">故障</a-select-option>
          </a-select>
        </a-form-item>
        <a-form-item>
          <a-button type="primary" @click="handleSearch">查询</a-button>
          <a-button style="margin-left: 8px" @click="resetSearch">重置</a-button>
        </a-form-item>
      </a-form>
    </a-card>

    <!-- 设备列表 -->
    <a-card>
      <a-table 
        :columns="columns" 
        :data-source="tableData"
        :row-selection="{ selectedRowKeys: selectedRowKeys, onChange: onSelectChange }"
        :pagination="{ pageSize: 10 }"
      >
        <template #bodyCell="{ column, record }">
          <template v-if="column.key === 'type'">
            <a-tag :color="getTypeColor(record.type)">
              {{ getTypeText(record.type) }}
            </a-tag>
          </template>
          <template v-if="column.key === 'status'">
            <a-badge :status="getStatusType(record.status)" :text="getStatusText(record.status)" />
          </template>
          <template v-if="column.key === 'load'">
            <a-progress :percent="record.load" size="small" :status="getLoadStatus(record.load)" />
          </template>
          <template v-if="column.key === 'action'">
            <a-space>
              <a-tooltip title="查看详情">
                <a @click="showDetailModal(record)"><eye-outlined /></a>
              </a-tooltip>
              <a-tooltip :title="record.status === 'running' ? '暂停' : '启动'">
                <a @click="toggleDeviceStatus(record)">
                  <pause-circle-outlined v-if="record.status === 'running'" style="color: #ff4d4f"/>
                  <play-circle-outlined v-else style="color: #52c41a"/>
                </a>
              </a-tooltip>
              <a-tooltip title="维护">
                <a @click="showMaintenanceModal(record)"><tool-outlined /></a>
              </a-tooltip>
              <a-tooltip title="编辑">
                <a @click="showEditModal(record)"><edit-outlined /></a>
              </a-tooltip>
              <a-tooltip title="删除">
                <a-popconfirm
                  title="确定要删除这台设备吗？"
                  ok-text="确定"
                  cancel-text="取消"
                  @confirm="handleDelete(record)"
                >
                  <delete-outlined style="color: #ff4d4f"/>
                </a-popconfirm>
              </a-tooltip>
            </a-space>
          </template>
        </template>
      </a-table>
    </a-card>

    <!-- 维护计划弹窗 -->
    <a-modal
      v-model:visible="maintenanceVisible"
      title="设备维护计划"
      @ok="handleMaintenanceOk"
      width="600px"
    >
      <a-form :label-col="{ span: 6 }" :wrapper-col="{ span: 18 }">
        <a-form-item label="维护类型" required>
          <a-select v-model:value="maintenanceForm.type">
            <a-select-option value="routine">例行维护</a-select-option>
            <a-select-option value="repair">故障维修</a-select-option>
            <a-select-option value="upgrade">设备升级</a-select-option>
          </a-select>
        </a-form-item>
        <a-form-item label="计划开始时间" required>
          <a-date-picker 
            v-model:value="maintenanceForm.startTime"
            :show-time="true"
            style="width: 100%"
          />
        </a-form-item>
        <a-form-item label="预计持续时间" required>
          <a-input-number 
            v-model:value="maintenanceForm.duration"
            :min="1"
            :max="48"
            addon-after="小时"
            style="width: 100%"
          />
        </a-form-item>
        <a-form-item label="维护内容" required>
          <a-textarea 
            v-model:value="maintenanceForm.content"
            :rows="4"
            placeholder="请输入维护内容"
          />
        </a-form-item>
        <a-form-item label="维护人员" required>
          <a-select v-model:value="maintenanceForm.maintainer" mode="multiple">
            <a-select-option value="user1">张三</a-select-option>
            <a-select-option value="user2">李四</a-select-option>
            <a-select-option value="user3">王五</a-select-option>
          </a-select>
        </a-form-item>
        <a-form-item label="备注">
          <a-textarea 
            v-model:value="maintenanceForm.remarks"
            :rows="3"
            placeholder="请输入备注信息"
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
  PauseCircleOutlined,
  PlayCircleOutlined,
  ToolOutlined,
  EyeOutlined,
  EditOutlined,
  DeleteOutlined
} from '@ant-design/icons-vue';

export default defineComponent({
  components: {
    PlusOutlined,
    PauseCircleOutlined,
    PlayCircleOutlined,
    ToolOutlined,
    EyeOutlined,
    EditOutlined,
    DeleteOutlined
  },
  setup() {
    const columns = [
      { title: '设备名称', dataIndex: 'name', key: 'name' },
      { title: '设备类型', dataIndex: 'type', key: 'type' },
      { title: 'IP地址', dataIndex: 'ip', key: 'ip' },
      { title: '状态', dataIndex: 'status', key: 'status' },
      { title: '负载', dataIndex: 'load', key: 'load' },
      { title: '最后检查时间', dataIndex: 'lastCheck', key: 'lastCheck' },
      { title: '操作', key: 'action', width: 200 },
    ];

    // 预设的设备数据
    const tableData = [
      {
        key: '1',
        name: 'Web服务器-01',
        type: 'server',
        ip: '192.168.1.101',
        status: 'running',
        load: 45,
        lastCheck: '2024-12-23 10:00:00',
      },
      {
        key: '2',
        name: '核心交换机-01',
        type: 'network',
        ip: '192.168.1.1',
        status: 'running',
        load: 32,
        lastCheck: '2024-12-23 09:55:00',
      },
      {
        key: '3',
        name: '存储阵列-01',
        type: 'storage',
        ip: '192.168.1.201',
        status: 'maintenance',
        load: 0,
        lastCheck: '2024-12-23 09:50:00',
      },
      {
        key: '4',
        name: '防火墙-01',
        type: 'security',
        ip: '192.168.1.2',
        status: 'running',
        load: 28,
        lastCheck: '2024-12-23 09:45:00',
      },
      {
        key: '5',
        name: 'DB服务器-01',
        type: 'server',
        ip: '192.168.1.102',
        status: 'paused',
        load: 0,
        lastCheck: '2024-12-23 09:40:00',
      }
    ];

    const searchForm = reactive({
      name: '',
      type: undefined,
      status: undefined
    });

    const selectedRowKeys = ref([]);
    const maintenanceVisible = ref(false);
    const maintenanceForm = reactive({
      type: undefined,
      startTime: null,
      duration: 2,
      content: '',
      maintainer: [],
      remarks: ''
    });

    const getTypeColor = (type) => {
      const colors = {
        'server': 'blue',
        'network': 'green',
        'storage': 'purple',
        'security': 'red'
      };
      return colors[type] || 'default';
    };

    const getTypeText = (type) => {
      const texts = {
        'server': '服务器',
        'network': '网络设备',
        'storage': '存储设备',
        'security': '安全设备'
      };
      return texts[type] || type;
    };

    const getStatusType = (status) => {
      const types = {
        'running': 'success',
        'paused': 'warning',
        'maintenance': 'processing',
        'fault': 'error'
      };
      return types[status] || 'default';
    };

    const getStatusText = (status) => {
      const texts = {
        'running': '运行中',
        'paused': '已暂停',
        'maintenance': '维护中',
        'fault': '故障'
      };
      return texts[status] || status;
    };

    const getLoadStatus = (value) => {
      if (value === 0) return 'normal';
      return value > 80 ? 'exception' : value > 60 ? 'warning' : 'normal';
    };

    const handleSearch = () => {
      // 这里应该调用API进行搜索
      console.log('搜索条件：', searchForm);
    };

    const resetSearch = () => {
      searchForm.name = '';
      searchForm.type = undefined;
      searchForm.status = undefined;
    };

    const onSelectChange = (keys) => {
      selectedRowKeys.value = keys;
    };

    const handleBatchPause = () => {
      message.success(`已暂停 ${selectedRowKeys.value.length} 台设备`);
      selectedRowKeys.value = [];
    };

    const handleBatchStart = () => {
      message.success(`已启动 ${selectedRowKeys.value.length} 台设备`);
      selectedRowKeys.value = [];
    };

    const handleBatchMaintenance = () => {
      maintenanceVisible.value = true;
    };

    const toggleDeviceStatus = (record) => {
      const action = record.status === 'running' ? '暂停' : '启动';
      message.success(`已${action}设备：${record.name}`);
    };

    const showMaintenanceModal = (record) => {
      maintenanceVisible.value = true;
    };

    const handleMaintenanceOk = () => {
      if (!maintenanceForm.type || !maintenanceForm.startTime || !maintenanceForm.content || maintenanceForm.maintainer.length === 0) {
        message.error('请填写必填项！');
        return;
      }
      message.success('维护计划已创建！');
      maintenanceVisible.value = false;
    };

    return {
      columns,
      tableData,
      searchForm,
      selectedRowKeys,
      maintenanceVisible,
      maintenanceForm,
      getTypeColor,
      getTypeText,
      getStatusType,
      getStatusText,
      getLoadStatus,
      handleSearch,
      resetSearch,
      onSelectChange,
      handleBatchPause,
      handleBatchStart,
      handleBatchMaintenance,
      toggleDeviceStatus,
      showMaintenanceModal,
      handleMaintenanceOk
    };
  }
});
</script>

<style scoped>
.device-manage {
  padding: 20px;
}
</style> 