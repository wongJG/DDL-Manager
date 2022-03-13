import Vue from 'vue';
import VueRouter from 'vue-router';
import Deadline from '../components/Deadline.vue';

Vue.use(VueRouter);

const routes = [
  {
    path: '/',
    name: 'Deadline',
    component: Deadline,
  },
  {
    path: '/about',
    name: 'About',
    // route level code-splitting
    // this generates a separate chunk (about.[hash].js) for this route
    // which is lazy-loaded when the route is visited.
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
