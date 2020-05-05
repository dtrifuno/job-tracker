<template>
  <div class="card my-1">
    <div class="card-body">
      <div>
        <h5 class="mb-0 float-left">{{ heading }}</h5>
        <span class="float-right">{{ headingRight }}</span>
        <br />
      </div>
      <div v-if="subheading || subheadingRight">
        <span class="float-left">{{ subheading }}</span>
        <span class="float-right">{{ subheadingRight }}</span>
        <br />
      </div>
      <ul v-if="bullets">
        <li v-for="(bullet, idx) in bullets" v-bind:key="idx">{{bullet}}</li>
      </ul>
      <div class="float-right">
        <button
          type="button"
          class="btn btn-outline-success btn-sm mx-1"
          v-if="onEdit"
          @click="onEdit"
        >
          <i class="fas fa-edit" aria-hidden="true" />
        </button>
        <button
          type="button"
          class="btn btn-outline-danger btn-sm"
          v-if="onDelete"
          @click="onDelete"
        >
          <i class="fas fa-trash-alt" aria-hidden="true" />
        </button>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "CVItem",
  props: {
    heading: String,
    headingRight: String,
    subheading: String,
    subheadingRight: String,
    bullets: Array,
    onDelete: Function,
    onEdit: Function
  }
};
</script>

<style>
</style>