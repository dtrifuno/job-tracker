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
        placeholder="Search table..."
      />
      <div class="input-group-append">
        <button class="btn btn-primary btn-sm" @click="showAddJobModal">Add Job</button>
      </div>
    </div>
    <Spinner v-if="isLoading"/>
    <table v-else class="table table-hover table-striped table-sm table-responsive-md">
      <thead class="thead-dark">
        <tr>
          <th scope="col">Company</th>
          <th scope="col">Position</th>
          <th scope="col">Location</th>
          <th scope="col">Status</th>
          <th scope="col">Updated</th>
          <th scope="col">Created</th>
          <th style="width: 5%" scope="col"></th>
        </tr>
      </thead>
      <tbody>
        <tr
          v-for="job in filteredJobs"
          v-bind:key="job.id"
          @click="$router.push({ name:'job-details', params: job })"
        >
          <td>{{ job.company }}</td>
          <td>{{ job.position }}</td>
          <td>{{ job.location }}</td>
          <td>{{ statusCodeToMsg(job.status) }}</td>
          <td>{{ new Date(job.dateUpdated).toLocaleDateString() }}</td>
          <td>{{ new Date(job.dateCreated).toLocaleDateString() }}</td>
          <td>
            <button
              type="button"
              class="btn btn-sm btn-outline-primary"
              @click.stop="() => showDeleteModal(job)"
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
import { mapActions, mapGetters, mapMutations, mapState } from "vuex";
import { statusCodeToMsg, debounce } from "@/utils";

import Spinner from "@/components/Spinner";

export default {
  name: "Jobs",
  components: { Spinner },
  data() {
    return {
      searchString: ""
    };
  },
  computed: {
    ...mapGetters(["filteredJobs"]),
    ...mapState({ isLoading: state => state.spinners.isLoadingJobs })
  },
  watch: {
    searchString: debounce(function(newVal) {
      this.updateJobSearchString(newVal);
    }, 500)
  },
  methods: {
    statusCodeToMsg,
    ...mapActions(["fetchJobs", "deleteJob"]),
    ...mapMutations(["updateJobSearchString", "toggleLoadingJobs"]),
    showAddJobModal() {
      this.$modal.show("AddJobModal");
    },
    showDeleteModal(job) {
      this.$modal.show("DeleteModal", {
        title: "Delete Job Application",
        target: ` your ${job.position} application at ${job.company} and all associated data`,
        deleteAction: () => this.deleteJob(job.id)
      });
    }
  },
  created() {
    this.toggleLoadingJobs();
    this.fetchJobs().finally(this.toggleLoadingJobs);
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
