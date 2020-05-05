<template>
  <modal name="AddEditEventModal" @before-open="beforeOpen" v-bind="modalProps">
    <div class="modal-content">
      <div class="modal-header">
        <h5 class="modal-title">{{ isUpdate ? "Edit" : "Add" }} Event</h5>
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
              <label for="dateInput" class="col-form-label col-lg-3"
                >Date</label
              >
              <div class="col-lg-9">
                <input
                  type="date"
                  v-model="date"
                  class="form-control"
                  id="dateInput"
                />
              </div>
            </div>

            <div class="form-group row">
              <label for="eventTypeSelect" class="col-form-label col-lg-3"
                >Event Type</label
              >
              <div class="col-lg-9">
                <select
                  class="form-control"
                  id="eventTypeSelect"
                  v-model="eventType"
                >
                  <option value="JobAdded">Job Added</option>
                  <option value="Note">
                    Note
                  </option>
                  <option value="ApplicationSubmitted">
                    Application Submitted
                  </option>
                  <option value="ScreeningScheduled">
                    Screening Scheduled
                  </option>
                  <option value="ScreeningCompleted">
                    Screening Completed
                  </option>
                  <option value="AssessmentScheduled">
                    Assessment Scheduled
                  </option>
                  <option value="AssessmentCompleted">
                    Assessment Completed
                  </option>
                  <option value="InterviewScheduled">
                    Interview Scheduled
                  </option>
                  <option value="InterviewCompleted">
                    Interview Completed
                  </option>
                  <option value="Rejected">
                    Rejected
                  </option>
                  <option value="OfferMade">
                    Offer Made
                  </option>
                  <option value="OfferAccepted">
                    Offer Accepted
                  </option>
                  <option value="OfferRejected">
                    Offer Rejected
                  </option>
                </select>
              </div>
            </div>

            <div
              class="form-group row"
              v-if="
                [
                  'ScreeningScheduled',
                  'InterviewScheduled',
                  'AssessmentScheduled',
                ].includes(eventType)
              "
            >
              <label for="lineThreeInput" class="col-form-label col-lg-3"
                >Event Date</label
              >
              <div class="col-lg-9">
                <input
                  type="text"
                  v-model="additionalData"
                  class="form-control"
                  id="lineThreeInput"
                />
              </div>
            </div>
            <div class="form-group row" v-if="eventType === 'Note'">
              <label for="lineThreeInput" class="col-form-label col-lg-3"
                >Note</label
              >
              <div class="col-lg-9">
                <input
                  type="text"
                  v-model="additionalData"
                  class="form-control"
                  id="lineThreeInput"
                />
              </div>
            </div>
            <div class="row">
              <button
                class="btn btn-primary ml-auto"
                @click="isUpdate ? onClickEdit() : onClickSubmit()"
              >
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
import { mapActions } from "vuex";

import modalProps from "./modalProps";

export default {
  name: "AddEditEventModal",
  data() {
    return {
      date: "",
      eventType: "",
      additionalData: "",
      isUpdate: false,
      id: null,
      modalProps,
    };
  },
  methods: {
    ...mapActions(["createEvent", "editEvent"]),
    beforeOpen(event) {
      if (event.params && event.params.address) {
        ["date", "eventType", "additionalData"].forEach(
          (field) => (this[field] = event.params.address[field])
        );
        this.id = event.params.address.id;
        this.isUpdate = true;
      } else {
        ["date", "lineTwo", "additionalData"].forEach(
          (field) => (this[field] = "")
        );
        this.id = null;
        this.isUpdate = false;
      }
    },
    async onClickSubmit() {
      const event = {
        date: this.date,
        eventType: this.eventType,
        additionalData: this.additionalData,
      };
      await this.createEvent(event);
    },
    async onClickEdit() {
      const event = {
        id: this.id,
        date: this.date,
        eventType: this.eventType,
        additionalData: this.additionalData,
      };
      await this.editEvent(event);
    },
    closeModal() {
      this.$modal.hide("AddEditEventModal");
    },
  },
};
</script>
