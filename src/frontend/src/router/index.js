import Vue from 'vue';
import VueRouter from 'vue-router';
import Dashboard from '../views/Dashboard.vue'
import Search from '../views/Search.vue'
import AdvancedSearch from '../views/AdvancedSearch.vue'
import Candidates from '../views/Candidates.vue'
import PortalDocuments from '../views/PortalDocuments.vue'
import SearchResults from '../views/SearchResults.vue'
import SearchCountResults from '../views/SearchCountResults.vue'
import BnaUser from '../views/BnaUser.vue'
import DatabaseConn from '../views/DatabaseConn.vue'
import ServerVariables from '../views/ServerVariables.vue'
//import store from '../store';
//import Home from '../views/Home.vue';

Vue.use(VueRouter);

const routes = [
  {
    path: '/',
    name: 'Home',
    component: Dashboard
  },
  // {
  //   path: '/about',
  //   name: 'About',
  //   // route level code-splitting
  //   // this generates a separate chunk (about.[hash].js) for this route
  //   // which is lazy-loaded when the route is visited.
  //   component: () =>
  //     import(/* webpackChunkName: "about" */ '../views/About.vue')
  // },
  {
    path: '/search',
    name: 'search',
    component: Search
  },
  {
    path: '/advanced-search',
    name: 'advanced-search',
    component: AdvancedSearch
  },
  {
    path: '/candidates',
    name: 'candidates',
    component: Candidates
  },
  {
    path: '/portal',
    name: 'portal',
    component: PortalDocuments
  },
  {
    path: '/search-results',
    name: 'search-results',
    component: SearchResults
  },
  {
    path: '/search-count-results',
    name: 'search-count-results',
    component: SearchCountResults
  },
  {
    path: '/bna-user',
    name: 'bna-user',
    component: BnaUser
  },
  {
    path: '/database-conn',
    name: 'database-conn',
    component: DatabaseConn
  },
  {
    path: '/server-variables',
    name: 'server-variables',
    component: ServerVariables
  },
];

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes
});

export default router;
