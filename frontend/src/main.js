import Vue from 'vue'
import App from './App.vue'
import router from './router'

Vue.config.productionTip = false

// 개발 환경에서만 개발자 도구 활성화
Vue.config.devtools = true;


new Vue({
  router,
  render: h => h(App)
}).$mount('#app')

