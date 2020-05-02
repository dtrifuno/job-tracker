<template>
  <main>
    <header class="page-header page-header-dark">
      <div class="page-header-content mb-n5">
        <div class="container">
          <div class="row justify-content-cent align-items-center">
            <div class="col-lg-7">
              <h1 class="page-header-title">
                Organize your job search with
                <span>Job Tracker</span>
              </h1>
              <p>
                Creating customized job application materials and keeping track
                of the status of your applications has never been easier. Get
                started now.
              </p>
              <div class="pt-1 pb-3">
                <button class="btn btn-secondary">Register</button>
              </div>
              <small class="text-muted">
                Already a user?
                <router-link to="/login" class="text-white">Click here to login.</router-link>
              </small>
            </div>
            <div class="col-lg-5">
              <img class="img-fluid" src="@/assets/header.png" />
            </div>
          </div>
        </div>
      </div>
    </header>

    <section class="py-3">
      <div class="container py-4">
        <div class="row text-center">
          <div class="col-lg-4 mb-5 mb-lg-0">
            <h3>Create a Profile</h3>
            <p class="mb-0">
              Lorem ipsum, dolor sit amet consectetur adipisicing elit. Fugiat
              pariatur voluptatum reprehenderit a sed, commodi qui, nesciunt eos
              magnam repellendus sapiente necessitatibus voluptatibus quia
              tenetur laborum quibusdam? Accusantium, tempora sequi.
            </p>
          </div>
          <div class="col-lg-4 mb-5 mb-lg-0">
            <h3>Apply to Jobs</h3>
            <p class="mb-0">
              Lorem ipsum dolor sit amet consectetur adipisicing elit. Accusamus
              soluta laboriosam expedita sed ipsa, modi libero praesentium, unde
              quisquam quidem qui. Possimus optio eius debitis ea accusantium
              asperiores quaerat veritatis?
            </p>
          </div>
          <div class="col-lg-4 mb-5 mb-lg-0">
            <h3>Track Status</h3>
            <p class="mb-0">
              Lorem ipsum dolor sit amet consectetur adipisicing elit. Aliquam
              voluptate laudantium quia quas omnis, ullam eum consectetur vero
              dicta similique magni reprehenderit molestias amet veniam
              molestiae dolorum fugit tempora enim.
            </p>
          </div>
        </div>
      </div>
    </section>
  </main>
</template>

<script>
export default {
  name: "Landing"
};
</script>

<style scoped>
.page-header {
  position: relative;
  padding-top: 8rem;
  padding-bottom: 10rem;
}

.page-header-dark {
  color: #fff;
  background-color: #1a1a1a;
}
.text-white {
  color: #fff;
}
.page-header-title {
  font-size: 2.5rem;
  color: #fff;
}
</style>
