import Vue from 'vue'
import Router from 'vue-router'

Vue.use(Router)

const router = new Router({
  routes: [
    //登录注册页面
    {
      path: '/login',
      component: resolve => require(['../components/login'], resolve),
      name: 'Login'
    },
    {
      path: '/tab',
      component: resolve => require(['../components/tab'], resolve),
      name: 'tab'
    },
    {
      path: '/homepage',
      component: resolve => require(['../components/homePage'], resolve),
      name: 'HomePage',
      children: [{
          path: '/homepage/mywork',
          component: resolve => require(['../components/myWork/myWork'], resolve),
          name: 'Mywork',
          children: [{
              path: '/tagl/Form_Modle',
              component: resolve => require(['../components/myWork/Form_Modle'], resolve),
              name: 'Form_Modle',
            },
            {
              path: '/tagl/Form_Modle/Add_Form',
              component: resolve => require(['../components/myWork/Add_Form'], resolve),
              name: 'Add_Form',
            },
            {
              path: '/tagl/Form_Modle/Edit_Form',
              component: resolve => require(['../components/myWork/Edit_Form'], resolve),
              name: 'Edit_Form',
            },
            {
              path: '/tagl/Doc_Exhibition',
              component: resolve => require(['../components/myWork/doc_exhibition'], resolve),
              name: 'docExhibition'
            },
            {
              path: '/tagl/TAGLStauts',
              component: resolve => require(['../components/myWork/ItDev'], resolve),
              name: 'TAGLStauts'
            },
          ]
        },
        {
          path: '/tagl/Map_Modle',
          component: resolve => require(['../components/myWork/Map_Modle_First'], resolve),
          name: 'Map_Modle'
        },
        {
          path: '/tagl/Map_Modle_Deep',
          component: resolve => require(['../components/myWork/Map_Modle_Two'], resolve),
          name: 'Map_Modle_Deep'
        },
        {
          path: '/tagl/Map_Modle_Final',
          component: resolve => require(['../components/myWork/Map_Modle_Final'], resolve),
          name: 'Map_Modle_Final'
        },
        {
          path: '/tagl/File_Modle',
          component: resolve => require(['../components/myWork/File_Modle'], resolve),
          name: 'File_Modle'
        },
        {
            path: '/tagl/IF_upload/:docid',
            component: resolve => require(['../components/myWork/IF_upload'], resolve),
            name: 'IF_upload'
        },
        {
            path: '/tagl/develop_design',
            component: resolve => require(['../components/myWork/develop_design'], resolve),
            name: 'develop_design'
        },
        {
            path: '/tagl/basic_design_usecase_edit/:docid/:title',
            component: resolve => require(['../components/myWork/basicDesignUsecaseEdit'], resolve),
            name: 'basic_design_usecase_edit'
        },
        {
            path: '/tagl/basic_design_usecase_add/:docid/:title',
            component: resolve => require(['../components/myWork/basicDesignUsecaseAdd'], resolve),
            name: 'basic_design_usecase_add'
        },
        {
            path: '/tagl/detail_design_usecase_edit/:docid/:title',
            component: resolve => require(['../components/myWork/detailDesignUsecaseEdit'], resolve),
            name: 'detail_design_usecase_edit'
        },
        {
            path: '/tagl/detail_design_usecase_add/:docid/:title',
            component: resolve => require(['../components/myWork/detailDesignUsecaseAdd'], resolve),
            name: 'detail_design_usecase_add'
        },
        {
            path: '/tagl/basic_design_sequence_edit/:usecaseId/:title',
            component: resolve => require(['../components/myWork/basicDesignSequenceEdit'], resolve),
            name: 'basic_design_sequence_edit'
        },
        {
            path: '/tagl/if_design_usecase_edit/:docid/:title',
            component: resolve => require(['../components/myWork/IFUsecaseEdit'], resolve),
            name: 'if_design_usecase_edit'
        },

        {
            path: '/tagl/if_design_usecase_add/:docid/:title',
            component: resolve => require(['../components/myWork/IFUsecaseAdd'], resolve),
            name: 'if_design_usecase_add'
        },
        {
          path: '/tagl/File_design',
          component: resolve => require(['../components/myWork/File_design'], resolve),
          name: 'File_design',
          children: [{
              path: '/tagl/File_design/basic_design_template',
              component: resolve => require(['../components/myWork/basic_design_template'], resolve),
              name: 'basic_design_template',

            }, 

          ]
        },
        {
          path: '/tagl/File_design/Preview/:docId/:docType',
          component: resolve => require(['../components/myWork/Preview'], resolve),
          name: 'Preview',
        },
        {
          path: '/tagl/File_design/Preview_seq/:secid',
          component: resolve => require(['../components/myWork/Preview_seq'], resolve),
          name: 'Preview_seq',
        },
        {
          path: '/tagl/Spec_search/:proj',
          component: resolve => require(['../components/myWork/Spec_Search'], resolve),
          name: 'Spec_search',
        },
        {
          path: '/tagl/Add_NewProject',
          component: resolve => require(['../components/myWork/Add_NewProject'], resolve),
          name: 'Add_NewProject',
          children: [{
              path: '/tagl/Add_NewProject/ProjectTemplate',
              component: resolve => require(['../components/myWork/Add_ProjectTemplate'], resolve),
              name: 'ProjectTemplate',

            },
            {
              path: '/tagl/Add_NewProject/FramworkTemplate',
              component: resolve => require(['../components/myWork/Add_FramworkTemplate'], resolve),
              name: 'FramworkTemplate',

            },
            {
              path: '/tagl/Add_NewProject/ModelTemplate',
              component: resolve => require(['../components/myWork/Add_ModelTemplate'], resolve),
              name: 'ModelTemplate',

            }, {
              path: '/tagl/Add_NewProject/ModuleRelationship',
              component: resolve => require(['../components/myWork/ModuleRelationship'], resolve),
              name: 'ModelRelationship',

            }
          ]
        },
        {
          path: '/tagl/Tree_Map',
          component: resolve => require(['../components/myWork/Tree_Map'], resolve),
          name: 'Tree_Map'
        },
        {
          path: '/tagl/authorManage',
          component: resolve => require(['../components/myWork/AuthorManage'], resolve),
          name: 'authorManage'
        },
        {
          path: '/tagl/add_basic_design',
          component: resolve => require(['../components/myWork/Add_basic_design'], resolve),
          name: 'add_basic_design'
        },
        {
          path: '/tagl/add_detail_design',
          component: resolve => require(['../components/myWork/Add_detail_design'], resolve),
          name: 'add_detail_design'
        },
        {
          path: '/tagl/edit_summery',
          component: resolve => require(['../components/myWork/Edit_summery'], resolve),
          name: 'edit_summery'
        },
        {
          path: '/tagl/edit_detail_summary',
          component: resolve => require(['../components/myWork/Edit_Detail_Summary'], resolve),
          name: 'edit_detail_summary'
        },
        {
          path: '/tagl/edit_input',
          component: resolve => require(['../components/myWork/Edit_Input'], resolve),
          name: 'edit_input'
        },
        {
          path: '/tagl/edit_usecase',
          component: resolve => require(['../components/myWork/Edit_useacase'], resolve),
          name: 'edit_usecase'
        },
        {
          path: '/tagl/step4',
          component: resolve => require(['../components/myWork/step_checklist'], resolve),
          name: 'step_checklist'
        },
        {
          path: '/tagl/step3',
          component: resolve => require(['../components/myWork/step_Consider'], resolve),
          name: 'step_Consider',
        },
        {
          path: '/tagl/step2',
          component: resolve => require(['../components/myWork/step_SceneTwo'], resolve),
          name: 'step_SceneTwo'
        },
        {
          path: '/tagl/step1',
          component: resolve => require(['../components/myWork/step_Scene'], resolve),
          name: 'step_Scene'
        },
        {
          path: '/tagl/step_Input',
          component: resolve => require(['../components/myWork/step_input'], resolve),
          name: 'step_Input'
        },
        {
          path: '/tagl/step_Sequence',
          component: resolve => require(['../components/myWork/step_Sequence'], resolve),
          name: 'step_Sequence'
        },
        {
          path: '/tagl/step_STD',
          component: resolve => require(['../components/myWork/step_STD'], resolve),
          name: 'step_STD'
        },
        {
          path: '/tagl/step_Block',
          component: resolve => require(['../components/myWork/step_Block'], resolve),
          name: 'step_Block'
        },
        {
          path: '/tagl/step_other',
          component: resolve => require(['../components/myWork/step_other'], resolve),
          name: 'step_other'
        },
        {
          path: '/tagl/step_Class',
          component: resolve => require(['../components/myWork/step_Class'], resolve),
          name: 'step_Class'
        },
        {
          path: '/tagl/edit_IF/:docId/:docType',
          component: resolve => require(['../components/myWork/Edit_IF'], resolve),
          name: 'edit_IF'
        },
        {
          path: '/tagl/step_IF',
          component: resolve => require(['../components/myWork/step_IF'], resolve),
          name: 'step_IF'
        },
        {
          path: '/tagl/Project_Step_One',
          component: resolve => require(['../components/myWork/addProject/Add_Project_Step_One'], resolve),
          name: 'Add_Project_Step_One'
        },
        {
          path: '/tagl/Project_Step_Two',
          component: resolve => require(['../components/myWork/addProject/Add_Project_Step_Two'], resolve),
          name: 'Add_Project_Step_Two'
        },
        {
          path: '/tagl/Project_Step_Three',
          component: resolve => require(['../components/myWork/addProject/Add_Project_Step_Three'], resolve),
          name: 'Add_Project_Step_Three'
        },
        {
          path: '/tagl/Project_Step_Four',
          component: resolve => require(['../components/myWork/addProject/Add_Project_Step_Four'], resolve),
          name: 'Add_Project_Step_Four'
        },
        {
          path: '/tagl/Project_Step_Five',
          component: resolve => require(['../components/myWork/addProject/Add_Project_Step_Fifth'], resolve),
          name: 'Add_Project_Step_Five'
        },
        {
          path: '/tagl/ModuleSummary',
          component: resolve => require(['../components/myWork/addProject/ModuleSummary'], resolve),
          name: 'ModuleSummary'
        },
        {
          path: '/tagl/ModuleRelationshipEdit',
          component: resolve => require(['../components/myWork/Edit_Module_Relationship'], resolve),
          name: 'ModuleRelationshipEdit'
        },
        {
          path: '/tagl/FramworkSummary',
          component: resolve => require(['../components/myWork/addProject/FramworkSummary'], resolve),
          name: 'FramworkSummary'
        },
        {
          path: '/tagl/Framwork_Model',
          component: resolve => require(['../components/myWork/addProject/Framwork_Model'], resolve),
          name: 'Framwork_Model'
        },
        {
          path: '/tagl/Diff',
          component: resolve => require(['../components/myWork/Diff'], resolve),
          name: 'Diff'
        },
        {
          path: '/tagl/BookManagement',
          component: resolve => require(['../components/myWork/BookManagement'], resolve),
          name: 'BookManagement'
        },
        {
            path: '/tagl/BookList',
            component: resolve => require(['../components/myWork/BookList'], resolve),
            name: 'BookList'
        },
        {
            path: '/tagl/BookManagementList',
            component: resolve => require(['../components/myWork/BookManagementList'], resolve),
            name: 'BookManagementList'
        },
        {
            path: '/tagl/BugList',
            component: resolve => require(['../components/myWork/BugList'], resolve),
            name: 'BugList'
        },
      
      ]
    },
    {
      path: '*',
      redirect: {
        name: 'Login'
      }
    }
  ]
})
router.beforeEach((to, from, next) => {
  if (to.path === '/login') {
    if (window.sessionStorage.getItem('token')) {
      next(false)
    } else {
      next()
    }
  } else {
    if (!window.sessionStorage.getItem('token')) {
      next({
        path: '/login'
      })
    } else {
      next();
    }
  }
})


export default router;
