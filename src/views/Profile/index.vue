<template>
  <div class="container">
    <div class="row">
      <h2 class="mt-4 mb-3">Profile</h2>
    </div>
    <div class="card row">
      <div class="card-header">
        <h4 class="mb-0">Biographical</h4>
      </div>
      <div class="card-body">
        <form>
          <div class="row form-group">
            <div class="col">
              <label for="firstNameInput">First Name</label>
              <input type="text" class="form-control" id="firstNameInput" v-model="firstName" />
            </div>
            <div class="col">
              <label for="lastNameInput">Last Name</label>
              <input type="text" class="form-control" id="lastNameInput" v-model="lastName" />
            </div>
          </div>

          <div class="row form-group">
            <div class="col">
              <label for="emailInput">Email</label>
              <input type="email" class="form-control" id="emailInput" v-model="email" />
            </div>
            <div class="col">
              <label for="phoneNumberInput">Phone Number</label>
              <input type="tel" class="form-control" id="phoneNumberInput" v-model="phoneNumber" />
            </div>
          </div>
          <div class="form-group">
            <label for="websiteUrlInput">Personal Website</label>
            <input type="url" class="form-control" id="websiteUrlInput" v-model="websiteUrl" />
          </div>
          <div class="form-group">
            <label for="githubUrlInput">Github URL</label>
            <input type="url" class="form-control" id="githubUrlInput" v-model="githubUrl" />
          </div>
          <div class="form-group">
            <label for="linkedinUrlInput">LinkedIn URL</label>
            <input type="url" class="form-control" id="linkedinUrlInput" v-model="linkedinUrl" />
          </div>
          <button type="submit" class="btn btn-primary">Update</button>
        </form>
      </div>
    </div>

    <div class="card row">
      <div class="card-header">
        <h4 class="mb-0">Addresses</h4>
      </div>
      <div class="card-body">
        <div class="list-group">
          <div v-for="address in addresses" v-bind:key="address.id" class="list-group-item">
            <div class="float-left py-2">
              {{
              [address.lineOne, address.lineTwo, address.lineThree]
              .filter((x) => x)
              .join(", ")
              }}
            </div>
            <div class="float-right">
              <button type="button" class="btn btn-outline-success btn-sm mx-1">
                <i class="fas fa-edit" aria-hidden="true" />
              </button>
              <button type="button" class="btn btn-sm btn-outline-danger float-right">
                <i href class="fas fa-trash-alt" aria-hidden="true" />
              </button>
            </div>
          </div>
        </div>
        <div class="pt-3">
          <button class="btn btn-primary" @click="showAddAddressModal">Add an Address</button>
        </div>
      </div>
    </div>

    <div class="card row">
      <div class="card-header">
        <h4 class="mb-0">Education</h4>
      </div>
      <div class="container">
        <CVItem
          v-for="school in education"
          v-bind:key="school.id"
          :heading="school.school"
          :headingRight="school.location"
          :subheading="school.degreeAndField + (school.gpa ? ', GPA: ' + school.gpa : '')"
          :subheadingRight="school.dateFromTo"
          :bullets="school.description.split('\n')"
          onDelete="1"
          onEdit="1"
        />
      </div>
      <div class="card-body">
        <button class="btn btn-primary" @click="showAddEducationModal">Add Education</button>
      </div>
    </div>

    <div class="card row">
      <div class="card-header">
        <h4 class="mb-0">Skills</h4>
      </div>
      <div class="card-body">
        <vue-tags-input />
        <br />
        <button class="btn btn-primary" @click="showAddSkillModal">Add a Skill</button>
      </div>
    </div>

    <div class="card row">
      <div class="card-header">
        <h4 class="mb-0">Work History</h4>
      </div>
      <div class="container">
        <CVItem
          v-for="job in workHistory"
          v-bind:key="job.id"
          :heading="job.company"
          :headingRight="job.location"
          :subheading="job.position"
          :subheadingRight="job.dateFromTo"
          :bullets="job.description.split('\n')"
          onDelete="1"
          onEdit="1"
        />
      </div>
      <div class="card-body">
        <button class="btn btn-primary" @click="showAddWorkExperienceModal">Add a Work Experience</button>
      </div>
    </div>

    <div class="card row">
      <div class="card-header">
        <h4 class="mb-0">Personal Projects</h4>
      </div>
      <div class="container">
        <CVItem
          v-for="project in projects"
          v-bind:key="project.id"
          :heading="project.projectName"
          :headingRight="project.url"
          :bullets="project.description.split('\n')"
          onDelete="1"
          onEdit="1"
        />
      </div>
      <div class="card-body">
        <button class="btn btn-primary" @click="showAddPersonalProjectModal">Add a Personal Project</button>
      </div>
    </div>
  </div>
</template>

<script>
import { mapState } from "vuex";

import VueTagsInput from "@johmun/vue-tags-input";

import CVItem from "./CVItem";

export default {
  name: "Profile",
  components: {
    VueTagsInput,
    CVItem
  },
  data() {
    return {
      firstName: this.$store.state.profile.biographical.firstName,
      lastName: this.$store.state.profile.biographical.lastName,
      email: this.$store.state.profile.biographical.email,
      phoneNumber: this.$store.state.profile.biographical.phoneNumber,
      websiteUrl: this.$store.state.profile.biographical.websiteUrl,
      githubUrl: this.$store.state.profile.biographical.githubUrl,
      linkedinUrl: this.$store.state.profile.biographical.linkedUrl
    };
  },
  computed: {
    ...mapState({
      addresses: state => state.profile.addresses,
      education: state => state.profile.education,
      workHistory: state => state.profile.workHistory,
      projects: state => state.profile.projects
    })
  },
  methods: {
    showAddAddressModal() {
      this.$modal.show("AddEditAddressModal");
    },
    showAddEducationModal() {
      this.$modal.show("AddEditEducationModal");
    },
    showAddPersonalProjectModal() {
      this.$modal.show("AddEditPersonalProjectModal");
    },
    showAddSkillModal() {
      this.$modal.show("AddEditSkillModal");
    },
    showAddWorkExperienceModal() {
      this.$modal.show("AddEditWorkExperienceModal");
    }
  }
};
</script>

<style>
.card {
  margin-bottom: 0.5rem;
}

h2,
.card-header {
  user-select: none;
}

.ti-tag {
  background-color: #1a1a1a !important;
}
</style>
