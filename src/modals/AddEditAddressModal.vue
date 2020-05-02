<template>
  <modal name="AddEditAddressModal" v-bind="modalProps">
    <div class="modal-content">
      <div class="modal-header">
        <h5 class="modal-title">Add Address</h5>
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
              <label for="positionInput" class="col-form-label col-lg-3"
                >Address Line 1</label
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
                >Address Line 2</label
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
                >Address Line 3</label
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
            <div class="row">
              <button type="submit" class="btn btn-primary ml-auto my-0">
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
  name: "AddEditAddressModal",
  data() {
    return {
      position: "",
      company: "",
      location: "",
      url: "",
      description: "",
      modalProps,
    };
  },
  methods: {
    closeModal() {
      this.$modal.hide("AddEditAddressModal");
    },
  },
};
</script>
