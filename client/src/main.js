// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'
import App from './App'
import router from './router'
import VueSocketio from 'vue-socket.io';

// This one for Development
// Vue.use(VueSocketio, 'http://0.0.0.0:8888');

// This one for Production.
Vue.use(VueSocketio, 'http://138.68.59.8:215');

Vue.config.productionTip = false

/* eslint-disable no-new */
new Vue({
  el: '#app',
  router,
  components: { App },
  template: '<App/>'
})
