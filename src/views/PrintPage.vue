<template>
  <div>
    <Bouncer bounceTo="login" />
    <div class="container pt-3 d-print-none">
      <div class="row">
        <div class="ml-auto">
          <button class="btn btn-sm btn-primary mx-3" @click="onClickBack">Back</button>
          <button class="btn btn-sm btn-primary" @click="onClickPrint">Print</button>
        </div>
      </div>
    </div>
    <div class="cv-container">
      <div v-html="html" />
    </div>
  </div>
</template>

<script>
import Bouncer from "@/components/Bouncer";

export default {
  name: "PrintPage",
  components: { Bouncer },
  data() {
    return {
      html: "",
      id: null,
    };
  },
  created() {
    this.id = this.$route.params.id;
    this.html = this.$route.params.html;
  },
  methods: {
    onClickBack() {
      this.$router.push({name: "job-details", params: { id: this.id }});
    },
    onClickPrint() {
      window.print();
    }
  }
};
</script>