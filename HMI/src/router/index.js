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
								path: '/hmi/list',
								component: resolve => require(['../components/myWork/List'],resolve),
								name: 'List'
							},
							{
								path: '/hmi/External_QA',
								component: resolve => require(['../components/myWork/External_QA'], resolve),
								name: 'External_QA'
							},
							{
								path: '/hmi/Internal_QA',
								component: resolve => require(['../components/myWork/Internal_QA'], resolve),
								name: 'Internal_QA'
							},
							{
								path: '/hmi/External_BUG',
								component: resolve => require(['../components/myWork/External_BUG'], resolve),
								name: 'External_BUG'
							},{
								path: '/hmi/Statistic_author_Category_Map',
								component: resolve => require(['../components/myWork/Statistic_author_Category_Map'], resolve),
								name: 'Statistic_author_Category_Map'
							},
							{
								path: '/hmi/Class',
								component: resolve => require(['../components/myWork/Statistic_Class'],resolve),
								name: 'Statistic_Class'
							},
							{
								path: '/hmi/Statistic_author_Category',
								component: resolve => require(['../components/myWork/Statistic_author_Category'],resolve),
								name: 'Statistic_author_Category'
							},
							{
								path: '/hmi/Statistic_screen_it',
								component: resolve => require(['../components/myWork/Statistic_screen_it'],resolve),
								name: 'Statistic_screen_it'
							},
							{
								path: '/hmi/TAGL_IT_Schedule',
								component: resolve => require(['../components/myWork/TAGL_IT_Schedule'],resolve),
								name: 'TAGL_IT_Schedule'
							},
						]
					},
					{
						path: '/hmi/ImportExport',
						component: resolve => require(['../components/myWork/ImportExport'],resolve),
						name: 'ImportExport'
					},
					{
						path: '/hmi/User',
						component: resolve => require(['../components/myWork/User'],resolve),
						name: 'User'
					},
					{
						path: '/hmi/MoveIn',
						component: resolve => require(['../components/myWork/MoveIn'],resolve),
						name: 'MoveIn'
					},
					{
						path: '/hmi/AfterMoveIn',
						component: resolve => require(['../components/myWork/Screen_migration'],resolve),
						name: 'AfterMoveIn'
					},
					{
						path: '/hmi/ItProReportStauts',
						component: resolve => require(['../components/myWork/ItProReportStauts'],resolve),
						name: 'ItProReportStauts'
					},
					{
						path: '/hmi/ItDevStauts',
						component: resolve => require(['../components/myWork/ItDev'],resolve),
						name: 'ItDevStauts'
					},
					{
						path: '/hmi/History',
						component: resolve => require(['../components/myWork/History'],resolve),
						name: 'History'
					},
					{
						path: '/hmi/Account',
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
