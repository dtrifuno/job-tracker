import Vue from "vue";
import Vuex from "vuex";

import auth from "./modules/auth";
import jobDetails from "./modules/jobDetails";
import jobs from "./modules/jobs";
import notifications from "./modules/notifications";
import profile from "./modules/profile";
import spinners from "./modules/spinners";

Vue.use(Vuex);

export default new Vuex.Store({
  modules: {
    auth,
    jobDetails,
    jobs,
    notifications,
    profile,
    spinners
  },
});
