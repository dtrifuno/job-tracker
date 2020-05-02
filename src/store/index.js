import Vue from "vue";
import Vuex from "vuex";

import auth from "./modules/auth";
import jobs from "./modules/jobs";
import profile from "./modules/profile";

Vue.use(Vuex);

export default new Vuex.Store({
  modules: {
    auth,
    jobs,
    profile,
  },
});
