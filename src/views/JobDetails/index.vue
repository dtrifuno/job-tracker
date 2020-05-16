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
          <div v-else class="p-2 py-3">
            <div class="form-group" v-if="editDescription">
              <textarea class="form-control" rows="20" v-model="description" />
              <small class="form-text text-muted">Use Markdown.</small>
            </div>
            <VueShowdown :markdown="description" v-if="!editDescription" />
          </div>
        </div>
      </div>

      <CustomizedCV />

      <div class="card row">
        <CardTitle
          title="Cover Letter"
          :buttonText="editCoverLetter ? 'Save' : 'Edit'"
          :buttonDisabled="spinners.isLoadingCoverLetter"
          :onClick="toggleCoverLetter"
        />
        <div class="container">
          <Spinner v-if="spinners.isLoadingCoverLetter" />
          <div v-else class="p-2 py-3">
            <div class="form-group py-2" v-if="editCoverLetter">
              <textarea class="form-control" rows="20" v-model="coverLetter" />
              <small class="form-text text-muted">Use Markdown.</small>
            </div>
            <VueShowdown :markdown="coverLetter" v-if="!editCoverLetter" />
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { mapActions, mapMutations, mapState } from "vuex";
import { VueShowdown } from "vue-showdown";

import Bouncer from "@/components/Bouncer";
import CardTitle from "@/components/CardTitle";
import CustomizedCV from "./CustomizedCV";
import Events from "./Events";
import Spinner from "@/components/Spinner";

export default {
  name: "JobDetails",
  components: { VueShowdown, Bouncer, CardTitle, CustomizedCV, Events, Spinner },
  data() {
    return {
      id: null,
      company: "",
      position: "",
      location: "",
      url: "",
      description: "",
      editDescription: false,
      coverLetter: "",
      editCoverLetter: false
    };
  },
  computed: {
    ...mapState({
      job: state => state.jobDetails.details,
      spinners: state => state.spinners.job
    })
  },
  methods: {
    ...mapActions([
      "getJob",
      "getCV",
      "getProfile",
      "updateJob",
      "flashSuccess"
    ]),
    ...mapMutations([
      "setJobLoading",
      "unsetJobLoading",
      "toggleLoadingJobDetails",
      "toggleLoadingJobDescription",
      "toggleLoadingCoverLetter"
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
        description: this.job.description,
        coverLetter: this.job.coverLetter
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
        description: "",
        coverLetter: ""
      };
      this.setDataFromObject(clearData);
    },
    onClickUpdate() {
      this.toggleLoadingJobDetails();
      this.updateJob({
        jobData: this.extractDataToObject(),
        id: this.id
      })
        .then(() => {
          this.setDataFromObject(this.extractJobDetailsFromState());
          this.flashSuccess("Changes successfully saved.");
        })
        .finally(this.toggleLoadingJobDetails);
    },
    toggleDescription() {
      if (this.editDescription) {
        this.toggleLoadingJobDescription();
        this.updateJob({
          jobData: { description: this.description },
          id: this.id
        })
          .then(() => {
            this.flashSuccess("Changes successfully saved.");
            this.editDescription = !this.editDescription;
          })
          .finally(this.toggleLoadingJobDescription);
      } else {
        this.editDescription = !this.editDescription;
      }
    },
    toggleCoverLetter() {
      if (this.editCoverLetter) {
        this.toggleLoadingCoverLetter();
        this.updateJob({
          jobData: { coverLetter: this.coverLetter },
          id: this.id
        })
          .then(() => {
            this.flashSuccess("Changes successfully saved.");
            this.editCoverLetter = !this.editCoverLetter;
          })
          .finally(this.toggleLoadingCoverLetter);
      } else {
        this.editCoverLetter = !this.editCoverLetter;
      }
    },
    showAddEventModal() {
      this.$modal.show("AddEditEventModal");
    }
  },
  created() {
    this.clearFields();
    this.setJobLoading();
    this.id = this.$route.params.id;
    this.getJob(this.id)
      .then(this.getProfile)
      .then(() => this.setDataFromObject(this.extractJobDetailsFromState()))
      .finally(this.unsetJobLoading);
  }
};
</script>

<style scoped>
.card {
  margin-bottom: 0.6rem;
}

h2,
.card-header {
  user-select: none;
}
</style>
