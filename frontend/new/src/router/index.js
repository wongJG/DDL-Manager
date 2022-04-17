import Vue from 'vue';
import VueRouter from 'vue-router';
import Deadline from '../components/Deadline.vue';
// import Calendar from '../components/Calendar.vue';
import Project from '../components/Project.vue';
import Register from '../components/Register.vue';
import Settings from '../components/Settings.vue';
import Admin from '../components/Admin.vue';

Vue.use(VueRouter);

const routes = [
  {
    path: '/',
    name: 'Deadline',
    component: Deadline,
  },
  {
    path: '/register',
    name: 'Register',
    component: Register,
  },
  {
    path: '/settings',
    name: 'Settings',
    component: Settings,
  },
  {
    path: '/admin',
    name: 'Admin',
    component: Admin,
  },
  {
    path: '/project',
    name: 'project',
    component: Project,
  },
  {
    path: '/about',
    name: 'About',
    component: () => import(/* webpackChunkName: "about" */ '../views/About.vue'),
  },
  {
    path: '/404',
    name: '404',
    component: () => import(/* webpackChunkName: "about" */ '../views/404.vue'),
  },
  {
    path: '*',
    redirect: '/404',
    name: 'notFound',
    hidden: true,
  },
];

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes,
});

export default router;
