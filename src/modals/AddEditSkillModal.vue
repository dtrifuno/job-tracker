<template>
  <modal name="AddEditSkillModal" @before-open="beforeOpen" v-bind="modalProps">
    <div class="modal-content">
      <div class="modal-header">
        <h5 class="modal-title">{{isUpdate ? "Edit" : "Add"}} Skill</h5>
        <button type="button" class="close" aria-label="Close" @click="closeModal">
          <span aria-hidden="true">×</span>
        </button>
      </div>
      <div class="card-body">
        <div class="container">
          <form>
            <div class="form-group row">
              <label for="categoryInput" class="col-form-label col-lg-2">Category</label>
              <div class="col-lg-10">
                <input type="text" v-model="category" class="form-control" id="categoryInput" />
              </div>
            </div>
            <div class="form-group row">
              <label for="skillInput" class="col-form-label col-lg-2">Skill</label>
              <div class="col-lg-10">
                <input type="text" v-model="skill" class="form-control" id="skillInput" />
              </div>
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
                  v-if="isUpdate"
                  class="btn btn-primary"
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
import { mapActions, mapState } from "vuex";

import modalProps from "./modalProps";

export default {
  name: "AddEditSkillModal",
  data() {
    return {
      category: "",
      skill: "",
      id: null,
      isUpdate: false,
      modalProps
    };
  },
  computed: {
    ...mapState({
      isLoading: state => state.spinners.profile.isLoadingSkills
    })
  },
  methods: {
    ...mapActions(["createSkill", "editSkill", "deleteSkill", "flashSuccess"]),
    extractDataToObject() {
      const data = {
        category: this.category,
        skill: this.skill
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
        category: "",
        skill: ""
      };
      this.setDataFromObject(clearData);
    },
    beforeOpen(event) {
      if (event.params && event.params.skill) {
        this.setDataFromObject(event.params.skill);
        this.id = event.params.skill.id;
        this.isUpdate = true;
      } else {
        this.clearFields();
        this.id = null;
        this.isUpdate = false;
      }
    },
    onClickSubmit() {
      this.createSkill({
        skillData: this.extractDataToObject()
      })
        .then(() => {
          this.closeModal();
          this.flashSuccess("Skill successfully added.");
        })
        .catch(err => err)
    },
    onClickEdit() {
      this.editSkill({
        id: this.id,
        skillData: this.extractDataToObject()
      })
        .then(() => {
          this.closeModal();
          this.flashSuccess("Changes successfully saved.");
        })
        .catch(err => err)
    },
    onClickDelete() {
      this.deleteSkill(this.id)
        .then(() => {
          this.closeModal();
          this.flashSuccess("Skill successfully deleted.");
        })
        .catch(err => err)
    },
    closeModal() {
      this.$modal.hide("AddEditSkillModal");
    }
  }
};
</script>
