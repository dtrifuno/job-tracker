<template>
  <div>
    <Bouncer bounceTo="login" />
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
      <Spinner v-if="isLoading" />
      <table v-else class="table table-hover table-striped table-sm table-responsive-md">
        <thead class="thead-dark">
          <tr>
            <TableHeading title="Company" category="company" />
            <TableHeading title="Position" category="position" />
            <TableHeading title="Location" category="location" />
            <TableHeading title="status" category="status" />
            <TableHeading title="Updated" category="dateUpdated" />
            <TableHeading title="Created" category="dateCreated" />
            <th style="width: 5%" scope="col"></th>
          </tr>
        </thead>
        <tbody>
          <tr
            v-for="job in sortedAndFilteredJobs"
            v-bind:key="job.id"
            @click="$router.push({ name:'job-details', params: job })"
          >
            <td>{{ job.company }}</td>
            <td>{{ job.position }}</td>
            <td>{{ job.location }}</td>
            <td>{{ statusCodeToMsg(job.status) }}</td>
            <td>{{ toLocaleDateString(job.dateUpdated) }}</td>
            <td>{{ toLocaleDateString(job.dateCreated) }}</td>
            <td>
              <button
                type="button"
                class="btn btn-sm btn-outline-primary"
                @click.stop="() => showDeleteModal(job)"
                aria-label="Delete Job"
              >
                <i class="fas fa-trash-alt" aria-hidden="true" />
              </button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script>
import { mapActions, mapGetters, mapMutations, mapState } from "vuex";
import { statusCodeToMsg, toLocaleDateString, debounce } from "@/utils";

import Bouncer from "@/components/Bouncer";
import Spinner from "@/components/Spinner";
import TableHeading from "./TableHeading";

export default {
  name: "Jobs",
  components: { Bouncer, Spinner, TableHeading },
  data() {
    return {
      searchString: ""
    };
  },
  computed: {
    ...mapGetters(["sortedAndFilteredJobs"]),
    ...mapState({ isLoading: state => state.spinners.isLoadingJobs })
  },
  watch: {
    searchString: function(newVal) {
      this.setLoadingJobs(true);
      debounce(function(newVal) {
        this.updateJobSearchString(newVal);
        this.setLoadingJobs(false);
      }, 300).bind(this, newVal)();
    }
  },
  methods: {
    statusCodeToMsg,
    toLocaleDateString,
    ...mapActions(["fetchJobs", "deleteJob"]),
    ...mapMutations(["updateJobSearchString", "setLoadingJobs"]),
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
    this.fetchJobs().catch(err => err);
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
