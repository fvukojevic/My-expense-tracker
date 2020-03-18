import Vue from 'vue'
import Vuelidate from 'vuelidate'
import App from './App.vue'
import GSignInButton from 'vue-google-signin-button'
import store from './store/store';
import axios from 'axios';

Vue.use(GSignInButton);
Vue.use(Vuelidate);

Vue.prototype.$http = axios

Vue.config.productionTip = false;

new Vue({
  render: h => h(App),
  store
}).$mount('#app')
