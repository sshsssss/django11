import Vue from 'vue'
import Vuex from 'vuex'
import getters from './getters'
import app from './modules/app'
import settings from './modules/settings'
import user from './modules/user'
import enumItem from './modules/enumItem'; 
import exam from './modules/exam';
import userManage from './modules/userManage';
import tagsView from './modules/tagsView'

Vue.use(Vuex)

const store = new Vuex.Store({
  modules: {
    app,
    settings,
    user,
    enumItem,
    exam,
    userManage,
    tagsView
  },
  getters
})

export default store
