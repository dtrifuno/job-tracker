<template>
  <div class="card-header py-2">
    <h4 class="float-left my-1">{{ title }}</h4>
    <div class="float-right">
      <button class="btn btn-outline-primary btn-sm" @click="onClick" :disabled="buttonDisabled">
        <i class="fas fa-plus" v-if="!buttonText" />
        {{ buttonText ? buttonText : "" }}
      </button>
    </div>
  </div>
</template>

<script>
export default {
  name: "CardTitle",
  props: {
    title: String,
    buttonText: {
      type: String,
      default: null
    },
    onClick: Function,
    buttonDisabled: {
      type: Boolean,
      default: false
    }
  }
};
</script>

<style>
</style>