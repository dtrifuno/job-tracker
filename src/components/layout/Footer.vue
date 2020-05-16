<template>
  <footer class="footer font-small border-top mt-3">
    <div class="footer-copyright text-center pt-2 pb-0">
      © 2020 Copyright:
      <a href="https://trifunovski.me/">Darko Trifunovski</a>
    </div>
    <div class="text-center pb-1">
      source code:
      <a href="https://github.com/dtrifuno/job-tracker"
        >github.com/dtrifuno/job-tracker</a
      >
    </div>
  </footer>
</template>

<script>
export default {
  name: "Footer",
};
</script>

<style scoped>
.footer {
  position: absolute;
  bottom: 0;
  width: 100%;
  height: 60px;
}

@media print {
  footer {
    display: none;
  }
}
</style>
