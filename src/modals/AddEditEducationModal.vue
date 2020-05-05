<template>
  <modal name="AddEditEducationModal" @before-open="beforeOpen" v-bind="modalProps">
    <div class="modal-content">
      <div class="modal-header">
        <h5 class="modal-title">{{isUpdate ? "Edit" : "Add"}} Education</h5>
        <button type="button" class="close" aria-label="Close" @click="closeModal">
          <span aria-hidden="true">×</span>
        </button>
      </div>
      <div class="modal-body">
        <form>
          <div class="container">
            <div class="form-group row">
              <label for="schoolInput" class="col-form-label col-lg-4">School</label>
              <div class="col-lg-8">
                <input type="text" v-model="school" class="form-control" id="schoolInput" />
              </div>
            </div>
            <div class="form-group row">
              <label for="locationInput" class="col-form-label col-lg-4">Location</label>
              <div class="col-lg-8">
                <input type="text" v-model="location" class="form-control" id="locationInput" />
              </div>
            </div>
            <div class="form-group row">
              <label
                for="degreeAndFieldInput"
                class="col-form-label col-lg-4"
              >Degree / Field of Study</label>
              <div class="col-lg-8">
                <input
                  type="text"
                  v-model="degreeAndField"
                  class="form-control"
                  id="degreeAndFieldInput"
                />
              </div>
            </div>
            <div class="form-group row">
              <label for="gpaInput" class="col-form-label col-lg-4">GPA</label>
              <div class="col-lg-8">
                <input type="text" v-model="gpa" class="form-control" id="gpaInput" />
              </div>
            </div>
            <div class="form-group row">
              <label for="dateFromInput" class="col-form-label col-lg-4">Start Date</label>
              <div class="col-lg-8">
                <input type="month" v-model="dateFrom" class="form-control" id="dateFromInput" />
              </div>
            </div>
            <div class="form-group row">
              <label for="dateToInput" class="col-form-label col-lg-4">End Date</label>
              <div class="col-lg-8">
                <input type="month" v-model="dateTo" class="form-control" id="dateToInput" />
                <small class="form-text text-muted">Leave blank if you are still studying here.</small>
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
          </div>
        </form>
      </div>
    </div>
  </modal>
</template>

<script>
import { mapActions } from "vuex";

import modalProps from "./modalProps";

export default {
  name: "AddEditEducationModal",
  data() {
    return {
      school: "",
      location: "",
      degreeAndField: "",
      gpa: "",
      dateFrom: "",
      dateTo: "",
      description: "",
      id: null,
      isUpdate: false,
      modalProps
    };
  },
  methods: {
    ...mapActions(["createEducationExperience", "editEducationExperience"]),
    beforeOpen(event) {
      if (event.params && event.params.educationExperience) {
        [
          "school",
          "location",
          "degreeAndField",
          "gpa",
          "dateFrom",
          "dateTo",
          "description"
        ].forEach(
          field => (this[field] = event.params.educationExperience[field])
        );
        this.id = event.params.educationExperience.id;
        this.isUpdate = true;
      } else {
        [
          "school",
          "location",
          "degreeAndField",
          "gpa",
          "dateFrom",
          "dateTo",
          "description"
        ].forEach(field => (this[field] = ""));
        this.isUpdate = false;
        this.id = null;
      }
    },
    async onClickSubmit() {
      const educationExperience = {
        school: this.school,
        location: this.location,
        degreeAndField: this.degreeAndField,
        gpa: this.gpa,
        dateFrom: this.dateFrom,
        dateTo: this.dateTo,
        description: this.description
      };
      await this.createEducationExperience(educationExperience);
    },
    async onClickEdit() {
      const educationExperience = {
        id: this.id,
        school: this.school,
        location: this.location,
        degreeAndField: this.degreeAndField,
        gpa: this.gpa,
        dateFrom: this.dateFrom,
        dateTo: this.dateTo,
        description: this.description
      };
      await this.editEducationExperience(educationExperience);
    },
    closeModal() {
      this.$modal.hide("AddEditEducationModal");
    }
  }
};
</script>
