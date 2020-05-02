import Vue from "vue";
import Router from "vue-router";

import store from "./store";
import Landing from "./views/Landing";

Vue.use(Router);

const bounceUnathorizedToLogin = (next) => {
  if (store.state.auth.isAuthenticated) {
    next();
  } else {
    next({
      name: "login",
    });
  }
};

const bounceAuthorizedToJobs = (next) => {
  if (!store.state.auth.isAuthenticated) {
    next();
  } else {
    next({
      name: "jobs",
    });
  }
};

export default new Router({
  routes: [
    // guest routes
    {
      path: "/",
      name: "landing",
      component: Landing,
      beforeEnter(to, from, next) {
        bounceAuthorizedToJobs(next);
      },
    },
    {
      path: "/login",
      name: "login",
      component: () =>
        import(/* webpackChunkName: "login" */ "./views/Login.vue"),
      beforeEnter(to, from, next) {
        bounceAuthorizedToJobs(next);
      },
    },
    {
      path: "/register",
      name: "register",
      component: () =>
        import(/* webpackChunkName: "register" */ "./views/Register.vue"),
      beforeEnter(to, from, next) {
        bounceAuthorizedToJobs(next);
      },
    },
    // auth routes
    {
      path: "/jobs",
      name: "jobs",
      component: () =>
        import(/* webpackChunkName: "jobs" */ "./views/Jobs/index.vue"),
      beforeEnter(to, from, next) {
        bounceUnathorizedToLogin(next);
      },
    },
    {
      path: "/stats",
      name: "stats",
      component: () =>
        import(/* webpackChunkName: "stats" */ "./views/Stats.vue"),
      beforeEnter(to, from, next) {
        bounceUnathorizedToLogin(next);
      },
    },
    {
      path: "/profile",
      name: "profile",
      component: () =>
        import(/* webpackChunkName: "profile" */ "./views/Profile/index.vue"),
      beforeEnter(to, from, next) {
        bounceUnathorizedToLogin(next);
      },
    },
  ],
});
