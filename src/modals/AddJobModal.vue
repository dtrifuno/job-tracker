<template>
  <modal name="AddJobModal" @before-open="beforeOpen" v-bind="modalProps">
    <div class="modal-content">
      <div class="modal-header">
        <h5 class="modal-title">Add Job</h5>
        <button type="button" class="close" aria-label="Close" @click="closeModal">
          <span aria-hidden="true">×</span>
        </button>
      </div>
      <div class="modal-body">
        <div class="container">
          <form>
            <div class="form-group row">
              <label for="positionInput" class="col-form-label col-lg-2">Position</label>
              <div class="col-lg-10">
                <input type="text" v-model="position" class="form-control" id="positionInput" />
              </div>
            </div>
            <div class="form-group row">
              <label for="companyNameInput" class="col-form-label col-lg-2">Company</label>
              <div class="col-lg-10">
                <input type="text" v-model="company" class="form-control" id="companyNameInput" />
              </div>
            </div>
            <div class="form-group row">
              <label for="locationNameInput" class="col-form-label col-lg-2">Location</label>
              <div class="col-lg-10">
                <input type="text" v-model="location" class="form-control" id="locationInput" />
              </div>
            </div>
            <div class="form-group row">
              <label for="urlInput" class="col-form-label col-lg-2">URL</label>
              <div class="col-lg-10">
                <input type="url" v-model="url" class="form-control" id="urlInput" />
              </div>
            </div>
            <div class="form-group row">
              <label for="jobDescriptionInput">Job Description</label>
              <textarea
                id="jobDescriptionInput"
                v-model="description"
                rows="5"
                class="form-control"
              ></textarea>
              <small class="form-text text-muted">Use Markdown</small>
            </div>
            <div class="row">
              <button
                type="submit"
                class="btn btn-primary ml-auto"
                @click.prevent="onClickSubmit()"
              >Submit</button>
            </div>
          </form>
        </div>
      </div>
    </div>
  </modal>
</template>

<script>
import { mapActions } from "vuex";

import modalProps from "./modalProps";

export default {
  name: "AddJobModal",
  data() {
    return {
      position: "",
      company: "",
      location: "",
      url: "",
      description: "",
      modalProps
    };
  },
  methods: {
    ...mapActions(["createJob"]),
    extractDataToObject() {
      const data = {
        position: this.position,
        company: this.company,
        location: this.location,
        url: this.url,
        description: this.description
      };
      return data;
    },
    setDataFromObject(data) {
      for (const [field, value] of Object.entries(data)) {
        this[field] = value;
      }
    },
    clearFields() {
      const clearFields = {
        position: "",
        company: "",
        location: "",
        url: "",
        description: ""
      };
      this.setDataFromObject(clearFields);
    },
    beforeOpen() {
      this.clearFields();
    },
    onClickSubmit() {
      this.createJob({
        date: (new Date()).toISOString().split("T")[0],
        jobData: this.extractDataToObject()
      });
    },
    closeModal() {
      this.$modal.hide("AddJobModal");
    }
  }
};
</script>
