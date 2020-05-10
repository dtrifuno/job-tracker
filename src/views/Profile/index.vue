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
        <form novalidate @submit.prevent="onSubmit">
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
      <CardTitle title="Addresses" :onClick="showAddAddressModal" />
      <div class="container">
        <div class="list-group" :class="{ 'my-2' : addresses.length > 0}">
          <div v-for="address in addresses" v-bind:key="address.id" class="list-group-item">
            <div class="float-left py-2">{{ addressToString(address) }}</div>
            <div class="float-right">
              <button
                type="button"
                class="btn btn-outline-success btn-sm mx-1"
                @click="showEditAddressModal(address)"
              >
                <i class="fas fa-edit" aria-hidden="true" />
              </button>
              <button
                type="button"
                class="btn btn-sm btn-outline-danger float-right"
                @click="showDeleteAddressModal(address)"
              >
                <i href class="fas fa-trash-alt" aria-hidden="true" />
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>

    <div class="card row">
      <CardTitle title="Education" :onClick="showAddEducationModal" />
      <div class="container">
        <CVItem
          v-for="school in sortedEducation"
          v-bind:key="school.id"
          :heading="school.school"
          :headingRight="school.location"
          :subheading="
            school.degreeAndField + (school.gpa ? ', GPA: ' + school.gpa : '')
          "
          :subheadingRight="
            `${renderMonth(school.dateFrom)} - ${renderMonth(school.dateTo)}`
          "
          :bullets="school.description ? school.description.split('\n'): []"
          :onEdit="() => showEditEducationModal(school)"
          :onDelete="() => showDeleteEducationModal(school)"
        />
      </div>
    </div>

    <div class="card row">
      <CardTitle title="Skills" :onClick="showAddSkillModal" />
      <div class="container">
        <table
          class="table table-bordered table-sm my-2"
          v-if="groupedSkills.sortedCategories.length > 0"
        >
          <thead>
            <th style="width: 14%" scope="col">Category</th>
            <th style="width: 86%" scope="col">Skills</th>
          </thead>
          <tbody>
            <tr v-for="(category, idx) in groupedSkills.sortedCategories" :key="idx">
              <th style="vertical-align: middle">{{category}}</th>
              <td>
                <button
                  class="btn btn-secondary"
                  v-for="skill in groupedSkills.sortedSkills[category]"
                  :key="skill.id"
                  @click="() => showEditSkillModal(skill)"
                >{{skill.skill}}</button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <div class="card row">
      <CardTitle title="Work History" :onClick="showAddWorkExperienceModal" />
      <div class="container">
        <CVItem
          v-for="job in sortedWorkHistory"
          v-bind:key="job.id"
          :heading="job.company"
          :headingRight="job.location"
          :subheading="job.position"
          :subheadingRight="
            `${renderMonth(job.dateFrom)} - ${renderMonth(job.dateTo)}`
          "
          :bullets="job.description ? job.description.split('\n') : []"
          :onEdit="() => showEditWorkExperienceModal(job)"
          :onDelete="() => showDeleteWorkExperienceModal(job)"
        />
      </div>
    </div>

    <div class="card row">
      <CardTitle title="Personal Projects" :onClick="showAddPersonalProjectModal" />
      <div class="container">
        <CVItem
          v-for="project in projects"
          v-bind:key="project.id"
          :heading="project.projectName"
          :headingRight="project.url"
          :bullets="project.description ? project.description.split('\n') : []"
          :onDelete="() => showDeletePersonalProjectModal(project)"
          :onEdit="() => showEditPersonalProjectModal(project)"
        />
      </div>
    </div>
  </div>
</template>

<script>
import { mapState, mapActions, mapGetters } from "vuex";

import { renderMonth } from "@/utils.js";

import CardTitle from "./CardTitle";
import CVItem from "./CVItem";

