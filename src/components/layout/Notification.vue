<template>
  <notifications position="top center" />
</template>

<script>
import { mapState } from "vuex";

export default {
  name: "Notification",
  computed: {
    ...mapState({
      notification: (state) => state.notifications.notification,
    }),
  },
  watch: {
    notification(currentNotification, prevNotification) {
      if (prevNotification !== currentNotification) {
        this.$notify({
          text: currentNotification.msg,
          type: currentNotification.type,
        });
      }
    },
  },
};
</script>

<style></style>
