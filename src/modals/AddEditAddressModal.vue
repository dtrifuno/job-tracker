<template>
  <modal name="AddEditAddressModal" @before-open="beforeOpen" v-bind="modalProps">
    <div class="modal-content">
      <div class="modal-header">
        <h5 class="modal-title">{{ isUpdate ? "Edit" : "Add" }} Address</h5>
        <button type="button" class="close" aria-label="Close" @click="closeModal">
          <span aria-hidden="true">×</span>
        </button>
      </div>
      <div class="modal-body">
        <form @submit.prevent="isUpdate ? onClickEdit() : onClickSubmit()">
          <div class="container">
            <div class="form-group row">
              <label for="lineOneInput" class="col-form-label col-lg-3">Address Line 1</label>
              <div class="col-lg-9">
                <input type="text" v-model="lineOne" class="form-control" id="lineOneInput" />
              </div>
            </div>
            <div class="form-group row">
              <label for="lineTwoInput" class="col-form-label col-lg-3">Address Line 2</label>
              <div class="col-lg-9">
                <input type="text" v-model="lineTwo" class="form-control" id="lineTwoInput" />
              </div>
            </div>
            <div class="form-group row">
              <label for="lineThreeInput" class="col-form-label col-lg-3">Address Line 3</label>
              <div class="col-lg-9">
                <input type="text" v-model="lineThree" class="form-control" id="lineThreeInput" />
              </div>
            </div>
            <div class="row">
              <button type="submit" class="btn btn-primary ml-auto">Submit</button>
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
  name: "AddEditAddressModal",
  data() {
    return {
      lineOne: "",
      lineTwo: "",
      lineThree: "",
      isUpdate: false,
      id: null,
      modalProps
    };
  },
  methods: {
    ...mapActions(["createAddress", "editAddress", "flashSuccess"]),
    extractDataToObject() {
      const data = {
        lineOne: this.lineOne,
        lineTwo: this.lineTwo,
        lineThree: this.lineThree
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
        lineOne: "",
        lineTwo: "",
        lineThree: ""
      };
      this.setDataFromObject(clearData);
    },
    beforeOpen(event) {
      if (event.params && event.params.address) {
        this.setDataFromObject(event.params.address);
        this.id = event.params.address.id;
        this.isUpdate = true;
      } else {
        this.clearFields();
        this.id = null;
        this.isUpdate = false;
      }
    },
    async onClickSubmit() {
      this.createAddress({ addressData: this.extractDataToObject() })
        .then(() => {
          this.closeModal();
          this.flashSuccess("Address sucessfully added.");
        })
        .catch(err => err);
    },
    onClickEdit() {
      this.editAddress({ id: this.id, addressData: this.extractDataToObject() })
        .then(this.closeModal)
        .catch(err => err);
    },
    closeModal() {
      this.$modal.hide("AddEditAddressModal");
    }
  }
};
</script>
