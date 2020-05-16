<template>
  <div />
</template>

<script>
import { mapState } from "vuex";

export default {
  name: "Bouncer",
  props: {
    bounceAuthorized: {
      type: Boolean,
      default: false
    },
    bounceTo: {
      type: String,
      default: "login"
    }
  },
  computed: {
    ...mapState({
      isAuthenticated: state => state.auth.isAuthenticated
    })
  },
  created() {
    if (this.isAuthenticated === this.bounceAuthorized) {
      this.$router.push({
        name: this.bounceTo
      });
    }
  },
  watch: {
    isAuthenticated: function(val) {
      if (val === this.bounceAuthorized) {
        this.$router.push({
          name: this.bounceTo
        });
      }
    }
  }
};
</script>