import Vue from "vue";
import VModal from "vue-js-modal";
import Notifications from "vue-notification";

import App from "./App";
import router from "./router";
import store from "./store";

Vue.config.productionTip = false;
Vue.use(VModal);
Vue.use(Notifications);

new Vue({
  router,
  store,
  render: (h) => h(App),
}).$mount("#app");
