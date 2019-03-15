import Vue from 'vue'
import VueRouter from 'vue-router'

Vue.use(VueRouter)

const router = new VueRouter({
  	routes: [
 		//登录注册页面
	 		{
	 			path: '/login',
	 			component: resolve => require(['../components/login'],resolve),
	 			name: 'Login'
	 		},
	 		{
	 			path: '/StyleTool',
	 			component: resolve => require(['../components/myWork/StyleTool'],resolve),
	 			name: 'StyleTool'
	 		},
	 		{
	 			path: '/homepage',
	 			component: resolve => require(['../components/homePage'],resolve),
				name: 'HomePage',
				children: [
					{
						path: '/homepage/mywork',
						component: resolve => require(['../components/myWork/myWork'],resolve),
						name: 'Mywork',
						children: [
							{
								path: '/homepage/mywork/list',
								component: resolve => require(['../components/myWork/List'],resolve),
								name: 'List'
							},
							{
								path: '/homepage/mywork/HU_compile',
								component: resolve => require(['../components/myWork/HU_compile'],resolve),
								name: 'HU_compile'
							},
							{
								path: '/homepage/mywork/ARL_all',
								component: resolve => require(['../components/myWork/ARL_all'],resolve),
								name: 'ARL_all'
							},{
								path: '/homepage/mywork/TAGL_definition',
								component: resolve => require(['../components/myWork/TAGL_definition'],resolve),
								name: 'TAGL_definition'
							},
							{
								path: '/homepage/mywork/CheckRule_HU',
								component: resolve => require(['../components/myWork/CheckRule_HU'],resolve),
								name: 'CheckRule_HU'
							},
							{
								path: '/homepage/mywork/CheckRule_TAGL',
								component: resolve => require(['../components/myWork/CheckRule_TAGL'],resolve),
								name: 'CheckRule_TAGL'
							},
							{
								path: '/homepage/mywork/Statistic_Function',
								component: resolve => require(['../components/myWork/Statistic_Function'],resolve),
								name: 'Statistic_Function'
							},
							{
								path: '/homepage/mywork/Statistic_Minor_Category',
								component: resolve => require(['../components/myWork/Statistic_Minor_Category'],resolve),
								name: 'Statistic_Minor_Category'
							},
							{
								path: '/homepage/mywork/Statistic_Group',
								component: resolve => require(['../components/myWork/Statistic_Group'],resolve),
								name: 'Statistic_Group'
							},
							{
								path: '/homepage/mywork/HUDef_BasicRequirement',
								component: resolve => require(['../components/myWork/HUDef_BasicRequirement'],resolve),
								name: 'HUDef_BasicRequirement'
							},
							{
								path: '/homepage/mywork/TAGLDef_BasicRequirement',
								component: resolve => require(['../components/myWork/TAGLDef_BasicRequirement'],resolve),
								name: 'TAGLDef_BasicRequirement'
							},
							{
								path: '/homepage/mywork/TAGLAna_BasicRequirement',
								component: resolve => require(['../components/myWork/TAGLAna_BasicRequirement'],resolve),
								name: 'TAGLAna_BasicRequirement'
							},
						]
					},
					{
						path: '/homepage/ARL',
						component: resolve => require(['../components/myWork/myWork'],resolve),
						name: 'ARL'
					},
					{
						path: '/homepage/ImportExport',
						component: resolve => require(['../components/myWork/ImportExport'],resolve),
						name: 'ImportExport'
					},
					{
						path: '/homepage/User',
						component: resolve => require(['../components/myWork/User'],resolve),
						name: 'User'
					},
					{
						path: '/homepage/History',
						component: resolve => require(['../components/myWork/History'],resolve),
						name: 'History'
					},
					{
						path: '/homepage/Account',
						component: resolve => require(['../components/myWork/Account'],resolve),
						name: 'Account'
					},
				]
	 		},
	 		{
	 			path: '*',
	 			redirect: { name:'Login'}
	 		}
	  ]
})
router.beforeEach((to,from,next) =>{
		if(to.path === '/login'){
			if(window.sessionStorage.getItem('admin')){
				next(false)				
			}else{
				next()
			}	
		}else{
				if(!window.sessionStorage.getItem('admin')){
					next({
						path:'/login'
					})
				}else{
					if(to.path === '/login'){
//						next(false)
					}else{
						next();
					}
				}
		}
})
	
export default router;
