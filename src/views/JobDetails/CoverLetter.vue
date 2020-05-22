<template>
  <div class="card row">
    <div class="card-header py-2">
      <h4 class="float-left my-1">Cover Letter</h4>
      <div class="float-right">
        <button
          v-if="!isEdit"
          class="btn btn-outline-primary btn-sm mx-2"
          @click="$router.push({ name:'print-page', params: { id: jobId, html: coverLetterHtml } })"
          :disabled="isLoading"
        >Print</button>
        <button
          class="btn btn-outline-primary btn-sm"
          @click="toggleCoverLetter"
          :disabled="isLoading"
        >{{ isEdit ? "Save" : "Edit" }}</button>
      </div>
    </div>
    <div class="container">
      <Spinner v-if="isLoading" />
      <div class="p-2" v-else-if="!isEdit">
        <div v-html="coverLetterHtml" />
      </div>
      <div v-else class="p-2 py-3">
        <div class="form-group py-2">
          <fieldset class="border px-3 mb-3">
            <legend class="w-auto">Recipient</legend>
            <div class="form-group row">
              <label for="recipientNameInput" class="col-form-label col-sm-3">Name</label>
              <div class="col-sm-9">
                <input
                  type="text"
                  class="form-control"
                  name="recipientNameInput"
                  v-model="recipientName"
                />
              </div>
            </div>
            <div class="form-group row">
              <label for="addressLineOneInput" class="col-form-label col-sm-3">Address Line 1</label>
              <div class="col-sm-9">
                <input
                  type="text"
                  class="form-control"
                  name="addressLineOneInput"
                  v-model="lineOne"
                />
              </div>
            </div>
            <div class="form-group row">
              <label for="addressLineTwoInput" class="col-form-label col-sm-3">Address Line 2</label>
              <div class="col-sm-9">
                <input
                  type="text"
                  class="form-control"
                  name="addressLineTwoInput"
                  v-model="lineTwo"
                />
              </div>
            </div>
            <div class="form-group row">
              <label for="addressLineThreeInput" class="col-form-label col-sm-3">Address Line 3</label>
              <div class="col-sm-9">
                <input
                  type="text"
                  class="form-control"
                  name="addressLineThreeInput"
                  v-model="lineThree"
                />
              </div>
            </div>
          </fieldset>

          <div class="row form-group">
            <div class="col-md-9">
              <label for="cityInput">Sender's City</label>
              <input type="text" name="cityInput" class="form-control" v-model="city" />
            </div>

            <div class="col-md-3">
              <label for="dateInput">Date</label>
              <input type="date" name="dateInput" class="form-control" v-model="date" />
            </div>
          </div>

          <div class="form-group">
            <label for="subjectInput">Subject Line</label>
            <input type="text" name="subjectInput" class="form-control" v-model="subjectLine" />
          </div>

          <div class="form-group">
            <label for="openingInput">Opening salutation</label>
            <input
              type="text"
              name="openingInput"
              class="form-control"
              placeholder="Dear Mr. Smith:"
              v-model="openingSalutation"
            />
          </div>

          <div class="form-group">
            <label for="coverLetterBodyInput">Body</label>
            <textarea
              name="coverLetterBodyInput"
              class="form-control"
              rows="20"
              v-model="coverLetterBody"
            />
            <small class="form-text text-muted">Use Markdown.</small>
          </div>

          <div class="form-group">
            <label for="closingInput">Closing salutation</label>
            <input
              type="text"
              name="closingInput"
              class="form-control"
              placeholder="Sincerely,"
              v-model="closingSalutation"
            />
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { mapState, mapActions } from "vuex";

import Spinner from "@/components/Spinner";

export default {
  name: "CoverLetter",
  props: ["jobId"],
  components: {
    Spinner
  },
  data() {
    return {
      isEdit: false,
      recipientName: "",
      lineOne: "",
      lineTwo: "",
      lineThree: "",
      city: "",
      date: "",
      subjectLine: "",
      openingSalutation: "",
      coverLetterBody: "",
      closingSalutation: ""
    };
  },
  computed: {
    ...mapState({
      isLoading: state => state.spinners.job.isLoadingCoverLetter,
      coverLetter: state => state.jobDetails.coverLetter,
      coverLetterHtml: state => state.jobDetails.coverLetterHtml
    })
  },
  created() {
    this.getCoverLetter(this.jobId).then(() => this.setDataFromObject(this.coverLetter));
  },
  methods: {
    ...mapActions(["getCoverLetter", "updateCoverLetter", "flashSuccess"]),
    extractDataToObject() {
      const data = {
        recipientName: this.recipientName,
        lineOne: this.lineOne,
        lineTwo: this.lineTwo,
        lineThree: this.lineThree,
        city: this.city,
        date: this.date,
        subjectLine: this.subjectLine,
        openingSalutation: this.openingSalutation,
        coverLetterBody: this.coverLetterBody,
        closingSalutation: this.closingSalutation
      };
      return data;
    },
    extractJobDetailsFromState() {
      const coverLetter = {
        ...this.coverLetter
      };
      return coverLetter;
    },
    setDataFromObject(data) {
      for (const [field, value] of Object.entries(data)) {
        this[field] = value;
      }
    },
    clearFields() {
      const clearData = {
        recipientName: "",
        lineOne: "",
        lineTwo: "",
        lineThree: "",
        city: "",
        date: "",
        subjectLine: "",
        openingSalutation: "",
        coverLetterBody: "",
        closingSalutation: ""
      };
      this.setDataFromObject(clearData);
    },
    toggleCoverLetter() {
      if (this.isEdit) {
        this.updateCoverLetter({
          jobId: this.jobId,
          coverLetterData: this.extractDataToObject()
        }).then(() => {
          this.flashSuccess("Changes successfully saved.");
          this.isEdit = !this.isEdit;
        });
      } else {
        this.isEdit = !this.isEdit;
      }
    }
  }
};
</script>

<style>
</style>