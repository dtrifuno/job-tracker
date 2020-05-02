<template>
  <modal name="AddEditPersonalProjectModal" v-bind="modalProps">
    <div class="modal-content">
      <div class="modal-header">
        <h5 class="modal-title">Add Personal Project</h5>
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
              <label for="projectNameInput" class="col-form-label col-lg-3"
                >Project Name</label
              >
              <div class="col-lg-9">
                <input
                  type="text"
                  v-model="projectName"
                  class="form-control"
                  id="projectNameInput"
                />
              </div>
            </div>
            <div class="form-group row">
              <label for="urlInput" class="col-form-label col-lg-3">URL</label>
              <div class="col-lg-9">
                <input
                  type="url"
                  v-model="url"
                  class="form-control"
                  id="urlInput"
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
  name: "AddEditPersonalProjectModal",
  data() {
    return {
      projectName: "",
      url: "",
      location: "",
      description: "",
      modalProps,
    };
  },
  methods: {
    closeModal() {
      this.$modal.hide("AddEditPersonalProjectModal");
    },
  },
};
</script>
