import Vue from 'vue';
import Router from 'vue-router';
import releases from './components/releasePage.vue';

Vue.use(Router);

export default new Router({
  mode: 'history',
  base: process.env.BASE_URL,
  routes: [
    {
      path: '/',
      name: 'releases',
      component: releases,
    },
  ],
});