export default {
  name: "Profile",
  components: {
    CVItem,
    CardTitle
  },
  data() {
    return {
      firstName: "",
      lastName: "",
      email: "",
      phoneNumber: "",
      websiteUrl: "",
      githubUrl: "",
      linkedinUrl: ""
    };
  },
  computed: {
    ...mapState({
      biographicalData: state => state.profile.biographicalData,
      addresses: state => state.profile.addresses,
      projects: state => state.profile.projects
    }),
    ...mapGetters(["sortedEducation", "sortedWorkHistory", "groupedSkills"])
  },
  created() {
    this.getProfile().then(() => this.extractBiographicalDataFromState());
  },
  methods: {
    ...mapActions([
      "getProfile",
      "editBiographicalData",
      "deleteAddress",
      "deleteEducationExperience",
      "deleteWorkExperience",
      "deletePersonalProject"
    ]),
    extractBiographicalDataToObject() {
      return {
        firstName: this.firstName,
        lastName: this.lastName,
        email: this.email,
        phoneNumber: this.phoneNumber,
        websiteUrl: this.websiteUrl,
        githubUrl: this.githubUrl,
        linkedinUrl: this.linkedinUrl
      };
    },
    setDataToObject(biographicalData) {
      this.firstName = biographicalData.firstName;
      this.lastName = biographicalData.lastName;
      this.email = biographicalData.email;
      this.phoneNumber = biographicalData.phoneNumber;
      this.websiteUrl = biographicalData.websiteUrl;
      this.githubUrl = biographicalData.githubUrl;
      this.linkedinUrl = biographicalData.linkedinUrl;
    },
    extractBiographicalDataFromState() {
      this.setDataToObject(this.biographicalData);
    },
    onSubmit() {
      const oldBiographicalData = { ...this.biographicalData };
      this.editBiographicalData(this.extractBiographicalDataToObject())
        .then(() => this.extractBiographicalDataFromState())
        .catch(() => this.setDataToObject(oldBiographicalData));
    },
    renderMonth,
    addressToString(address) {
      return [address.lineOne, address.lineTwo, address.lineThree]
        .filter(x => x)
        .join(", ");
    },

    // Address modals
    showAddAddressModal() {
      this.$modal.show("AddEditAddressModal");
    },
    showDeleteAddressModal(address) {
      this.$modal.show("DeleteModal", {
        title: "Delete Address",
        target: `the address ${this.addressToString(address)}`,
        deleteAction: () => this.deleteAddress(address.id)
      });
    },
    showEditAddressModal(address) {
      this.$modal.show("AddEditAddressModal", {
        address
      });
    },

    // Education modals
    showAddEducationModal() {
      this.$modal.show("AddEditEducationModal");
    },
    showDeleteEducationModal(educationExperience) {
      this.$modal.show("DeleteModal", {
        title: "Delete Educational Experience",
        target: "this educational experience",
        deleteAction: () =>
          this.deleteEducationExperience(educationExperience.id)
      });
    },
    showEditEducationModal(educationExperience) {
      this.$modal.show("AddEditEducationModal", {
        educationExperience
      });
    },

    // Personal project modals
    showAddPersonalProjectModal() {
      this.$modal.show("AddEditPersonalProjectModal");
    },
    showDeletePersonalProjectModal(personalProject) {
      this.$modal.show("DeleteModal", {
        title: "Delete Personal Project",
        target: personalProject.projectName,
        deleteAction: () => this.deletePersonalProject(personalProject.id)
      });
    },
    showEditPersonalProjectModal(personalProject) {
      this.$modal.show("AddEditPersonalProjectModal", {
        personalProject
      });
    },

    // Skills modals
    showAddSkillModal() {
      this.$modal.show("AddEditSkillModal");
    },
    showEditSkillModal(skill) {
      this.$modal.show("AddEditSkillModal", {
        skill
      });
    },

    // Work experience modals
    showAddWorkExperienceModal() {
      this.$modal.show("AddEditWorkExperienceModal");
    },
    showDeleteWorkExperienceModal(workExperience) {
      this.$modal.show("DeleteModal", {
        title: "Delete Work Experience",
        deleteAction: () => this.deleteWorkExperience(workExperience.id)
      });
    },
    showEditWorkExperienceModal(workExperience) {
      this.$modal.show("AddEditWorkExperienceModal", {
        workExperience
      });
    }
  }
};
</script>

<style>
.card {
  margin-bottom: 0.6rem;
}

h2,
.card-header {
  user-select: none;
}
</style>
