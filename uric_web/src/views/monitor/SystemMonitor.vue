<template>
  <div class="system-monitor">
    <h3>系统监控</h3>
    
    <!-- 概览卡片 -->
    <a-row :gutter="16" style="margin-bottom: 20px">
      <a-col :span="6">
        <a-card>
          <template #title>
            <span style="color: #1890ff">
              <thunderbolt-outlined /> 在线服务器
            </span>
          </template>
          <h2 style="text-align: center; color: #1890ff">42/45</h2>
          <p style="text-align: center; color: #666">正常运行率：93.3%</p>
        </a-card>
      </a-col>
      <a-col :span="6">
        <a-card>
          <template #title>
            <span style="color: #52c41a">
              <safety-outlined /> 系统正常
            </span>
          </template>
          <h2 style="text-align: center; color: #52c41a">38</h2>
          <p style="text-align: center; color: #666">正常系统数</p>
        </a-card>
      </a-col>
      <a-col :span="6">
        <a-card>
          <template #title>
            <span style="color: #faad14">
              <warning-outlined /> 系统警告
            </span>
          </template>
          <h2 style="text-align: center; color: #faad14">4</h2>
          <p style="text-align: center; color: #666">警告系统数</p>
        </a-card>
      </a-col>
      <a-col :span="6">
        <a-card>
          <template #title>
            <span style="color: #ff4d4f">
              <stop-outlined /> 系统故障
            </span>
          </template>
          <h2 style="text-align: center; color: #ff4d4f">3</h2>
          <p style="text-align: center; color: #666">故障系统数</p>
        </a-card>
      </a-col>
    </a-row>

    <!-- 系统状态表格 -->
    <a-card title="系统状态" style="margin-bottom: 20px">
      <a-table :columns="columns" :data-source="tableData" :pagination="{ pageSize: 5 }">
        <template #bodyCell="{ column, record }">
          <template v-if="column.key === 'status'">
            <a-tag :color="getStatusColor(record.status)">
              {{ record.status }}
            </a-tag>
          </template>
          <template v-if="column.key === 'cpu'">
            <a-progress :percent="record.cpu" size="small" :status="getCPUStatus(record.cpu)" />
          </template>
          <template v-if="column.key === 'memory'">
            <a-progress :percent="record.memory" size="small" :status="getMemoryStatus(record.memory)" />
          </template>
          <template v-if="column.key === 'disk'">
            <a-progress :percent="record.disk" size="small" :status="getDiskStatus(record.disk)" />
          </template>
        </template>
      </a-table>
    </a-card>

    <!-- 性能趋势图 -->
    <a-card title="性能趋势">
      <div ref="performanceChart" style="height: 400px"></div>
    </a-card>
  </div>
</template>

<script>
import { defineComponent, onMounted, ref } from 'vue';
import * as echarts from 'echarts';
import { ThunderboltOutlined, SafetyOutlined, WarningOutlined, StopOutlined } from '@ant-design/icons-vue';
import axios from 'axios';
import settings from '@/settings';

export default defineComponent({
  components: {
    ThunderboltOutlined,
    SafetyOutlined,
    WarningOutlined,
    StopOutlined,
  },
  setup() {
    const performanceChart = ref(null);
    const columns = [
      { title: '服务器', dataIndex: 'server', key: 'server' },
      { title: '状态', dataIndex: 'status', key: 'status' },
      { title: 'CPU使用率', dataIndex: 'cpu', key: 'cpu' },
      { title: '内存使用率', dataIndex: 'memory', key: 'memory' },
      { title: '磁盘使用率', dataIndex: 'disk', key: 'disk' },
      { title: '更新时间', dataIndex: 'updateTime', key: 'updateTime' },
    ];

    const tableData = ref([]);
    const overview = ref({
      total: 0,
      normal: 0,
      warning: 0,
      critical: 0,
      uptime_rate: 0
    });

    // 获取系统概览数据
    const fetchOverview = async () => {
      try {
        const response = await axios.get(`${settings.host}/monitor/system/overview/`);
        overview.value = response.data;
      } catch (error) {
        console.error('获取系统概览数据失败:', error);
      }
    };

    // 获取系统状态数据
    const fetchSystemStatus = async () => {
      try {
        const response = await axios.get(`${settings.host}/monitor/system/`);
        tableData.value = response.data;
      } catch (error) {
        console.error('获取系统状态数据失败:', error);
      }
    };

    // 获取性能趋势数据
    const fetchPerformanceTrends = async () => {
      try {
        const response = await axios.get(`${settings.host}/monitor/system/trends/`);
        const data = response.data;
        
        const chart = echarts.init(performanceChart.value);
        const option = {
          title: {
            text: '24小时性能趋势',
            left: 'center'
          },
          tooltip: {
            trigger: 'axis'
          },
          legend: {
            data: ['CPU使用率', '内存使用率', '磁盘使用率'],
            top: 30
          },
          xAxis: {
            type: 'category',
            data: data.timestamps
          },
          yAxis: {
            type: 'value',
            max: 100,
            axisLabel: {
              formatter: '{value}%'
            }
          },
          series: [
            {
              name: 'CPU使用率',
              type: 'line',
              smooth: true,
              data: data.cpu
            },
            {
              name: '内存使用率',
              type: 'line',
              smooth: true,
              data: data.memory
            },
            {
              name: '磁盘使用率',
              type: 'line',
              smooth: true,
              data: data.disk
            }
          ]
        };
        chart.setOption(option);
      } catch (error) {
        console.error('获取性能趋势数据失败:', error);
      }
    };

    const getStatusColor = (status) => {
      const colors = {
        '正常': 'success',
        '警告': 'warning',
        '故障': 'error',
      };
      return colors[status] || 'default';
    };

    const getCPUStatus = (value) => value > 80 ? 'exception' : value > 60 ? 'warning' : 'normal';
    const getMemoryStatus = (value) => value > 80 ? 'exception' : value > 60 ? 'warning' : 'normal';
    const getDiskStatus = (value) => value > 80 ? 'exception' : value > 60 ? 'warning' : 'normal';

    onMounted(() => {
      fetchOverview();
      fetchSystemStatus();
      fetchPerformanceTrends();
    });

    return {
      columns,
      tableData,
      overview,
      performanceChart,
      getStatusColor,
      getCPUStatus,
      getMemoryStatus,
      getDiskStatus,
    };
  }
});
</script>

<style scoped>
.system-monitor {
  padding: 20px;
}
</style> 