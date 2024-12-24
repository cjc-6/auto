<template>
  <a-layout style="min-height: 100vh">
    <a-layout-sider v-model:collapsed="collapsed" collapsible>
      <div class="logo"
           style="font-style: italic;text-align: center;font-size: 20px;color:#fff;margin: 10px 0;line-height: 50px;font-family: 'Times New Roman'">
        <span><a-switch v-model:checked="checked"/> DevOps</span>
      </div>
      <div class="logo"/>
      <a-menu v-model:selectedKeys="selectedKeys" theme="dark" mode="inline">
        <template v-for="menu in menu_list" :key="menu.id">
          <template v-if="menu.children.length===0">
            <a-menu-item :key="menu.id">
              <router-link :to="menu.menu_url">
                <desktop-outlined/>
                <span> {{ menu.title }}</span>
              </router-link>
            </a-menu-item>
          </template>

          <template v-else>
            <a-sub-menu :key="menu.id">
              <template #title>
                <span>
                  <user-outlined/>
                  <span>{{ menu.title }}</span>
                </span>
              </template>
              <a-menu-item v-for="child_menu in menu.children" :key="child_menu.id">
                <router-link :to="child_menu.menu_url">{{ child_menu.title }}</router-link>
              </a-menu-item>
            </a-sub-menu>
          </template>
        </template>
      </a-menu>
    </a-layout-sider>
    <a-layout>
      <a-layout-header style="background: #fff; padding: 20px">
        <a-row type="flex" justify="start">
          <a-col :span="6">
            <a-breadcrumb>
              <a-breadcrumb-item href="">
                <home-outlined/>
              </a-breadcrumb-item>
              <a-breadcrumb-item href="">
                <user-outlined/>
                <span>Application List</span>
              </a-breadcrumb-item>
              <a-breadcrumb-item>Application</a-breadcrumb-item>
            </a-breadcrumb>
          </a-col>

          <a-col :span="1" :offset="17">
            <a-breadcrumb>
              <a-button @click="logout" type="primary" class="logout">
                注销
              </a-button>
            </a-breadcrumb>
          </a-col>
        </a-row>
      </a-layout-header>

      <a-layout-content style="margin: 0 16px">
        <router-view></router-view>
      </a-layout-content>
      
      <a-layout-footer style="text-align: center">
        Ant Design ©2018 Created by Ant UED
      </a-layout-footer>
    </a-layout>
  </a-layout>
</template>

<script>
import {
  DesktopOutlined,
  FileOutlined,
  PieChartOutlined,
  TeamOutlined,
  UserOutlined,
  HomeOutlined
} from '@ant-design/icons-vue';
import {defineComponent, ref} from 'vue';

export default defineComponent({
  setup() {
    const checked = ref(true);
    return {
      checked,
    };
  },
  components: {
    PieChartOutlined,
    DesktopOutlined,
    UserOutlined,
    TeamOutlined,
    FileOutlined,
    HomeOutlined,
  },

  data() {
    return {
      collapsed: ref(false),
      selectedKeys: ref(['1']),
      menu_list: [
        {
          id: 1, icon: 'mail', title: '展示中心', tube: '', 'menu_url': '/uric/show_center', children: []
        },
        {
          id: 2, icon: 'mail', title: '资产管理', 'menu_url': '/uric/host', children: []
        },
        {
          "id": 3, icon: 'bold', title: '批量任务', tube: '', menu_url: '/uric/workbench', children: [
            {id: 10, icon: 'mail', title: '执行任务', 'menu_url': '/uric/multi_exec'},
            {id: 11, icon: 'mail', title: '命令管理', 'menu_url': '/uric/template_manage'},
          ]
        },
        {
          id: 4, icon: 'tool', title: '设备管理', 'menu_url': '/uric/device_manage', children: []
        },
        {
          id: 7, icon: 'monitor', title: '监控预警', tube: '', menu_url: '/uric/workbench', children: [
            {id: 23, title: '系统监控', 'menu_url': '/uric/monitor/system'},
            {id: 24, title: '应用监控', 'menu_url': '/uric/monitor/application'},
            {id: 25, title: '告警规则', 'menu_url': '/uric/monitor/alert-rules'},
            {id: 26, title: '告警历史', 'menu_url': '/uric/monitor/alert-history'}
          ]
        }
      ]
    };
  },
  methods: {
    logout() {
      let self = this;
      this.$confirm({
        title: 'Uric系统提示',
        content: '您确认要注销登陆吗？',
        onOk() {
          self.$store.commit('setToken', '')
          self.$router.push('/login')
        }
      })
    },
  }
});
</script>

<style>
#components-layout-demo-side .logo {
  height: 32px;
  margin: 16px;
}

.site-layout .site-layout-background {
  background: #fff;
}

[data-theme='dark'] .site-layout .site-layout-background {
  background: #141414;
}

.logout {
  line-height: 1.5715;
}
</style>