import Vue from 'vue'
import Router from 'vue-router'
Vue.use(Router)
export default new Router({
    routes: [
        {
            path: '*',
            redirect: {
                name: 'login'
            }
        },
        {
            path: '/login',
            component: resolve => require(['@/views/login/login'], resolve),
            name: 'login'
        },
        {
            path: '/homepage',
            component: resolve => require(['@/views/homepage.vue'], resolve),
            name: "homepage",
            redirect: '/item0',
            children: [
                {
                    path: '/item0',
                    component: resolve => require(['@/views/item0'], resolve),
                    name: 'item0',
                    meta: { title: 'item0' }
                },
                {
                    path: '/item1',
                    component: resolve => require(['@/views/excel/excelOne'], resolve),
                    name: 'item1',
                    meta: { title: 'item1' }
                }, {
                    path: '/item2',
                    component: resolve => require(['@/views/excel/excelTwo'], resolve),
                    name: 'item2',
                    meta: { title: 'item2' }
                }, {
                    path: '/item3',
                    component: resolve => require(['@/views/excel/excelThree'], resolve),
                    name: 'item3',
                    meta: { title: 'item3' }
                }, {
                    path: '/item4',
                    component: resolve => require(['@/views/item4'], resolve),
                    name: 'item4',
                    meta: { title: 'item4' }
                }, {
                    path: '/item5',
                    component: resolve => require(['@/views/item5'], resolve),
                    name: 'item5',
                    meta: { title: 'item5' }
                }, {
                    path: '/item6',
                    component: resolve => require(['@/views/item6'], resolve),
                    name: 'item6',
                    meta: { title: 'item6' }
                }, {
                    path: '/item7',
                    component: resolve => require(['@/views/item7'], resolve),
                    name: 'item7',
                    meta: { title: 'item7' }
                }, {
                    path: '/item8',
                    component: resolve => require(['@/views/item8'], resolve),
                    name: 'item8',
                    meta: { title: 'item8' }
                }
            ]
        },
        {
            path: '/add_project',
            component: resolve => require(['@/views/project/add_project'], resolve),
            name: 'add_project',
            meta: { title: 'add_project' }
        },
        {
            path: '/project_list',
            component: resolve => require(['@/views/project/project_list'], resolve),
            name: 'project_list',
            meta: { title: 'project_list' }
        },
        {
            path: '/project_detail',
            component: resolve => require(['@/views/project/project_detail'], resolve),
            name: 'project_detail',
            meta: { title: 'project_detail' }
        },
    ]
})
