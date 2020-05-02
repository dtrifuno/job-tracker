<template>
  <modal name="AddEditSkillModal" v-bind="modalProps">
    <div class="modal-content">
      <div class="modal-header">
        <h5 class="modal-title">Add Skill</h5>
        <button
          type="button"
          class="close"
          aria-label="Close"
          @click="closeModal"
        >
          <span aria-hidden="true">×</span>
        </button>
      </div>
      <div class="card-body">
        <div class="container">
          <form>
            <div class="form-group row">
              <label for="categoryInput" class="col-form-label col-lg-2"
                >Category</label
              >
              <div class="col-lg-10">
                <input
                  type="text"
                  v-model="category"
                  class="form-control"
                  id="categoryInput"
                />
              </div>
            </div>
            <div class="form-group row">
              <label for="skillInput" class="col-form-label col-lg-2"
                >Skill</label
              >
              <div class="col-lg-10">
                <input
                  type="text"
                  v-model="skill"
                  class="form-control"
                  id="skillInput"
                />
              </div>
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
  name: "AddEditSkillModal",
  data() {
    return {
      category: "",
      skill: "",
      modalProps,
    };
  },
  methods: {
    closeModal() {
      this.$modal.hide("AddEditSkillModal");
    },
  },
};
</script>
