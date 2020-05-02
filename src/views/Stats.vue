<template>
  <div>
    <modal name="hello-world"> hello, world! </modal>
    <div class="container">
      <div class="row">
        <h2 class="mt-4 mb-3">Stats</h2>
        <button @click="showModal"></button>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  methods: {
    showModal() {
      this.$modal.show("hello-world");
    },
  },
};
</script>

<style></style>
