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
          </form>
        </div>
      </div>
    </div>
  </modal>
</template>

<script>
import { mapActions, mapMutations, mapState } from "vuex";

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
  computed: {
    ...mapState({
      isLoading: state => state.spinners.profile.isLoadingWorkHistory
    }),
  },
  methods: {
    ...mapActions([
      "createWorkExperience",
      "editWorkExperience",
      "deleteWorkExperience",
      "flashSuccess"
    ]),
    ...mapMutations(["toggleLoadingWorkHistory"]),
    extractDataToObject() {
      const data = {
        position: this.position,
        company: this.company,
        location: this.location,
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
      const data = {
        position: "",
        company: "",
        location: "",
        dateFrom: "",
        dateTo: "",
        description: ""
      };
      this.setDataFromObject(data);
    },
    beforeOpen(event) {
      if (event.params && event.params.workExperience) {
        this.setDataFromObject(event.params.workExperience);
        this.id = event.params.workExperience.id;
        this.isUpdate = true;
      } else {
        this.clearFields();
        this.isUpdate = false;
        this.id = null;
      }
    },
    onClickSubmit() {
      this.toggleLoadingWorkHistory();
      this.createWorkExperience({
        workExperienceData: this.extractDataToObject()
      })
        .then(() => {
          this.closeModal();
          this.flashSuccess("Work experience sucessfully added.");
        })
        .catch(err => err)
        .finally(this.toggleLoadingWorkHistory);
    },
    onClickEdit() {
      this.toggleLoadingWorkHistory();
      this.editWorkExperience({
        id: this.id,
        workExperienceData: this.extractDataToObject()
      })
        .then(() => {
          this.closeModal();
          this.flashSuccess("Changes successfully saved.");
        })
        .catch(err => err)
        .finally(this.toggleLoadingWorkHistory);
    },
    onClickDelete() {
      this.toggleLoadingWorkHistory();
      this.deleteWorkExperience(this.id)
        .then(() => {
          this.closeModal();
          this.flashSuccess("Work experience successfully deleted.");
        })
        .catch(err => err)
        .finally(this.toggleLoadingWorkHistory);
    },
    closeModal() {
      this.$modal.hide("AddEditWorkExperienceModal");
    }
  }
};
</script>
