import Vue from 'vue'
import Router from 'vue-router'
import tron from '@/components/tron'

Vue.use(Router)

export default new Router({
  routes: [
    {
      path: '/',
      name: 'tron',
      component: tron
    }
  ]
})
