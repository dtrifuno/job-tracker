<template>
  <modal name="AddEditEventModal" @before-open="beforeOpen" v-bind="modalProps">
    <div class="modal-content">
      <div class="modal-header">
        <h5 class="modal-title">{{ isUpdate ? "Edit" : "Add" }} Event</h5>
        <button type="button" class="close" aria-label="Close" @click="closeModal">
          <span aria-hidden="true">×</span>
        </button>
      </div>
      <div class="modal-body">
        <form>
          <div class="container">
            <div class="form-group row">
              <label for="eventTypeSelect" class="col-form-label col-lg-3">Event Type</label>
              <div class="col-lg-9">
                <select
                  class="form-control"
                  id="eventTypeSelect"
                  v-model="eventType"
                  @change="clearExtraFields"
                >
                  <option
                    v-for="eventType in eventTypes"
                    :key="eventType"
                    :value="eventType"
                  >{{ statusCodeToMsg(eventType) }}</option>
                </select>
              </div>
            </div>

            <div class="form-group row">
              <label for="dateInput" class="col-form-label col-lg-3">Date</label>
              <div class="col-lg-9">
                <input type="date" v-model="date" class="form-control" id="dateInput" />
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
              <label for="eventDateInput" class="col-form-label col-lg-3">Event Date</label>
              <div class="col-lg-9">
                <input type="date" v-model="eventDate" class="form-control" id="eventDateInput" />
              </div>
            </div>
            <div class="form-group row" v-if="eventType === 'Note'">
              <label for="commentInput" class="col-form-label col-lg-3">Note</label>
              <div class="col-lg-9">
                <input type="text" v-model="comment" class="form-control" id="commentInput" />
              </div>
            </div>
            <div class="row">
              <div class="ml-auto">
                <button
                  class="btn btn-primary mx-3"
                  @click="isUpdate ? onClickEdit() : onClickSubmit()"
                  :disabled="isLoading"
                >Submit</button>
                <button
                  class="btn btn-primary"
                  v-if="isUpdate"
                  @click.prevent="onClickDelete"
                  :disabled="isLoading"
                >Delete</button>
              </div>
            </div>
          </div>
        </form>
      </div>
    </div>
  </modal>
</template>

<script>
import { mapActions, mapState, mapMutations } from "vuex";

import { statusCodeToMsg } from "@/utils";

import modalProps from "./modalProps";

export default {
  name: "AddEditEventModal",
  data() {
    return {
      date: "",
      eventType: "",
      eventDate: "",
      comment: "",
      isUpdate: false,
      id: null,
      eventTypes: [
        "JobAdded",
        "Note",
        "ApplicationSubmitted",
        "ScreeningScheduled",
        "ScreeningCompleted",
        "AssessmentScheduled",
        "AssessmentCompleted",
        "InterviewScheduled",
        "InterviewCompleted",
        "Rejected",
        "OfferMade",
        "OfferAccepted",
        "OfferRejected"
      ],
      modalProps
    };
  },
  computed: {
    ...mapState({
      isLoading: state => state.spinners.job.isLoadingEvents,
      jobId: state => state.jobDetails.details.id
    })
  },
  methods: {
    statusCodeToMsg,
    ...mapActions(["createEvent", "editEvent", "deleteEvent", "flashSuccess"]),
    ...mapMutations(["toggleLoadingEvents"]),
    extractDataToObject() {
      const data = {
        date: this.date,
        eventType: this.eventType
      };
      if (this.eventDate) {
        data.eventDate = this.eventDate;
      } else if (this.comment) {
        data.comment = this.comment;
      }
      return data;
    },
    setDataFromObject(data) {
      for (const [field, value] of Object.entries(data)) {
        this[field] = value;
      }
    },
    clearFields() {
      this.date = "";
      this.eventType = "";
      this.eventDate = "";
      this.comment = "";
    },
    clearExtraFields() {
      this.eventDate = "";
      this.comment = "";
    },
    beforeOpen(event) {
      if (event.params && event.params.event) {
        this.setDataFromObject(event.params.event);
        this.id = event.params.event.id;
        this.isUpdate = true;
      } else {
        this.clearFields();
        this.id = null;
        this.isUpdate = false;
      }
    },
    onClickSubmit() {
      this.toggleLoadingEvents();
      this.createEvent({ jobId: this.jobId, eventData: this.extractDataToObject() })
        .then(() => {
          this.closeModal();
          this.flashSuccess("Event sucessfully added.");
        })
        .catch(err => err)
        .finally(this.toggleLoadingEvents);
    },
    onClickEdit() {
      this.toggleLoadingEvents();
      this.editEvent({ id: this.id, eventData: this.extractDataToObject() })
        .then(() => {
          this.closeModal();
          this.flashSuccess("Changes successfully saved.");
        })
        .catch(err => err)
        .finally(this.toggleLoadingEvents);
    },
    onClickDelete() {
      this.toggleLoadingEvents();
      this.deleteEvent(this.id)
        .then(() => {
          this.closeModal();
          this.flashSuccess("Event successfully deleted.");
        })
        .catch(err => err)
        .finally(this.toggleLoadingEvents);
    },
    closeModal() {
      this.$modal.hide("AddEditEventModal");
    }
  }
};
</script>
