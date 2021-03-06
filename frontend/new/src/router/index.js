import Vue from 'vue';
import VueRouter from 'vue-router';
import Deadline from '../components/Deadline.vue';
import Project from '../components/Project.vue';
import Register from '../components/Register.vue';
import Settings from '../components/Settings.vue';
import Admin from '../components/Admin.vue';
import Login from '../components/Login.vue';

Vue.use(VueRouter);

const routes = [
  {
    path: '/deadline',
    name: 'Deadline',
    component: Deadline,
    meta: {
      title: 'Deadline',
      requiresAuth: true,
    },
  },
  {
    path: '/',
    name: 'Login',
    component: Login,
    meta: {
      title: 'Login',
    },
  },
  {
    path: '/register',
    name: 'Register',
    component: Register,
    meta: {
      title: 'Register',
    },
  },
  {
    path: '/settings',
    name: 'Settings',
    component: Settings,
    meta: {
      title: 'Settings',
      requiresAuth: true,
    },
  },
  {
    path: '/admin',
    name: 'Admin',
    component: Admin,
    meta: {
      title: 'Admin',
      requiresAuth: true,
    },
  },
  {
    path: '/project',
    name: 'project',
    component: Project,
    meta: {
      title: 'Project',
      requiresAuth: true,
    },
  },
  {
    path: '/about',
    name: 'About',
    component: () => import(/* webpackChunkName: "about" */ '../views/About.vue'),
    meta: {
      title: 'About',
    },
  },
  {
    path: '/404',
    name: '404',
    component: () => import(/* webpackChunkName: "about" */ '../views/404.vue'),
  },
  {
    path: '/signout',
    name: 'logout',
    meta: {
      logout: true,
    },
  },
  {
    path: '*',        // All unmatched pages redirect to 404 page
    redirect: '/404',
    name: 'notFound',
    hidden: true,
  },
];

```Construct the router```
const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes,
});

router.beforeEach((to, from, next) => {     // Verified login state
  if (to.meta.title) {
    document.title = to.meta.title;
  }
  if (to.matched.some((record) => record.meta.requiresAuth)) {  // If the page require auth
    if (!sessionStorage.getItem('isLogin')) { // If it is not logged in
      next({
        path: '/',
        query: { redirect: to.fullPath },  // Go to login page
      });
    } else {
      next();                              // Go to the requested page
    }
  } else if (to.matched.some((record) => record.meta.logout)) {  // if logout is hit
    sessionStorage.clear();
    next({
      path: '/',
      query: { redirect: to.fullPath },    // redirect to login page
    });
  } else {
    next();
  }
});

export default router;
