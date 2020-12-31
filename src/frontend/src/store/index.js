import Vue from 'vue';
import Vuex from 'vuex';
import axios from 'axios';
import VueAxios from 'vue-axios';

Vue.use(Vuex);//load vuex
Vue.use(VueAxios, axios)

export default new Vuex.Store({
  state: {
    selected_searches: [],
    commonurl: 'http://127.0.0.1:5000/'
  },
  getters: {
    basic_results: state => {
      return state.basic_results;
    }
  },
  mutations: {
    set_selected_searches(state, selected_searches) {
      state.selected_searches = selected_searches
    }
  },
  actions: {
  },
  modules: {}
});
