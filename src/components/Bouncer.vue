<template>
  <div />
</template>

<script>
import { mapActions } from "vuex";

export default {
  name: "Bouncer",
  methods: {
    ...mapActions(["loadUser"])
  },
  created() {
    this.loadUser().then(() =>
      this.$router.push({
        name: "jobs"
      })
    );
  }
};
</script>