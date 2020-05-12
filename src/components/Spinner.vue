<template>
  <div class="d-flex justify-content-center py-3">
    <div class="spinner-border" role="status" :style="styleObject">
      <span class="sr-only">Loading...</span>
    </div>
  </div>
</template>

<script>
export default {
  name: "Spinner",
  props: {
    size: {
      type: Number,
      default: 5
    }
  },
  data() {
    return {
      styleObject: {
        width: this.size + 'rem',
        height: this.size + 'rem',
      }
    };
  }
};
</script>

<style>
</style>