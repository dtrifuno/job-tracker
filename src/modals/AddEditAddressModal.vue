<template>
  <modal name="AddEditAddressModal" @before-open="beforeOpen" v-bind="modalProps">
    <div class="modal-content">
      <div class="modal-header">
        <h5 class="modal-title">{{isUpdate ? "Edit" : "Add"}} Address</h5>
        <button type="button" class="close" aria-label="Close" @click="closeModal">
          <span aria-hidden="true">×</span>
        </button>
      </div>
      <div class="modal-body">
        <form>
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
              <button
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
    ...mapActions(["createAddress", "editAddress"]),
    beforeOpen(event) {
      if (event.params && event.params.address) {
        ["lineOne", "lineTwo", "lineThree"].forEach(
          field => (this[field] = event.params.address[field])
        );
        this.id = event.params.address.id;
        this.isUpdate = true;
      } else {
        ["lineOne", "lineTwo", "lineThree"].forEach(
          field => (this[field] = "")
        );
        this.id = null;
        this.isUpdate = false;
      }
    },
    async onClickSubmit() {
      const address = {
        lineOne: this.lineOne,
        lineTwo: this.lineTwo,
        lineThree: this.lineThree
      };
      await this.createAddress(address);
    },
    async onClickEdit() {
      const address = {
        id: this.id,
        lineOne: this.lineOne,
        lineTwo: this.lineTwo,
        lineThree: this.lineThree
      };
      await this.editAddress(address);
    },
    closeModal() {
      this.$modal.hide("AddEditAddressModal");
    }
  }
};
</script>
