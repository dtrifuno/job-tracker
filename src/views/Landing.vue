<template>
  <main>
    <Bouncer bounceAuthorized bounceTo="jobs" />
    <header class="page-header page-header-dark">
      <div class="page-header-content mb-n5">
        <div class="container">
          <div class="row justify-content-center align-items-center">
            <div class="col-lg-6">
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
                <button
                  class="btn btn-secondary"
                  @click="$router.push({ name: 'register' })"
                >Register</button>
              </div>
              <small class="text-muted">
                Already a user?
                <router-link to="/login" class="text-white">Click here to login.</router-link>
              </small>
            </div>
            <div class="col-lg-6">
              <div class="header-image">
                <img class="img-fluid" src="@/assets/header.png" />
              </div>
            </div>
          </div>
        </div>
      </div>
    </header>

    <section class="py-4">
      <div class="container py-4">
        <div class="row text-left">
          <div class="col-lg-4">
            <h4>Create a Profile</h4>
            <p class="mb-0">
              Fill out a detailed profile, listing your background, skills and accomplishments.
              Use the information stored in the profile to quickly create a resume tailored to any job opening.
            </p>
          </div>
          <div class="col-lg-4">
            <h4>Apply to Jobs</h4>
            <p class="mb-0">
              Keep track of job openings you are interested in by adding them to the Jobs section.
              Store information like job title, company, location and a detailed job description.
            </p>
          </div>
          <div class="col-lg-4">
            <h4>Track Status</h4>
            <p class="mb-0">
              Monitor the status of each of your applications.
              Organize your calendar by keeping track of scheduled interviews and assessment deadlines.
            </p>
          </div>
        </div>
      </div>
    </section>
  </main>
</template>

<script>
import Bouncer from "@/components/Bouncer";

export default {
  name: "Landing",
  components: {
    Bouncer
  }
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

.header-image {
  display: block;
  position: relative;
}

.header-image:before {
  display: block;
  content: "";
  position: absolute;
  width: 100%;
  height: 100%;
  box-shadow: inset 0px 0px 12px 10px #1a1a1a;
}
</style>
