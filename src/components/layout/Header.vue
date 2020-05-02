<template>
  <nav class="navbar navbar-expand-md navbar-light bg-light pb-1 pt-1 noselect">
    <div class="container">
      <span class="navbar-brand">Job Tracker</span>
      <button
        class="navbar-toggler"
        type="button"
        data-toggle="collapse"
        data-target="#navbarTogglerDemo02"
        aria-controls="navbarTogglerDemo02"
        aria-expanded="false"
        aria-label="Toggle navigation"
      >
        <span class="navbar-toggler-icon"></span>
      </button>

      <div class="collapse navbar-collapse" id="navbarTogglerDemo02">
        <ul class="navbar-nav ml-auto mt-2 mt-lg-0">
          <li class="nav-item" v-if="!isAuthenticated">
            <router-link to="/" class="nav-link" exact active-class="active"
              >Home</router-link
            >
          </li>
          <li class="nav-item" v-if="!isAuthenticated">
            <router-link
              to="/login"
              class="nav-link"
              exact
              active-class="active"
              >Login</router-link
            >
          </li>
          <li class="nav-item" v-if="!isAuthenticated">
            <router-link
              to="/register"
              class="nav-link"
              exact
              active-class="active"
              >Register</router-link
            >
          </li>
          <li class="nav-item" v-if="isAuthenticated">
            <router-link to="/jobs" class="nav-link" exact active-class="active"
              >Jobs</router-link
            >
          </li>
          <li class="nav-item" v-if="isAuthenticated">
            <router-link
              to="/stats"
              class="nav-link"
              exact
              active-class="active"
              >Stats</router-link
            >
          </li>
          <li class="nav-item" v-if="isAuthenticated">
            <router-link
              to="/profile"
              class="nav-link"
              exact
              active-class="active"
              >Profile</router-link
            >
          </li>
          <li class="nav-item" v-if="isAuthenticated">
            <button class="nav-link logout-btn" @click="clickLogout">
              Logout
            </button>
          </li>
        </ul>
      </div>
    </div>
  </nav>
</template>

<script>
import { mapActions, mapState } from "vuex";

export default {
  name: "Header",
  computed: {
    ...mapState({
      isAuthenticated: (state) => state.auth.isAuthenticated,
    }),
  },
  methods: {
    ...mapActions(["logout"]),
    clickLogout() {
      this.logout();
      this.$router.push({ path: "/" });
    },
  },
};
</script>

<style scoped>
.noselect {
  user-select: none;
}

.logout-btn {
  cursor: pointer;
  text-transform: uppercase;
  font-weight: 600;
  border: 0;
  background: none;
}
</style>
