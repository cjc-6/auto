import {createRouter, createWebHistory} from 'vue-router'
import ShowCenter from '../views/ShowCenter.vue'
import Login from '../views/Login.vue'
import Base from '../views/Base'
import Host from '../views/Host'
import Console from '../views/Console'
import MultiExec from '../views/MultiExec'
import SystemMonitor from '../views/monitor/SystemMonitor.vue'
import AppMonitor from '../views/monitor/AppMonitor.vue'
import AlertRules from '../views/monitor/AlertRules.vue'
import AlertHistory from '../views/monitor/AlertHistory.vue'
import TemplateManage from '../views/TemplateManage.vue'
import DeviceManage from '../views/DeviceManage.vue'
import store from "../store"

const routes = [
    {
        path: '/login',
        name: 'Login',
        component: Login,
        meta: {
            title: '账户登录',
            authenticate: false,
        }
    },
    {
        path: '/uric',
        name: 'Base',
        component: Base,
        meta: {
            authenticate: true,
        },
        children: [
            {
                meta: {
                    title: '展示中心',
                    authenticate: true,
                },
                path: 'show_center',
                name: 'ShowCenter',
                component: ShowCenter
            },
            {
                meta: {
                    title: '资产管理',
                    authenticate: true,
                },
                path: 'host',
                name: 'Host',
                component: Host
            },
            {
                meta: {
                    title: 'Console',
                    authenticate: true,
                },
                path: 'console/:host_id',
                name: 'Console',
                component: Console
            },
            {
                path: 'multi_exec',
                name: 'MultiExec',
                component: MultiExec,
                meta: {
                    title: '批量执行',
                    authenticate: true,
                }
            },
            {
                path: 'template_manage',
                name: 'TemplateManage',
                component: TemplateManage,
                meta: {
                    title: '命令管理',
                    authenticate: true,
                }
            },
            {
                path: 'device_manage',
                name: 'DeviceManage',
                component: DeviceManage,
                meta: {
                    title: '设备管理',
                    authenticate: true,
                }
            },
            {
                path: 'monitor/system',
                name: 'SystemMonitor',
                component: SystemMonitor,
                meta: {
                    title: '系统监控',
                    authenticate: true,
                }
            },
            {
                path: 'monitor/application',
                name: 'AppMonitor',
                component: AppMonitor,
                meta: {
                    title: '应用监控',
                    authenticate: true,
                }
            },
            {
                path: 'monitor/alert-rules',
                name: 'AlertRules',
                component: AlertRules,
                meta: {
                    title: '告警规则',
                    authenticate: true,
                }
            },
            {
                path: 'monitor/alert-history',
                name: 'AlertHistory',
                component: AlertHistory,
                meta: {
                    title: '告警历史',
                    authenticate: true,
                }
            }
        ]
    },
    {
        path: '/',
        redirect: '/login'
    }
];

const router = createRouter({
    history: createWebHistory(process.env.BASE_URL),
    routes
})

router.beforeEach((to, from, next) => {
    if (to.meta.title) {
        document.title = to.meta.title;
    }

    if (to.meta.authenticate && !store.getters.token) {
        next({name: "Login"})
    } 
    else if (store.getters.token && to.name === 'Login') {
        next({name: "ShowCenter"})
    }
    else {
        next()
    }
});

export default router

