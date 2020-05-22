<template>
  <div>
    <Bouncer bounceTo="login" />
    <div class="container">
      <div class="row">
        <h2 class="mt-4 mb-3">Job Details</h2>
      </div>
      <div class="card row">
        <CardTitle
          title="General"
          buttonText="Save"
          :buttonDisabled="spinners.isLoadingJobDetails"
          :onClick="onClickUpdate"
        />
        <div class="card-body">
          <Spinner v-if="spinners.isLoadingJobDetails" />
          <div v-else>
            <div class="form-group">
              <label for="companyInput">Company</label>
              <input type="text" class="form-control" id="companyInput" v-model="company" />
            </div>
            <div class="form-group">
              <label for="positionInput">Position</label>
              <input type="text" class="form-control" id="positionInput" v-model="position" />
            </div>
            <div class="form-group">
              <label for="locationInput">Location</label>
              <input type="text" class="form-control" id="locationInput" v-model="location" />
            </div>
            <div class="form-group">
              <label for="urlInput">URL</label>
              <input type="url" class="form-control" id="urlInput" v-model="url" />
            </div>
          </div>
        </div>
      </div>

      <div class="card row">
        <CardTitle title="Timeline" :onClick="showAddEventModal" />
        <div class="container">
          <Spinner v-if="spinners.isLoadingEvents" />
          <Events v-else :events="job.events" />
        </div>
      </div>

      <div class="card row">
        <CardTitle
          title="Job Description"
          :buttonText="editDescription ? 'Save' : 'Edit'"
          :buttonDisabled="spinners.isLoadingJobDescription"
          :onClick="toggleDescription"
        />
        <div class="container">
          <Spinner v-if="spinners.isLoadingJobDescription" />
          <div v-else class="p-3 py-4">
            <div class="form-group" v-if="editDescription">
              <textarea class="form-control" rows="20" v-model="description" />
              <small class="form-text text-muted">Use Markdown.</small>
            </div>
            <div v-if="!editDescription">
              <div v-html="job.descriptionHtml" />
            </div>
          </div>
        </div>
      </div>

      <CustomizedCV :jobId="id"/>

      <CoverLetter :jobId="id"/>
    </div>
  </div>
</template>

<script>
import { mapActions, mapState } from "vuex";

import Bouncer from "@/components/Bouncer";
import Spinner from "@/components/Spinner";
import CardTitle from "@/components/CardTitle";
import Events from "./Events";
import CustomizedCV from "./CustomizedCV";
import CoverLetter from "./CoverLetter";

export default {
  name: "JobDetails",
  components: {
    Bouncer,
    CardTitle,
    CustomizedCV,
    CoverLetter,
    Events,
    Spinner
  },
  data() {
    return {
      id: null,
      company: "",
      position: "",
      location: "",
      url: "",
      description: "",
      editDescription: false
    };
  },
  computed: {
    ...mapState({
      job: state => state.jobDetails.details,
      spinners: state => state.spinners.job,
      isProfileLoaded: state => state.spinners.profile.isProfileLoaded
    })
  },
  methods: {
    ...mapActions([
      "getJob",
      "getCV",
      "getProfile",
      "updateJob",
      "updateJobDescription",
      "flashSuccess"
    ]),
    extractDataToObject() {
      const data = {
        company: this.company,
        position: this.position,
        location: this.location,
        url: this.url
      };
      return data;
    },
    extractJobDetailsFromState() {
      const jobDetails = {
        company: this.job.company,
        position: this.job.position,
        location: this.job.location,
        url: this.job.url,
        description: this.job.description
      };
      return jobDetails;
    },
    setDataFromObject(data) {
      for (const [field, value] of Object.entries(data)) {
        this[field] = value;
      }
    },
    clearFields() {
      const clearData = {
        company: "",
        position: "",
        location: "",
        url: "",
        description: ""
      };
      this.setDataFromObject(clearData);
    },
    onClickUpdate() {
      this.updateJob({
        jobData: this.extractDataToObject(),
        id: this.id
      }).then(() => {
        this.setDataFromObject(this.extractJobDetailsFromState());
        this.flashSuccess("Changes successfully saved.");
      });
    },
    toggleDescription() {
      if (this.editDescription) {
        this.updateJobDescription({
          description: this.description,
          id: this.id
        }).then(() => {
          this.flashSuccess("Changes successfully saved.");
          this.editDescription = !this.editDescription;
        });
      } else {
        this.editDescription = !this.editDescription;
      }
    },

    showAddEventModal() {
      this.$modal.show("AddEditEventModal");
    }
  },
  created() {
    this.id = this.$route.params.id;
    this.clearFields();
    if (this.id && this.id === this.job.id) {
      this.setDataFromObject(this.extractJobDetailsFromState())
    } else if (!this.isProfileLoaded) {
      this.getProfile()
        .then(() => this.getJob(this.id))
        .then(() => this.setDataFromObject(this.extractJobDetailsFromState()));
    } else {
      this.getJob(this.id).then(() =>
        this.setDataFromObject(this.extractJobDetailsFromState())
      );
    }
  }
};
</script>