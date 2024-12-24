<template>
  <h3>展示中心</h3>
  <a-row>
    <a-col :span="8">
      <p>
        <a-input-search
            v-model:value="city"
            placeholder="请输入城市名称"
            enter-button="Search"
            size="large"
            @search="get_weather"
        />
      </p>

    </a-col>
  </a-row>

  <a-row>
    <a-col :span="16">
      <a-table :columns="columns" :data-source="data">
        <template #bodyCell="{ column, text }">
          <template v-if="column.dataIndex === 'name'">
            <a>{{ text }}</a>
          </template>
        </template>
      </a-table>
    </a-col>
  </a-row>


  <a-row>
    <a-col :span="12">
      <div class="chart" ref="chart01"></div>
    </a-col>

    <a-col :span="12">
      <div class="chart" ref="chart02"></div>

    </a-col>
  </a-row>


</template>

<script>
import axios from "axios"
import * as echarts from 'echarts';
import {ref} from 'vue';


export default {
  name: "ShowCenter",
  data() {
    return {
      city: "北京", // 默认城市
      columns: [
        {
          title: '日期',
          dataIndex: 'date',
          key: 'date',
        },
        {
          title: '天气',
          dataIndex: 'type',
          key: 'type',
          width: 80,
        },
        {
          title: '最高温度',
          dataIndex: 'high',
          key: 'high',
          ellipsis: true,
        },
        {
          title: '最低温度',
          dataIndex: 'low',
          key: 'low',
          ellipsis: true,
        },
        {
          title: '当前温度',
          dataIndex: 'temperature',
          key: 'temperature',
          ellipsis: true,
        }
      ],
      data: [], // 表格数据源
    };
  },
  methods: {
    get_weather() {
      // 如果用户没有输入城市名称，默认使用 "北京"
      const searchCity = this.city || "北京";

      axios.get("https://api.seniverse.com/v3/weather/now.json", {
        params: {
          key: 'SQNqZ6lEbyAGfEcTP', // 请确保这是您的API密钥
          location: searchCity,      // 使用默认城市或用户输入的城市
          language: 'zh-Hans',
          unit: 'c'
        }
      }).then((response) => {
        const weatherData = response.data.results[0];
        const now = weatherData.now;
        const location = weatherData.location;

        // 构造表格数据
        this.data = [
          {
            date: new Date(weatherData.last_update).toLocaleString(),
            type: now.text,
            high: now.temperature,
            low: now.temperature, // 如果有高低温信息，可以替换为实际值
            temperature: `${now.temperature}°C`
          }
        ];

        // 更新 city 数据属性，确保显示的是实际查询的城市
        this.city = searchCity;

        // 可选：显示提示信息
        console.log(`成功获取 ${searchCity} 的天气信息`);
      }).catch(error => {
        console.error("Error fetching weather data:", error);
        // 不弹出提示框，静默处理错误
      });
    },


    chart01() {
      console.log(":::", this.$refs.chart01);
      var myChart = echarts.init(this.$refs.chart01);
      
      // 生成过去24小时的时间点
      const hours = Array.from({length: 24}, (_, i) => {
        const hour = 23 - i;
        return `${hour}:00`;
      }).reverse();

      // 生成模拟的CPU使用率数据
      const cpuData = Array.from({length: 24}, () => {
        return Math.floor(Math.random() * 40 + 30); // 生成30-70之间的随机数
      });

      const option = {
        title: {
          text: 'CPU使用率监控（24小时）',
          left: 'center'
        },
        tooltip: {
          trigger: 'axis',
          formatter: '{b}<br />CPU使用率: {c}%'
        },
        xAxis: {
          type: 'category',
          data: hours,
          axisLabel: {
            rotate: 45
          }
        },
        yAxis: {
          type: 'value',
          min: 0,
          max: 100,
          axisLabel: {
            formatter: '{value}%'
          }
        },
        series: [
          {
            name: 'CPU使用率',
            type: 'line',
            data: cpuData,
            smooth: true,
            lineStyle: {
              color: '#5470C6',
              width: 2
            },
            areaStyle: {
              color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
                {
                  offset: 0,
                  color: 'rgba(84,112,198,0.5)'
                },
                {
                  offset: 1,
                  color: 'rgba(84,112,198,0.1)'
                }
              ])
            },
            markLine: {
              data: [
                {
                  name: '警戒线',
                  yAxis: 80,
                  lineStyle: {
                    color: '#FF4444'
                  },
                  label: {
                    formatter: '警戒线 (80%)',
                    position: 'end'
                  }
                }
              ]
            }
          }
        ],
        grid: {
          left: '3%',
          right: '4%',
          bottom: '15%',
          containLabel: true
        }
      };

      option && myChart.setOption(option);
    },

    chart02() {
      var myChart = echarts.init(this.$refs.chart02);
      
      // 模拟5台服务器的内存使用情况
      const serverData = [
        { name: 'Server-01', total: 32, used: 24.5 },
        { name: 'Server-02', total: 16, used: 12.8 },
        { name: 'Server-03', total: 64, used: 45.2 },
        { name: 'Server-04', total: 8, used: 6.7 },
        { name: 'Server-05', total: 32, used: 28.9 }
      ];

      const option = {
        title: {
          text: '服务器内存使用情况',
          left: 'center'
        },
        tooltip: {
          trigger: 'axis',
          axisPointer: {
            type: 'shadow'
          },
          formatter: function(params) {
            const data = serverData[params[0].dataIndex];
            const usedPercent = ((data.used / data.total) * 100).toFixed(1);
            return `${data.name}<br/>` +
                   `总内存: ${data.total}GB<br/>` +
                   `已使用: ${data.used}GB<br/>` +
                   `使用率: ${usedPercent}%`;
          }
        },
        grid: {
          left: '3%',
          right: '4%',
          bottom: '3%',
          containLabel: true
        },
        xAxis: {
          type: 'category',
          data: serverData.map(item => item.name)
        },
        yAxis: {
          type: 'value',
          name: '内存 (GB)',
          max: 70
        },
        series: [
          {
            name: '总内存',
            type: 'bar',
            stack: 'memory',
            itemStyle: {
              color: 'rgba(128, 128, 128, 0.2)'
            },
            data: serverData.map(item => item.total)
          },
          {
            name: '已使用',
            type: 'bar',
            stack: 'memory',
            itemStyle: {
              color: '#91CC75'
            },
            data: serverData.map(item => item.used),
            markLine: {
              data: [
                {
                  name: '警戒线',
                  yAxis: 50,
                  lineStyle: {
                    color: '#FF4444'
                  },
                  label: {
                    formatter: '警戒线 (50GB)',
                    position: 'end'
                  }
                }
              ]
            }
          }
        ]
      };

      option && myChart.setOption(option);
    },
  },


  mounted() {


    this.get_weather();
    this.chart01();
    this.chart02();

  }
}
</script>

<style scoped>
.chart {
  height: 500px;
}
</style>