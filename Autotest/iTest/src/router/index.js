import Vue from 'vue'
import Router from 'vue-router'
import { getToken} from '@/utils/cookies'

Vue.use(Router)

import Homepage from '../views/homepage/Homepage'

export const routerMap = [{
    path: '*',
    redirect: {
        name: 'homepage'
    }
},
{
    path: '/login',
    name: 'login',
    component: resolve => require(['@/views/login/Login'], resolve)
},
{
    path: '/homepage',
    name: 'homepage',
    component: resolve => require(['@/views/homepage/Homepage'], resolve),
    redirect: '/dashboard',
    children: [{
        path: '/backstage',
        component: resolve => require(['@/views/backstage/Backstage'], resolve),
        name: 'backstage',
        children: [{
            path: '/backstage/countryManage',
            component: resolve => require(['@/views/backstage/countryManage/CountryManage'], resolve),
            name: 'countryManage',
            redirect: '/backstage/countryManage/countryManage',
            children: [{
                path: '/backstage/countryManage/countryManage',
                component: resolve => require(['@/views/backstage/countryManage/CountryShow'], resolve),
                name: 'CountryShow'
            }, {
                path: '/backstage/countryManage/edit',
                component: resolve => require(['@/views/backstage/countryManage/Edit'], resolve),
                name: 'countryManageEdit'
            }, {
                path: '/backstage/countryManage/add',
                component: resolve => require(['@/views/backstage/countryManage/Edit'], resolve),
                name: 'countryManageAdd'
            }]
        },
        {
            path: '/backstage/landManage',
            component: resolve => require(['@/views/backstage/landManage/LandManage'], resolve),
            name: 'landManage',
            redirect: '/backstage/landManage/landShow',
            children: [{
                path: '/backstage/landManage/landShow',
                component: resolve => require(['@/views/backstage/landManage/LandShow'], resolve),
                name: ''
            }, {
                path: '/backstage/landManage/edit',
                component: resolve => require(['@/views/backstage/landManage/Edit'], resolve),
                name: 'landManageEdit'
            }, {
                path: '/backstage/landManage/add',
                component: resolve => require(['@/views/backstage/landManage/Edit'], resolve),
                name: 'landManageAdd'
            }]
        },
        {
            path: '/backstage/customManage',
            component: resolve => require(['@/views/backstage/customManage/CustomManage'], resolve),
            name: 'customManage',
            redirect: '/backstage/customManage/customShow',
            children: [{
                path: '/backstage/customManage/customShow',
                component: resolve => require(['@/views/backstage/customManage/CustomShow'], resolve),
                name: ''
            }, {
                path: '/backstage/customManage/edit',
                component: resolve => require(['@/views/backstage/customManage/Edit'], resolve),
                name: 'customManageEdit'
            }, {
                path: '/backstage/customManage/add',
                component: resolve => require(['@/views/backstage/customManage/Edit'], resolve),
                name: 'customManageAdd'
            }]
        },
        {
            path: '/backstage/projectManage',
            component: resolve => require(['@/views/backstage/projectManage/ProjectManage'], resolve),
            name: 'projectManage',
            redirect: '/backstage/projectManage/projectShow',
            children: [{
                path: '/backstage/projectManage/projectShow',
                component: resolve => require(['@/views/backstage/projectManage/ProjectShow'], resolve),
                name: ''
            }, {
                path: '/backstage/projectManage/edit',
                component: resolve => require(['@/views/backstage/projectManage/Edit'], resolve),
                name: 'projectManageEdit'
            }, {
                path: '/backstage/projectManage/add',
                component: resolve => require(['@/views/backstage/projectManage/Edit'], resolve),
                name: 'projectManageAdd'
            }]
        },
        {
            path: '/backstage/keywordManage',
            component: resolve => require(['@/views/backstage/keywordManage/KeywordManage'], resolve),
            name: 'keywordManage',
            redirect: '/backstage/keywordManage/keywordShow',
            children: [{
                path: '/backstage/keywordManage/keywordShow',
                component: resolve => require(['@/views/backstage/keywordManage/KeywordShow'], resolve),
                name: ''
            }, {
                path: '/backstage/keywordManage/edit',
                component: resolve => require(['@/views/backstage/keywordManage/Edit'], resolve),
                name: 'keywordManageEdit'
            }, {
                path: '/backstage/keywordManage/add',
                component: resolve => require(['@/views/backstage/keywordManage/Edit'], resolve),
                name: 'keywordManageAdd'
            }]
        },
        {
            path: '/backstage/moduleManage',
            component: resolve => require(['@/views/backstage/moduleManage/ModuleManage'], resolve),
            name: 'moduleManage',
            redirect: '/backstage/moduleManage/moduleShow',
            children: [{
                path: '/backstage/moduleManage/moduleShow',
                component: resolve => require(['@/views/backstage/moduleManage/ModuleShow'], resolve),
                name: ''
            }, {
                path: '/backstage/moduleManage/edit',
                component: resolve => require(['@/views/backstage/moduleManage/Edit'], resolve),
                name: 'moduleManageEdit'
            },
            {
                path: '/backstage/moduleManage/add',
                component: resolve => require(['@/views/backstage/moduleManage/Edit'], resolve),
                name: 'moduleManageAdd'
            }]
        },
        {
            path: '/backstage/PersonnelManage',
            component: resolve => require(['@/views/backstage/PersonnelManage/PersonnelManage'], resolve),
            name: 'PersonnelManage',
            redirect: '/backstage/PersonnelManage/PersonnelShow',
            children: [{
                path: '/backstage/PersonnelManage/PersonnelShow',
                component: resolve => require(['@/views/backstage/PersonnelManage/PersonnelShow'], resolve),
                name: ''
            }, 
            ]
        },
        {
            path: '/backstage/RoleManage',
            component: resolve => require(['@/views/backstage/RoleManage/RoleManage'], resolve),
            name: 'RoleManage',
            redirect: '/backstage/RoleManage/RoleShow',
            children: [{
                path: '/backstage/RoleManage/RoleShow',
                component: resolve => require(['@/views/backstage/RoleManage/RoleShow'], resolve),
                name: 'RoleShow'
            }]
        }]
    }, {
        path: '/testCase',
        component: resolve => require(['@/views/testcase/TestCase'], resolve),
        name: 'testCase',
        redirect: '/testCase/testCaseShow',
        children: [{
            path: '/testCase/testCaseShow',
            component: resolve => require(['@/views/testcase/TestCaseShow'], resolve),
            name: ''
        }, {
            path: '/testCase/edit',
            component: resolve => require(['@/views/testcase/Edit'], resolve),
            name: 'testCaseEdit'
        }, {
            path: '/testCase/add',
            component: resolve => require(['@/views/testcase/Edit'], resolve),
            name: 'testCaseAdd'
        }, {
            path: '/testCase/preview',
            component: resolve => require(['@/views/testcase/Preview'], resolve),
            name: 'testCasePreview'
        }]
    }, {
        path: '/dashboard',
        component: resolve => require(['@/views/dashboard/dashboardShow'], resolve),
        name: 'dashboard',
    }, {
        path: '/testCase/diff',
        component: resolve => require(['@/views/testcase/TestDiff'], resolve),
        name: 'testCaseDiff'
    },{
        path: '/testPlan',
        component: resolve => require(['@/views/testPlan/TestPlan'], resolve),
        name: 'testPlan',
        redirect: '/testPlan/testPlanShow',
        children: [{
            path: '/testPlan/testPlanShow',
            component: resolve => require(['@/views/testPlan/TestPlanShow'], resolve),
            name: ''
        }, {
            path: '/testPlan/edit',
            component: resolve => require(['@/views/testPlan/TestPlanEdit'], resolve),
            name: 'testPlanEdit'
        }, {
            path: '/testPlan/add',
            component: resolve => require(['@/views/testPlan/TestPlanAdd'], resolve),
            name: 'testPlanAdd'
        }, {
            path: '/testPlan/preview',
            component: resolve => require(['@/views/testPlan/Preview'], resolve),
            name: 'testPlanPreview'
        }, {
            path: '/testPlan/execute',
            component: resolve => require(['@/views/testPlan/Execute'], resolve),
            name: 'testPlanExecute'
        }, {
            path: '/testPlan/history',
            component: resolve => require(['@/views/testPlan/TestPlanHistory'], resolve),
            name: 'testPlanHistory'
        }, {
            path: '/testPlan/planConfiguration',
            component: resolve => require(['@/views/testPlan/PlanConfiguration'], resolve),
            name: 'PlanConfiguration'
        }]
    }]
}]

const router = new Router({
    routes: routerMap
})

router.beforeEach((to, from, next) => {
    if (to.path === '/login') {
        // console.log(window.sessionStorage.getItem('Token'),'Token')
        if (window.sessionStorage.getItem('Token')) {
            next(false)
        } else {
            next()
        }
    } else {
        if (!window.sessionStorage.getItem('Token')) {
            next({
                path: '/login'
            })
        } else {
            next();
        }
    }
    
})

export default router
