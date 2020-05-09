<template>
  <div class="card my-2">
    <div class="card-body mx-2">
      <div>
        <h5 class="mb-0 float-left">{{ heading }}</h5>
        <h6 class="mb-0 float-right">{{headingRight}}</h6>
        <br />
      </div>
      <div v-if="subheading || subheadingRight">
        <span class="float-left font-weight-bold">{{ subheading }}</span>
        <span class="float-right font-italic">{{ subheadingRight }}</span>
        <br />
      </div>
      <ul class="mb-0 pl-4" v-if="bullets">
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