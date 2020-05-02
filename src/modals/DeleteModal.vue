<template>
  <modal name="DeleteModal" @before-open="beforeOpen" v-bind="modalProps">
    <div class="modal-content">
      <div class="modal-header">
        <h5 class="modal-title">{{ title }}</h5>
        <button type="button" class="close" aria-label="Close" @click="closeModal">
          <span aria-hidden="true">×</span>
        </button>
      </div>
      <div class="modal-body">
        <div class="container">
          <div>
            <p>Lorem ipsum dolor sit amet consectetur adipisicing elit. Amet eos exercitationem obcaecati repellat, ut voluptas eum impedit quae quos ex dolorum, autem velit dignissimos perspiciatis magni doloremque est magnam nobis!</p>
          </div>
          <div class="float-right">
            <button type="submit" class="btn btn-primary mx-1" @click="onDelete">Yes</button>
            <button type="submit" class="btn btn-secondary mx-1" @click="closeModal">No</button>
          </div>
        </div>
      </div>
    </div>
  </modal>
</template>

<script>
import modalProps from "./modalProps";

export default {
  name: "DeleteModal",
  data() {
    return {
      title: "Delete",
      deleteAction: null,
      modalProps
    };
  },
  methods: {
    beforeOpen(event) {
      this.title = event.params.title || this.title;
      this.deleteAction = event.params.deleteAction;
    },
    onDelete() {
      this.deleteAction();
      this.closeModal();
    },
    closeModal() {
      this.$modal.hide("DeleteModal");
    }
  }
};
</script>
