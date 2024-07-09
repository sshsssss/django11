import Vue from 'vue'
import Router from 'vue-router'

Vue.use(Router)

/* Layout */
import Layout from '@/layout'

/**
 * Note: sub-menu only appear when route children.length >= 1
 * Detail see: https://panjiachen.github.io/vue-element-admin-site/guide/essentials/router-and-nav.html
 *
 * hidden: true                   if set true, item will not show in the sidebar(default is false)
 * alwaysShow: true               if set true, will always show the root menu
 *                                if not set alwaysShow, when item has more than one children route,
 *                                it will becomes nested mode, otherwise not show the root menu
 * redirect: noRedirect           if set noRedirect will no redirect in the breadcrumb
 * name:'router-name'             the name is used by <keep-alive> (must set!!!)
 * meta : {
    roles: ['admin','editor']    control the page roles (you can set multiple roles)
    title: 'title'               the name show in sidebar and breadcrumb (recommend set)
    icon: 'svg-name'/'el-icon-x' the icon show in the sidebar
    breadcrumb: false            if set false, the item will hidden in breadcrumb(default is true)
    activeMenu: '/example/list'  if set path, the sidebar will highlight the path you set
  }
 */

/**
 * constantRoutes
 * a base page that does not have permission requirements
 * all roles can be accessed
 */
export const teacherRoutes = [
  {
    path: '/login',
    component: () => import('@/views/login/index'),
    hidden: true
  },

  {
    path: '/404',
    component: () => import('@/views/404'),
    hidden: true
  },
  {
    path: '/',
    component: Layout,
    redirect: '/dashboard',
    children: [{
      path: 'dashboard',
      name: 'Dashboard',
      component: () => import('@/views/dashboard/index'),
      meta: { title: 'Dashboard', icon: 'dashboard' }
    }]
  },
  {
    path: '/manage',
    component: Layout,
    redirect: '/manage/image',
    name: '管理',
    meta: { title: '管理', icon: 'el-icon-s-help' },
    children: [
      {
        path: 'user',
        name: 'user',
        component: () => import('@/views/table/manage_user'),
        meta: { title: '用户管理', icon: 'table' }
      },
      {
        path: 'image',
        name: 'Image',
        component: () => import('@/views/table/index'),
        meta: { title: '镜像管理', icon: 'table' }
      },
      {
        path: 'course',
        name: 'Course',
        component: () => import('@/views/table/course'),
        meta: { title: '课程管理', icon: 'table' }
      },
      {
        path: 'course_detail',
        name: 'Course_detail',
        component: () => import('@/views/table/course_detail')
      },
      {
        path: 'container_detail',
        name: 'Container_detail',
        component: () => import('@/views/table/container_detail')
      },
      
    ]
  },

  {
    path: '/exam',
    component: Layout,
    name: 'ExamPage',
    meta: {
      title: '题库管理',
      icon: 'exam'
    },
    children: [
      {
        path: 'paper/list',
        component: () => import('@/views/exam/paper/list'),
        name: 'ExamPaperPageList',
        meta: { title: '考试列表', noCache: true }
      },
      {
        path: 'paper/edit',
        component: () => import('@/views/exam/paper/edit'),
        name: 'ExamPaperEdit',
        meta: { title: '考试编辑', noCache: true, activeMenu: '/exam/paper/list' },
        hidden: true
      },
      {
        path: 'question/list',
        component: () => import('@/views/exam/question/list'),
        name: 'ExamQuestionPageList',
        meta: { title: '题库', noCache: true }
      },
      {
        path: 'question/edit/singleChoice',
        component: () => import('@/views/exam/question/edit/single-choice'),
        name: 'singleChoicePage',
        meta: { title: '单选题编辑', noCache: true, activeMenu: '/exam/question/list' },
        hidden: true
      },
      {
        path: 'question/edit/multipleChoice',
        component: () => import('@/views/exam/question/edit/multiple-choice'),
        name: 'multipleChoicePage',
        meta: { title: '多选题编辑', noCache: true, activeMenu: '/exam/question/list' },
        hidden: true
      },
      {
        path: 'question/edit/trueFalse',
        component: () => import('@/views/exam/question/edit/true-false'),
        name: 'trueFalsePage',
        meta: { title: '判断题编辑', noCache: true, activeMenu: '/exam/question/list' },
        hidden: true
      },
      {
        path: 'question/edit/gapFilling',
        component: () => import('@/views/exam/question/edit/gap-filling'),
        name: 'gapFillingPage',
        meta: { title: '填空题编辑', noCache: true, activeMenu: '/exam/question/list' },
        hidden: true
      },
      {
        path: 'question/edit/shortAnswer',
        component: () => import('@/views/exam/question/edit/short-answer'),
        name: 'shortAnswerPage',
        meta: { title: '简答题编辑', noCache: true, activeMenu: '/exam/question/list' },
        hidden: true
      }
    ]
  },
  {
    path: '/education',
    component: Layout,
    name: 'EducationPage',
    meta: {
      title: '学科管理',
      icon: 'education'
    },
    alwaysShow: true,
    children: [
      {
        path: 'subject/list',
        component: () => import('@/views/education/subject/list'),
        name: 'EducationSubjectPage',
        meta: { title: '学科列表', noCache: true }
      },
      {
        path: 'subject/edit',
        component: () => import('@/views/education/subject/edit'),
        name: 'EducationSubjectEditPage',
        meta: { title: '学科编辑', noCache: true, activeMenu: '/education/subject/list' },
        hidden: true
      }
    ]
  },
  {
    path: '/answer',
    component: Layout,
    name: 'AnswerPage',
    meta: {
      title: '成绩管理',
      icon: 'answer'
    },
    alwaysShow: true,
    children: [
      {
        path: 'list',
        component: () => import('@/views/answer/list'),
        name: 'AnswerPageList',
        meta: { title: '答卷列表', noCache: true }
      }
    ]
  },
  {
    path: '/experiment',
    name: 'Experiment',
    component: () => import('@/views/table/experiment')
  },

  {
    path: '/form',
    component: Layout,
    meta: { title: '编辑', icon: 'form' },
    children: [
      {
        path: 'chapter_add',
        name: '章节添加',
        component: () => import('@/views/form/chapter_add'),
        meta: { title: '章节添加', icon: 'form' }
      },
      {
        path: 'course_add',
        name: '课程添加',
        component: () => import('@/views/form/course_add'),
        meta: { title: '课程添加', icon: 'form' }
      },

    ]
  },

  // 404 page must be placed at the end !!!
  { path: '*', redirect: '/404', hidden: true }
]

