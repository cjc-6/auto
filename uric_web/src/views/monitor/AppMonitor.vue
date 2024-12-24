<template>
  <div class="app-monitor">
    <h3>应用监控</h3>

    <!-- 应用选择和时间范围 -->
    <a-card style="margin-bottom: 20px">
      <a-form layout="inline">
        <a-form-item label="应用服务">
          <a-select style="width: 200px" placeholder="请选择应用" v-model:value="currentApp">
            <a-select-option value="order">订单服务</a-select-option>
            <a-select-option value="user">用户服务</a-select-option>
            <a-select-option value="payment">支付服务</a-select-option>
            <a-select-option value="inventory">库存服务</a-select-option>
          </a-select>
        </a-form-item>
        <a-form-item label="时间范围">
          <a-select style="width: 120px" v-model:value="timeRange">
            <a-select-option value="30min">最近30分钟</a-select-option>
            <a-select-option value="1h">最近1小时</a-select-option>
            <a-select-option value="6h">最近6小时</a-select-option>
            <a-select-option value="24h">最近24小时</a-select-option>
          </a-select>
        </a-form-item>
        <a-form-item>
          <a-button type="primary">刷新</a-button>
        </a-form-item>
      </a-form>
    </a-card>

    <!-- 应用状态概览 -->
    <div class="app-stats" style="margin-bottom: 20px">
      <a-row :gutter="16">
        <a-col :span="6">
          <a-card>
            <statistic
              title="QPS"
              :value="1234"
              :precision="2"
              style="text-align: center"
            >
              <template #suffix>
                <span style="font-size: 14px">次/秒</span>
              </template>
            </statistic>
          </a-card>
        </a-col>
        <a-col :span="6">
          <a-card>
            <statistic
              title="平均响应时间"
              :value="156"
              style="text-align: center"
            >
              <template #suffix>
                <span style="font-size: 14px">ms</span>
              </template>
            </statistic>
          </a-card>
        </a-col>
        <a-col :span="6">
          <a-card>
            <statistic
              title="错误率"
              :value="0.15"
              :precision="2"
              :value-style="{ color: '#cf1322' }"
              style="text-align: center"
            >
              <template #suffix>
                <span style="font-size: 14px">%</span>
              </template>
            </statistic>
          </a-card>
        </a-col>
        <a-col :span="6">
          <a-card>
            <statistic
              title="在线实例数"
              :value="3"
              style="text-align: center"
            >
              <template #suffix>
                <span style="font-size: 14px">个</span>
              </template>
            </statistic>
          </a-card>
        </a-col>
      </a-row>
    </div>

    <!-- 性能监控图表 -->
    <a-row :gutter="16" style="margin-bottom: 20px">
      <a-col :span="12">
        <a-card title="QPS趋势">
          <div ref="qpsChart" style="height: 300px"></div>
        </a-card>
      </a-col>
      <a-col :span="12">
        <a-card title="响应时间趋势">
          <div ref="rtChart" style="height: 300px"></div>
        </a-card>
      </a-col>
    </a-row>

    <a-row :gutter="16" style="margin-bottom: 20px">
      <a-col :span="12">
        <a-card title="错误率趋势">
          <div ref="errorChart" style="height: 300px"></div>
        </a-card>
      </a-col>
      <a-col :span="12">
        <a-card title="内存使用趋势">
          <div ref="memoryChart" style="height: 300px"></div>
        </a-card>
      </a-col>
    </a-row>

    <!-- 接口调用TOP10 -->
    <a-card title="接口调用TOP10" style="margin-bottom: 20px">
      <a-table :columns="columns" :data-source="tableData" :pagination="false">
        <template #bodyCell="{ column, record }">
          <template v-if="column.key === 'status'">
            <a-tag :color="getStatusColor(record.status)">
              {{ record.status }}
            </a-tag>
          </template>
        </template>
      </a-table>
    </a-card>
  </div>
</template>

<script>
import { defineComponent, ref, onMounted } from 'vue';
import { Statistic } from 'ant-design-vue';
import * as echarts from 'echarts';
import axios from 'axios';
import settings from '@/settings';

