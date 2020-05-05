<template>
  <modal name="AddEditWorkExperienceModal" @before-open="beforeOpen" v-bind="modalProps">
    <div class="modal-content">
      <div class="modal-header">
        <h5 class="modal-title">{{isUpdate ? "Edit" : "Add"}} Work Experience</h5>
        <button type="button" class="close" aria-label="Close" @click="closeModal">
          <span aria-hidden="true">×</span>
        </button>
      </div>
      <div class="modal-body">
        <div class="container">
          <form>
            <div class="form-group row">
              <label for="positionInput" class="col-form-label col-lg-3">Position</label>
              <div class="col-lg-9">
                <input type="text" v-model="position" class="form-control" id="positionInput" />
              </div>
            </div>
            <div class="form-group row">
              <label for="companyNameInput" class="col-form-label col-lg-3">Company</label>
              <div class="col-lg-9">
                <input type="text" v-model="company" class="form-control" id="companyNameInput" />
              </div>
            </div>
            <div class="form-group row">
              <label for="locationNameInput" class="col-form-label col-lg-3">Location</label>
              <div class="col-lg-9">
                <input type="text" v-model="location" class="form-control" id="locationInput" />
              </div>
            </div>
            <div class="form-group row">
              <label for="dateFromInput" class="col-form-label col-lg-3">Start Date</label>
              <div class="col-lg-9">
                <input type="month" v-model="dateFrom" class="form-control" id="dateFromInput" />
              </div>
            </div>
            <div class="form-group row">
              <label for="dateToInput" class="col-form-label col-lg-3">End Date</label>
              <div class="col-lg-9">
                <input type="month" v-model="dateTo" class="form-control" id="dateToInput" />
                <small class="form-text text-muted">Leave blank if you are still working here.</small>
              </div>
            </div>
            <div class="form-group row">
              <label for="descriptionInput">Description</label>
              <textarea id="descriptionInput" v-model="description" rows="5" class="form-control"></textarea>
              <small class="form-text text-muted">Use line breaks to create bullet points.</small>
            </div>
            <div class="row">
              <button
                type="submit"
                class="btn btn-primary ml-auto"
                @click="isUpdate ? onClickEdit() : onClickSubmit()"
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
  name: "AddEditWorkExperienceModal",
  data() {
    return {
      position: "",
      company: "",
      location: "",
      dateFrom: "",
      dateTo: "",
      description: "",
      id: null,
      isUpdate: false,
      modalProps
    };
  },
  methods: {
    ...mapActions(["createWorkExperience", "editWorkExperience"]),
    beforeOpen(event) {
      if (event.params && event.params.workExperience) {
        [
          "position",
          "company",
          "location",
          "dateFrom",
          "dateTo",
          "description"
        ].forEach(field => (this[field] = event.params.workExperience[field]));
        this.id = event.params.workExperience.id;
        this.isUpdate = true;
      } else {
        [
          "position",
          "company",
          "location",
          "dateFrom",
          "dateTo",
          "description"
        ].forEach(field => (this[field] = ""));
        this.isUpdate = false;
        this.id = null;
      }
    },
    async onClickSubmit() {
      const workExperience = {
        position: this.position,
        company: this.company,
        location: this.location,
        dateFrom: this.dateFrom,
        dateTo: this.dateTo,
        description: this.description
      };
      await this.createWorkExperience(workExperience);
    },
    async onClickEdit() {
      const workExperience = {
        id: this.id,
        position: this.position,
        company: this.company,
        location: this.location,
        dateFrom: this.dateFrom,
        dateTo: this.dateTo,
        description: this.description
      };
      await this.editWorkExperience(workExperience);
    },
    closeModal() {
      this.$modal.hide("AddEditWorkExperienceModal");
    }
  }
};
</script>
