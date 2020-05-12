<template>
  <div class="card item my-2" @click="onClick">
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
        <li v-for="(bullet, idx) in bullets" v-bind:key="idx">{{ bullet }}</li>
      </ul>
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
    onClick: Function
  }
};
</script>

<style scoped>
.item {
  cursor: pointer;
  transition: color 0.15s ease-in-out, background-color 0.15s ease-in-out, border-color 0.15s ease-in-out, box-shadow 0.15s ease-in-out, -webkit-box-shadow 0.15s ease-in-out;
}

.item:hover {
  background-color: #ececec;
}
</style>