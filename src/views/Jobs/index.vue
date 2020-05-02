<template>
  <div class="container">
    <h2 class="mt-4 mb-2">Job Applications</h2>
    <div class="input-group mb-1">
      <label for="searchTableOnly" class="sr-only">Search</label>
      <input
        type="text"
        class="form-control"
        id="searchTableInput"
        v-model="searchString"
        v-on:keyup="onSearchStringChange"
        placeholder="Search table..."
      />
      <div class="input-group-append">
        <button class="btn btn-primary btn-sm" @click="showAddJobModal">Add Job</button>
      </div>
    </div>
    <table class="table table-hover table-striped table-sm table-responsive-md">
      <thead class="thead-dark">
        <tr>
          <th scope="col">Company</th>
          <th scope="col">Position</th>
          <th scope="col">Location</th>
          <th scope="col">Status</th>
          <th scope="col">Updated</th>
          <th scope="col">Created</th>
          <th scope="col"></th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="job in filteredJobs" v-bind:key="job.id">
          <td>{{ job.company }}</td>
          <td>{{ job.position }}</td>
          <td>{{ job.location }}</td>
          <td>{{ job.status }}</td>
          <td>{{ job.date_updated }}</td>
          <td>{{ job.date_created }}</td>
          <td>
            <button
              type="button"
              class="btn btn-sm btn-outline-danger"
              @click="showDeleteModal(job.id)"
            >
              <i class="fas fa-trash-alt" aria-hidden="true" />
            </button>
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script>
import { mapActions, mapGetters, mapMutations } from "vuex";

export default {
  name: "Jobs",
  components: {},
  data() {
    return {
      searchString: ""
    };
  },
  computed: {
    ...mapGetters(["filteredJobs"])
  },
  methods: {
    ...mapActions(["fetchJobs", "deleteJob"]),
    ...mapMutations(["updateJobSearchString"]),
    showAddJobModal() {
      this.$modal.show("AddJobModal");
    },
    onSearchStringChange() {
      this.updateJobSearchString(this.searchString);
    },
    showDeleteModal(id) {
      this.$modal.show("DeleteModal", {
        title: "Delete Job Application",
        deleteAction: () => this.deleteJob(id)
      });
    }
  },
  created() {
    this.fetchJobs();
  }
};
</script>

<style scoped>
thead tr {
  font-weight: bold;
}
.thead .tr {
  color: #fff;
  background-color: #1a1a1a;
  border-color: #1a1a1a;
}

.table > tbody > tr > td {
  vertical-align: middle;
  cursor: pointer;
}
</style>
