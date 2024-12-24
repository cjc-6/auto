<template>
  <div class="alert-history">
    <h3>告警历史记录</h3>

    <!-- 筛选条件 -->
    <a-card style="margin-bottom: 20px">
      <a-form layout="inline">
        <a-form-item label="告警对象">
          <a-input placeholder="请输入告警对象" v-model="searchForm.target" />
        </a-form-item>
        <a-form-item label="告警级别">
          <a-select style="width: 120px" placeholder="请选择级别" v-model="searchForm.level">
            <a-select-option value="high">高</a-select-option>
            <a-select-option value="medium">中</a-select-option>
            <a-select-option value="low">低</a-select-option>
          </a-select>
        </a-form-item>
        <a-form-item label="告警状态">
          <a-select style="width: 120px" placeholder="请选择状态" v-model="searchForm.status">
            <a-select-option value="unconfirmed">未确认</a-select-option>
            <a-select-option value="confirmed">已确认</a-select-option>
            <a-select-option value="resolved">已解决</a-select-option>
          </a-select>
        </a-form-item>
        <a-form-item label="时间范围">
          <a-range-picker v-model="searchForm.timeRange" />
        </a-form-item>
        <a-form-item>
          <a-button type="primary" @click="handleSearch">查询</a-button>
        </a-form-item>
      </a-form>
    </a-card>

    <!-- 告警统计 -->
    <div class="alert-stats" style="margin-bottom: 20px">
      <a-row :gutter="16">
        <a-col :span="6">
          <a-card>
            <statistic
              title="今日告警总数"
              :value="statistics.total_today"
              style="text-align: center"
            >
              <template #suffix>
                <span style="font-size: 14px">条</span>
              </template>
            </statistic>
          </a-card>
        </a-col>
        <a-col :span="6">
          <a-card>
            <statistic
              title="未确认告警"
              :value="statistics.unconfirmed"
              :value-style="{ color: '#cf1322' }"
              style="text-align: center"
            >
              <template #suffix>
                <span style="font-size: 14px">条</span>
              </template>
            </statistic>
          </a-card>
        </a-col>
        <a-col :span="6">
          <a-card>
            <statistic
              title="已确认告警"
              :value="statistics.confirmed"
              :value-style="{ color: '#faad14' }"
              style="text-align: center"
            >
              <template #suffix>
                <span style="font-size: 14px">条</span>
              </template>
            </statistic>
          </a-card>
        </a-col>
        <a-col :span="6">
          <a-card>
            <statistic
              title="已解决告警"
              :value="statistics.resolved"
              :value-style="{ color: '#52c41a' }"
              style="text-align: center"
            >
              <template #suffix>
                <span style="font-size: 14px">条</span>
              </template>
            </statistic>
          </a-card>
        </a-col>
      </a-row>
    </div>

    <!-- 告警列表 -->
    <a-card title="告警列表">
      <template #extra>
        <a-space>
          <a-button>导出记录</a-button>
          <a-button type="primary" @click="handleConfirmAll">批量确认</a-button>
        </a-space>
      </template>
      <a-table :columns="columns" :data-source="tableData">
        <template #bodyCell="{ column, record }">
          <template v-if="column.key === 'level'">
            <a-tag :color="getLevelColor(record.level)">
              {{ record.level }}
            </a-tag>
          </template>
          <template v-if="column.key === 'status'">
            <a-tag :color="getStatusColor(record.status)">
              {{ record.status }}
            </a-tag>
          </template>
          <template v-if="column.key === 'action'">
            <a-space>
              <a>详情</a>
              <a v-if="record.status === '未确认'">确认</a>
              <a v-if="record.status === '已确认'">标记解决</a>
            </a-space>
          </template>
        </template>
      </a-table>
    </a-card>
  </div>
</template>

<script>
import { defineComponent, ref, onMounted } from 'vue';
import { Statistic } from 'ant-design-vue';
import axios from 'axios';
import settings from '@/settings';
import { message } from 'ant-design-vue';

export default defineComponent({
  components: {
    Statistic
  },
  setup() {
    const searchForm = ref({
      target: '',
      level: '',
      status: '',
      timeRange: []
    });

    const statistics = ref({
      total_today: 0,
      unconfirmed: 0,
      confirmed: 0,
      resolved: 0
    });

    const columns = [
      { title: '告警时间', dataIndex: 'time', key: 'time' },
      { title: '告警对象', dataIndex: 'target', key: 'target' },
      { title: '告警内容', dataIndex: 'content', key: 'content' },
      { title: '告警级别', dataIndex: 'level', key: 'level' },
      { title: '状态', dataIndex: 'status', key: 'status' },
      { title: '确认人', dataIndex: 'confirmer', key: 'confirmer' },
      { title: '确认时间', dataIndex: 'confirmTime', key: 'confirmTime' },
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

    const getStatusColor = (status) => {
      const colors = {
        '未确认': '#f5222d',
        '已确认': '#faad14',
        '已解决': '#52c41a',
      };
      return colors[status] || 'default';
    };

    // 获取告警统计数据
    const fetchStatistics = async () => {
      try {
        const response = await axios.get(`${settings.host}/monitor/alerts/statistics/`);
        statistics.value = response.data;
      } catch (error) {
        console.error('获取告警统计数据失败:', error);
        message.error('获取告警统计数据失败');
      }
    };

    // 获取告警历史列表
    const fetchAlertHistory = async () => {
      try {
        const params = {
          target: searchForm.value.target,
          level: searchForm.value.level,
          status: searchForm.value.status,
          start_time: searchForm.value.timeRange[0]?.format('YYYY-MM-DD HH:mm:ss'),
          end_time: searchForm.value.timeRange[1]?.format('YYYY-MM-DD HH:mm:ss')
        };
        const response = await axios.get(`${settings.host}/monitor/alerts/`, { params });
        tableData.value = response.data;
      } catch (error) {
        console.error('获取告警历史失败:', error);
        message.error('获取告警历史失败');
      }
    };

    // 确认告警
    const handleConfirm = async (record) => {
      try {
        await axios.post(`${settings.host}/monitor/alerts/${record.id}/confirm/`);
        message.success('确认成功');
        fetchAlertHistory();
        fetchStatistics();
      } catch (error) {
        console.error('确认告警失败:', error);
        message.error('确认告警失败');
      }
    };

    // 解决告警
    const handleResolve = async (record) => {
      try {
        await axios.post(`${settings.host}/monitor/alerts/${record.id}/resolve/`);
        message.success('标记解决成功');
        fetchAlertHistory();
        fetchStatistics();
      } catch (error) {
        console.error('标记解决失败:', error);
        message.error('标记解决失败');
      }
    };

    // 搜索告警
    const handleSearch = () => {
      fetchAlertHistory();
    };

    // 重置搜索条件
    const handleReset = () => {
      searchForm.value = {
        target: '',
        level: '',
        status: '',
        timeRange: []
      };
      fetchAlertHistory();
    };

    onMounted(() => {
      fetchStatistics();
      fetchAlertHistory();
    });

    return {
      searchForm,
      statistics,
      columns,
      tableData,
      getLevelColor,
      getStatusColor,
      handleConfirm,
      handleResolve,
      handleSearch,
      handleReset
    };
  },
});
</script>

<style scoped>
.alert-history {
  padding: 20px;
}
</style> 