export const studentRoutes = [
  {
    path: '/login',
    component: () => import('@/views/login/index'),
    hidden: true
  },

  {
    path: '/404',
    component: () => import('@/views/404'),
    hidden: true
  },
  {
    path: '/',
    component: Layout,
    redirect: '/experiment_list',
    name: '实验列表',
    meta: { title: '实验列表', icon: 'form' },
    children: [
      {
        path: 'experiment_list',
        name: 'Form',
        component: () => import('@/views/student/experiment_list'),
        meta: { title: '实验列表', icon: 'form' }
      },
      {
        path: 'experiment_detail',
        name: 'Form',
        component: () => import('@/views/student/experiment_detail'),
      }
    ]
  },
  {
    path: '/dashboard',
    component: Layout,
    redirect: '/dashboard/dashboard',
    children: [{
      path: 'dashboard',
      name: 'Dashboard',
      component: () => import('@/views/dashboard/studentdash'),
      meta: { title: '用户信息', icon: 'dashboard' }
    }]
  },
  {
    path: '/experiment',
    name: 'Experiment',
    component: () => import('@/views/table/experiment')
  },


  {
    path: '/index',
    component: Layout,
    name: '首页',
    children: [{
      path: '',
      component: () => import('@/views/student/dashboard/index'),
      name: '首页',
      meta: { title: '首页' }
    }]
  },
  {
    path: '/paper',
    component: Layout,
    children: [
      {
        path: 'index',
        component: () => import('@/views/student/paper/index'),
        name: 'PaperIndex',
        meta: { title: '考试中心' }
      }
    ]
  },
  {
    path: '/record',
    component: Layout,
    children: [
      {
        path: 'index',
        component: () => import('@/views/student/record/index'),
        name: 'RecordIndex',
        meta: { title: '考试记录' }
      }
    ]
  },
  {
    path: '/question',
    component: Layout,
    children: [
      {
        path: 'index',
        component: () => import('@/views/student/question-error/index'),
        name: 'QuestionErrorIndex',
        meta: { title: '错题本' }
      }
    ]
  },
  { path: '/do', name: 'ExamPaperDo', component: () => import('@/views/student/exam/paper/do'), meta: { title: '考试答题' } },
  { path: '/edit', name: 'ExamPaperEdit', component: () => import('@/views/student/exam/paper/edit'), meta: { title: '考试批改' } },
  { path: '/read', name: 'ExamPaperRead', component: () => import('@/views/student/exam/paper/read'), meta: { title: '考试查看' } },

  // 404 page must be placed at the end !!!
  { path: '*', redirect: '/404', hidden: true }
]


const getRoutesByUserType = (router) => {
  const usertype = localStorage.getItem('status')
  console.log(usertype)
  if (usertype === 'teacher') {
    return teacherRoutes
  }
  else {
    return studentRoutes
  }
}


const createRouter = () => new Router({
  // mode: 'history', // require service support
  scrollBehavior: () => ({ y: 0 }),
  routes: getRoutesByUserType()
})

const router = createRouter()

export function resetRouter() {
  const newRouter = createRouter()
  router.matcher = newRouter.matcher // reset router
}

export default router
