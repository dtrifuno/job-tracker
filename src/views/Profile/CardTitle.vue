<template>
  <div class="card-header py-2">
    <h4 class="float-left my-1">{{ title }}</h4>
    <div class="float-right">
      <button class="btn btn-outline-primary btn-sm" @click="onClick">
        <i class="fas fa-plus" />
      </button>
    </div>
  </div>
</template>

<script>
export default {
  name: "CardTitle",
  props: {
    title: String,
    onClick: Function
  }
};
</script>

<style>
</style>