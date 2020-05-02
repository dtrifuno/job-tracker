<template>
  <div>
    <div class="col-md-6 m-auto">
      <div class="card card-body mt-5">
        <h2 class="text-center">Login</h2>
        <form @submit.prevent="null">
          <div class="form-group">
            <label for="emailInput">Email</label>
            <input
              type="text"
              class="form-control"
              v-model="email"
              id="emailInput"
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
            <button type="submit" class="btn btn-primary">Login</button>
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
export default {
  name: "Login",
  data() {
    return {
      email: "",
      password: "",
    };
  },
};
</script>

<style></style>
