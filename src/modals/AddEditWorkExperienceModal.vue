<template>
  <modal name="AddEditWorkExperienceModal" v-bind="modalProps">
    <div class="modal-content">
      <div class="modal-header">
        <h5 class="modal-title">Add Work Experience</h5>
        <button
          type="button"
          class="close"
          aria-label="Close"
          @click="closeModal"
        >
          <span aria-hidden="true">×</span>
        </button>
      </div>
      <div class="modal-body">
        <div class="container">
          <form>
            <div class="form-group row">
              <label for="positionInput" class="col-form-label col-lg-3"
                >Position</label
              >
              <div class="col-lg-9">
                <input
                  type="text"
                  v-model="position"
                  class="form-control"
                  id="positionInput"
                />
              </div>
            </div>
            <div class="form-group row">
              <label for="companyNameInput" class="col-form-label col-lg-3"
                >Company</label
              >
              <div class="col-lg-9">
                <input
                  type="text"
                  v-model="company"
                  class="form-control"
                  id="companyNameInput"
                />
              </div>
            </div>
            <div class="form-group row">
              <label for="locationNameInput" class="col-form-label col-lg-3"
                >Location</label
              >
              <div class="col-lg-9">
                <input
                  type="text"
                  v-model="location"
                  class="form-control"
                  id="locationInput"
                />
              </div>
            </div>
            <div class="form-group row">
              <label for="datesFromToInput" class="col-form-label col-lg-3"
                >Dates From / To</label
              >
              <div class="col-lg-9">
                <input
                  type="text"
                  v-model="datesFromTo"
                  class="form-control"
                  id="datesFromToInput"
                />
              </div>
            </div>
            <div class="form-group row">
              <label for="descriptionInput">Description</label>
              <textarea
                id="descriptionInput"
                v-model="description"
                rows="5"
                class="form-control"
              ></textarea>
              <small class="form-text text-muted"
                >Use line breaks to create bullet points.</small
              >
            </div>
            <div class="row">
              <button type="submit" class="btn btn-primary ml-auto">
                Submit
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>
  </modal>
</template>

<script>
import modalProps from "./modalProps";

export default {
  name: "AddEditWorkExperienceModal",
  data() {
    return {
      position: "",
      company: "",
      location: "",
      datesFromTo: "",
      description: "",
      modalProps,
    };
  },
  methods: {
    closeModal() {
      this.$modal.hide("AddEditWorkExperienceModal");
    },
  },
};
</script>
