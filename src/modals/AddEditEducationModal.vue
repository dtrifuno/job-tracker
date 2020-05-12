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
              <div class="ml-auto">
                <button
                  type="submit"
                  class="btn btn-primary mx-3"
                  @click.prevent="isUpdate ? onClickEdit() : onClickSubmit()"
                  :disabled="isLoading"
                >Submit</button>
                <button
                  class="btn btn-primary"
                  v-if="isUpdate"
                  @click.prevent="onClickDelete"
                  :disabled="isLoading"
                >Delete</button>
              </div>
            </div>
          </div>
        </form>
      </div>
    </div>
  </modal>
</template>

<script>
import { mapActions, mapMutations, mapState } from "vuex";

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
  computed: {
    ...mapState({
      isLoading: state => state.spinners.profile.isLoadingEducation
    })
  },
  methods: {
    ...mapActions([
      "createEducationExperience",
      "editEducationExperience",
      "deleteEducationExperience",
      "flashSuccess"
    ]),
    ...mapMutations(["toggleLoadingEducation"]),
    extractDataToObject() {
      const data = {
        school: this.school,
        location: this.location,
        degreeAndField: this.degreeAndField,
        gpa: this.gpa,
        dateFrom: this.dateFrom,
        dateTo: this.dateTo,
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
      const clearData = {
        school: "",
        location: "",
        degreeAndField: "",
        gpa: "",
        dateFrom: "",
        dateTo: "",
        description: ""
      };
      this.setDataFromObject(clearData);
    },
    beforeOpen(event) {
      if (event.params && event.params.educationExperience) {
        this.setDataFromObject(event.params.educationExperience);
        this.id = event.params.educationExperience.id;
        this.isUpdate = true;
      } else {
        this.clearFields();
        this.id = null;
        this.isUpdate = false;
      }
    },
    onClickSubmit() {
      this.toggleLoadingEducation();
      this.createEducationExperience({
        educationExperienceData: this.extractDataToObject()
      })
        .then(() => {
          this.closeModal();
          this.flashSuccess("Educational experience sucessfully added.");
        })
        .catch(err => err)
        .finally(this.toggleLoadingEducation);
    },
    onClickEdit() {
      this.toggleLoadingEducation();
      this.editEducationExperience({
        id: this.id,
        educationExperienceData: this.extractDataToObject()
      })
        .then(() => {
          this.closeModal();
          this.flashSuccess("Changes successfully saved.");
        })
        .catch(err => err)
        .finally(this.toggleLoadingEducation);
    },
    onClickDelete() {
      this.toggleLoadingEducation();
      this.deleteEducationExperience(this.id)
        .then(() => {
          this.closeModal();
          this.flashSuccess("Educational experience successfully deleted.");
        })
        .catch(err => err)
        .finally(this.toggleLoadingEducation);
    },
    closeModal() {
      this.$modal.hide("AddEditEducationModal");
    }
  }
};
</script>
