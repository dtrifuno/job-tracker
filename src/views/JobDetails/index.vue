<template>
  <div class="container">
    <div class="row">
      <h2 class="mt-4 mb-3">Profile</h2>
    </div>
    <div class="card row">
      <div class="card-header">
        <h4 class="mb-0">Job Details</h4>
      </div>
      <div class="card-body">
        <form novalidate>
          <div class="form-group">
            <label for="companyInput">Company</label>
            <input type="text" class="form-control" id="companyInput" v-model="company" />
          </div>
          <div class="form-group">
            <label for="positionInput">Position</label>
            <input type="text" class="form-control" id="positionInput" v-model="position" />
          </div>
          <div class="form-group">
            <label for="locationInput">Location</label>
            <input type="text" class="form-control" id="locationInput" v-model="location" />
          </div>
          <div class="form-group">
            <label for="urlInput">URL</label>
            <input type="url" class="form-control" id="urlInput" v-model="url" />
          </div>
          <button type="submit" class="btn btn-primary">Update</button>
        </form>
      </div>
    </div>

    <div class="card row">
      <div class="card-header">
        <h4 class="mb-0">Timeline</h4>
      </div>
      <div class="card-body">
        <button class="btn btn-primary" @click="showAddEventModal">Add Event</button>
      </div>
    </div>

    <div class="card row">
      <div class="card-header">
        <h4 class="mb-0">Job Description</h4>
      </div>
      <div class="card-body">
        <div class="form-group" v-if="editDescription">
          <textarea class="form-control" rows="20" v-model="description" />
          <small class="form-text text-muted">Use Markdown.</small>
        </div>
        <VueShowdown :markdown="description" v-if="!editDescription" />
        <div class="form-group">
          <button
            class="btn btn-primary"
            @click="editDescription = !editDescription"
          >{{ editDescription ? "Save" : "Edit" }}</button>
        </div>
      </div>
    </div>

    <!-- Refactor into a separate component. -->
    <div class="card row">
      <div class="card-header">
        <h4 class="mb-0">Customized CV</h4>
      </div>
      <div class="card-body"></div>
    </div>

    <div class="card row">
      <div class="card-header">
        <h4 class="mb-0">Cover Letter</h4>
      </div>
      <div class="card-body">
        <div class="form-group" v-if="editCoverLetter">
          <textarea class="form-control" rows="20" v-model="coverLetter" />
          <small class="form-text text-muted">Use Markdown.</small>
        </div>
        <VueShowdown :markdown="coverLetter" v-if="!editCoverLetter" />
        <div class="form-group">
          <button
            class="btn btn-primary"
            @click="editCoverLetter = !editCoverLetter"
          >{{ editCoverLetter ? "Save" : "Edit" }}</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { VueShowdown } from "vue-showdown";

import {mapActions} from "vuex";

export default {
  name: "JobDetails",
  components: { VueShowdown },
  data() {
    return {
      id: null,
      company: "",
      position: "",
      location: "",
      url: "",
      description: "",
      editDescription: false,
      coverLetter: "",
      editCoverLetter: false
    };
  },
  methods: {
    ...mapActions(["getJob"]),
    extractDataToObject() {
      const data = {
        company: this.company,
        position: this.position,
        location: this.location,
        url: this.url,
        description: this.description,
        coverLetter: this.coverLetter,
      };
      return data;
    },
    setDataFromObject(data) {
      for (const [field, value] of Object.entries(data)) {
        this[field] = value;
      }
    },
    clearFields() {
      const clearData = {
        company: "",
        position: "",
        location: "",
        url: "",
        description: "",
        coverLetter: "",
      };
      this.setDataFromObject(clearData);
    },
    showAddEventModal() {
      this.$modal.show("AddEditEventModal");
    }
  },
  created() {
    this.clearFields();
    this.id = this.$route.params.id;
    this.getJob(this.id)
  }
};
</script>

<style scoped>
.card {
  margin-bottom: 0.5rem;
}

h2,
.card-header {
  user-select: none;
}
</style>
