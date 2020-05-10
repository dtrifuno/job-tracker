<template>
  <modal name="AddEditPersonalProjectModal" @before-open="beforeOpen" v-bind="modalProps">
    <div class="modal-content">
      <div class="modal-header">
        <h5 class="modal-title">{{isUpdate ? "Edit" : "Add"}} Personal Project</h5>
        <button type="button" class="close" aria-label="Close" @click="closeModal">
          <span aria-hidden="true">×</span>
        </button>
      </div>
      <div class="modal-body">
        <div class="container">
          <form novalidate>
            <div class="form-group row">
              <label for="projectNameInput" class="col-form-label col-lg-3">Project Name</label>
              <div class="col-lg-9">
                <input type="text" v-model="projectName" class="form-control" id="projectNameInput" />
              </div>
            </div>
            <div class="form-group row">
              <label for="urlInput" class="col-form-label col-lg-3">URL</label>
              <div class="col-lg-9">
                <input type="url" v-model="url" class="form-control" id="urlInput" />
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
                @click.prevent="isUpdate ? onClickEdit() : onClickSubmit()"
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
  name: "AddEditPersonalProjectModal",
  data() {
    return {
      projectName: "",
      url: "",
      description: "",
      id: null,
      isUpdate: false,
      modalProps
    };
  },
  methods: {
    ...mapActions([
      "createPersonalProject",
      "editPersonalProject",
      "flashSuccess"
    ]),
    extractDataToObject() {
      const data = {
        projectName: this.projectName,
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
      const clearData = {
        projectName: "",
        url: "",
        description: ""
      };
      this.setDataFromObject(clearData);
    },
    beforeOpen(event) {
      if (event.params && event.params.personalProject) {
        this.setDataFromObject(event.params.personalProject);
        this.id = event.params.personalProject.id;
        this.isUpdate = true;
      } else {
        this.clearFields();
        this.id = null;
        this.isUpdate = false;
      }
    },
    async onClickSubmit() {
      this.createPersonalProject({
        personalProjectData: this.extractDataToObject()
      })
        .then(() => {
          this.closeModal();
          this.flashSuccess("Personal project sucessfully added.");
        })
        .catch(err => err);
    },
    async onClickEdit() {
      this.editPersonalProject({
        id: this.id,
        personalProjectData: this.extractDataToObject()
      }).then(this.closeModal);
    },
    closeModal() {
      this.$modal.hide("AddEditPersonalProjectModal");
    }
  }
};
</script>
