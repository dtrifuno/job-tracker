<template>
  <div>
    <div class="col-md-6 m-auto">
      <div class="card card-body mt-5">
        <h2 class="text-center">Register</h2>
        <form @submit.prevent="pressRegister">
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
            <label for="confirmPasswordInput">Confirm Password</label>
            <input
              type="password"
              class="form-control"
              v-model="confirmPassword"
              id="confirmPasswordInput"
            />
          </div>
          <div class="form-group">
            <button type="submit" class="btn btn-primary">
              Register
            </button>
          </div>
        </form>
        <small class="text-muted form-text">
          Already have an account?
          <router-link to="/login">Click here</router-link>
          to login instead.
        </small>
      </div>
    </div>
  </div>
</template>

<script>
import { mapActions } from "vuex";

export default {
  name: "Register",
  data() {
    return {
      username: "",
      password: "",
      confirmPassword: "",
    };
  },
  methods: {
    ...mapActions(["createUser", "flashError"]),
    pressRegister() {
      if (this.password !== this.confirmPassword) {
        this.flashError(
          "The entered passwords do not match. Please try again."
        );
      } else {
        const user = { username: this.username, password: this.password };
        this.createUser(user)
          .then(() => this.$router.push({ name: "jobs" }))
          .catch((err) => err);
      }
    },
  },
};
</script>