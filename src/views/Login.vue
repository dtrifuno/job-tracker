<template>
  <div>
    <div class="col-md-6 m-auto">
      <div class="card card-body mt-5">
        <h2 class="text-center">Login</h2>
        <form @submit.prevent="pressLogin">
          <div class="form-group">
            <label for="usernameInput">Username</label>
            <input
              type="text"
              class="form-control"
              v-model="username"
              id="usernameInput"
            />
          </div>
          <div class="form-group">
            <label for="passwordInput">Password</label>
            <input
              type="password"
              class="form-control"
              v-model="password"
              id="passwordInput"
            />
          </div>
          <div class="form-group">
            <button type="submit" class="btn btn-primary">
              Login
            </button>
          </div>
        </form>
        <small class="text-muted form-text">
          Don't have an account?
          <router-link to="/register">Click here</router-link>
          to register instead.
        </small>
      </div>
    </div>
  </div>
</template>

<script>
import { mapActions } from "vuex";

export default {
  name: "Login",
  data() {
    return {
      username: "",
      password: "",
    };
  },
  methods: {
    ...mapActions(["login"]),
    pressLogin() {
      const user = { username: this.username, password: this.password };
      this.login(user)
        .then(() => this.$router.push({ name: "jobs" }))
        .catch((err) => err);
    },
  },
};
</script>