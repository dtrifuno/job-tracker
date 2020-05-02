<template>
  <modal name="AddEditEducationModal" v-bind="modalProps">
    <div class="modal-content">
      <div class="modal-header">
        <h5 class="modal-title">Add Education</h5>
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
        <form>
          <div class="container">
            <div class="form-group row">
              <label for="schoolInput" class="col-form-label col-lg-4"
                >School</label
              >
              <div class="col-lg-8">
                <input
                  type="text"
                  v-model="school"
                  class="form-control"
                  id="schoolInput"
                />
              </div>
            </div>
            <div class="form-group row">
              <label for="locationInput" class="col-form-label col-lg-4"
                >Location</label
              >
              <div class="col-lg-8">
                <input
                  type="text"
                  v-model="location"
                  class="form-control"
                  id="locationInput"
                />
              </div>
            </div>
            <div class="form-group row">
              <label for="degreeAndFieldInput" class="col-form-label col-lg-4"
                >Degree / Field of Study
              </label>
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
              <label for="gpaInput" class="col-form-label col-lg-4">
                GPA
              </label>
              <div class="col-lg-8">
                <input
                  type="text"
                  v-model="gpa"
                  class="form-control"
                  id="gpaInput"
                />
              </div>
            </div>
            <div class="form-group row">
              <label for="dateFromToInput" class="col-form-label col-lg-4"
                >Date From / To</label
              >
              <div class="col-lg-8">
                <input
                  type="text"
                  v-model="dateFromTo"
                  class="form-control"
                  id="dateFromToInput"
                />
              </div>
            </div>
            <div class="form-group row">
              <label for="descriptionInput">Description </label>
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
          </div>
        </form>
      </div>
    </div>
  </modal>
</template>

<script>
import modalProps from "./modalProps";

export default {
  name: "AddEditEducationModal",
  data() {
    return {
      school: "",
      location: "",
      degreeAndField: "",
      gpa: "",
      dateFromTo: "",
      description: "",
      modalProps,
    };
  },
  methods: {
    closeModal() {
      this.$modal.hide("AddEditEducationModal");
    },
  },
};
</script>