export default defineComponent({
  components: {
    Statistic
  },
  setup() {
    const currentApp = ref('order');
    const timeRange = ref('1h');
    const qpsChart = ref(null);
    const rtChart = ref(null);
    const errorChart = ref(null);
    const memoryChart = ref(null);
    const performanceData = ref({
      qps: 0,
      avg_response_time: 0,
      error_rate: 0,
      concurrent_connections: 0
    });

    const columns = [
      { title: '接口路径', dataIndex: 'path', key: 'path' },
      { title: '调用次数', dataIndex: 'count', key: 'count' },
      { title: '平均响应时间', dataIndex: 'avgRt', key: 'avgRt' },
      { title: '最大响应时间', dataIndex: 'maxRt', key: 'maxRt' },
      { title: '错误次数', dataIndex: 'errorCount', key: 'errorCount' },
      { title: '状态', dataIndex: 'status', key: 'status' },
    ];

    const tableData = ref([]);

    const getStatusColor = (status) => {
      return status === '正常' ? '#52c41a' : '#f5222d';
    };

    // 获取应用性能数据
    const fetchPerformanceData = async () => {
      try {
        const response = await axios.get(`${settings.host}/monitor/application/performance/`, {
          params: {
            app_name: currentApp.value,
            time_range: timeRange.value
          }
        });
        performanceData.value = response.data;
      } catch (error) {
        console.error('获取应用性能数据失败:', error);
      }
    };

    // 获取API调用统计
    const fetchApiStats = async () => {
      try {
        const response = await axios.get(`${settings.host}/monitor/application/apis/`, {
          params: {
            app_name: currentApp.value,
            time_range: timeRange.value
          }
        });
        tableData.value = response.data;
      } catch (error) {
        console.error('获取API调用统计失败:', error);
      }
    };

    const handleRefresh = async () => {
      await fetchPerformanceData();
      await fetchApiStats();
    };

    const initCharts = () => {
      // 初始化QPS趋势图
      const qps = echarts.init(qpsChart.value);
      qps.setOption({
        tooltip: {
          trigger: 'axis'
        },
        xAxis: {
          type: 'category',
          data: ['10:00', '10:05', '10:10', '10:15', '10:20', '10:25', '10:30']
        },
        yAxis: {
          type: 'value'
        },
        series: [{
          data: [820, 932, 901, 934, 1290, 1330, 1320],
          type: 'line',
          smooth: true
        }]
      });

      // 初始化响应时间趋势图
      const rt = echarts.init(rtChart.value);
      rt.setOption({
        tooltip: {
          trigger: 'axis'
        },
        xAxis: {
          type: 'category',
          data: ['10:00', '10:05', '10:10', '10:15', '10:20', '10:25', '10:30']
        },
        yAxis: {
          type: 'value'
        },
        series: [{
          data: [120, 132, 101, 134, 90, 230, 210],
          type: 'line',
          smooth: true
        }]
      });

      // 初始化错误率趋势图
      const error = echarts.init(errorChart.value);
      error.setOption({
        tooltip: {
          trigger: 'axis'
        },
        xAxis: {
          type: 'category',
          data: ['10:00', '10:05', '10:10', '10:15', '10:20', '10:25', '10:30']
        },
        yAxis: {
          type: 'value',
          axisLabel: {
            formatter: '{value}%'
          }
        },
        series: [{
          data: [0.1, 0.2, 0.15, 0.3, 0.2, 0.1, 0.15],
          type: 'line',
          smooth: true,
          lineStyle: {
            color: '#ff4d4f'
          },
          itemStyle: {
            color: '#ff4d4f'
          }
        }]
      });

      // 初始化内存使用趋势图
      const memory = echarts.init(memoryChart.value);
      memory.setOption({
        tooltip: {
          trigger: 'axis'
        },
        xAxis: {
          type: 'category',
          data: ['10:00', '10:05', '10:10', '10:15', '10:20', '10:25', '10:30']
        },
        yAxis: {
          type: 'value',
          axisLabel: {
            formatter: '{value}MB'
          }
        },
        series: [{
          data: [1024, 1124, 1234, 1345, 1256, 1356, 1567],
          type: 'line',
          smooth: true,
          lineStyle: {
            color: '#1890ff'
          },
          itemStyle: {
            color: '#1890ff'
          }
        }]
      });
    };

    onMounted(() => {
      initCharts();
      fetchPerformanceData();
      fetchApiStats();
    });

    return {
      currentApp,
      timeRange,
      qpsChart,
      rtChart,
      errorChart,
      memoryChart,
      columns,
      tableData,
      performanceData,
      getStatusColor,
      handleRefresh
    };
  },
});
</script>

<style scoped>
.app-monitor {
  padding: 20px;
}
</style> 