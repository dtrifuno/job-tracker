<template>
  <div>
    <Bouncer bounceTo="login"/>
    <div class="container">
      <div class="row">
        <h2 class="mt-4 mb-3">Profile</h2>
      </div>
      <div class="card row">
        <CardTitle
          title="Biographical"
          buttonText="Save"
          :onClick="onSubmit"
          :buttonDisabled="spinners.isLoadingBiographical"
        />
        <div class="card-body">
          <Spinner v-if="spinners.isLoadingBiographical" />
          <div v-else>
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
          </div>
        </div>
      </div>

      <div class="card row">
        <CardTitle title="Addresses" :onClick="showAddAddressModal" />
        <div class="container">
          <Spinner v-if="spinners.isLoadingAddresses" />
          <div class="list-group" :class="{ 'my-2' : addresses.length > 0}" v-else>
            <div
              v-for="address in addresses"
              v-bind:key="address.id"
              class="list-group-item address-item"
              @click="showEditAddressModal(address)"
            >
              <div class="float-left py-2">{{ addressToString(address) }}</div>
            </div>
          </div>
        </div>
      </div>

      <div class="card row">
        <CardTitle title="Education" :onClick="showAddEducationModal" />
        <div class="container">
          <Spinner v-if="spinners.isLoadingEducation" />
          <CVItem
            v-else
            v-for="school in sortedEducation"
            v-bind:key="school.id"
            :heading="school.school"
            :headingRight="school.location"
            :subheading="
            school.degreeAndField + (school.gpa ? ', GPA: ' + school.gpa : '')
          "
            :subheadingRight="
            `${toMonthYearString(school.dateFrom)} - ${toMonthYearString(school.dateTo)}`
          "
            :bullets="school.description ? school.description.split('\n'): []"
            :onClick="() => showEditEducationModal(school)"
          />
        </div>
      </div>

      <div class="card row">
        <CardTitle title="Skills" :onClick="showAddSkillModal" />
        <div class="container">
          <Spinner v-if="spinners.isLoadingSkills" />
          <table
            class="table table-bordered table-sm my-2"
            v-else-if="groupedSkills.sortedCategories.length > 0"
          >
            <thead>
              <th style="width: 14%" scope="col">Category</th>
              <th style="width: 86%" scope="col">Skills</th>
            </thead>
            <tbody>
              <tr v-for="(category, idx) in groupedSkills.sortedCategories" :key="idx">
                <th style="vertical-align: middle">{{category}}</th>
                <td class="p-1">
                  <button
                    class="btn btn-secondary p-2 mx-1"
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
          <Spinner v-if="spinners.isLoadingWorkHistory" />
          <CVItem
            v-else
            v-for="job in sortedWorkHistory"
            v-bind:key="job.id"
            :heading="job.company"
            :headingRight="job.location"
            :subheading="job.position"
            :subheadingRight="
            `${toMonthYearString(job.dateFrom)} - ${toMonthYearString(job.dateTo)}`
          "
            :bullets="job.description ? job.description.split('\n') : []"
            :onClick="() => showEditWorkExperienceModal(job)"
          />
        </div>
      </div>

      <div class="card row">
        <CardTitle title="Personal Projects" :onClick="showAddPersonalProjectModal" />
        <div class="container">
          <Spinner v-if="spinners.isLoadingPersonalProjects" />
          <CVItem
            v-else
            v-for="project in projects"
            v-bind:key="project.id"
            :heading="project.projectName"
            :headingRight="project.url"
            :bullets="project.description ? project.description.split('\n') : []"
            :onClick="() => showEditPersonalProjectModal(project)"
          />
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { mapState, mapActions, mapGetters, mapMutations } from "vuex";

import { toMonthYearString, addressToString } from "@/utils.js";

import Bouncer from "@/components/Bouncer";
import CardTitle from "@/components/CardTitle";
import Spinner from "@/components/Spinner";
import CVItem from "./CVItem";

export default {
  name: "Profile",
  components: {
    Bouncer,
    CardTitle,
    CVItem,
    Spinner
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
      projects: state => state.profile.projects,
      spinners: state => state.spinners.profile
    }),
    ...mapGetters(["sortedEducation", "sortedWorkHistory", "groupedSkills"])
  },
  created() {
    if (!this.spinners.isProfileLoaded) {
      this.setProfileLoading();
      this.getProfile()
        .then(this.extractBiographicalDataFromState)
        .then(this.setProfileLoaded);
    } else {
      this.extractBiographicalDataFromState();
    }
  },
  methods: {
    toMonthYearString,
    addressToString,
    ...mapActions([
      "getProfile",
      "editBiographicalData",
      "deleteAddress",
      "deleteEducationExperience",
      "deleteWorkExperience",
      "deletePersonalProject",
      "flashSuccess"
    ]),
    ...mapMutations([
      "setProfileLoading",
      "setProfileLoaded",
      "toggleLoadingBiographical"
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
    async onSubmit() {
      const oldBiographicalData = { ...this.biographicalData };
      this.toggleLoadingBiographical();
      this.editBiographicalData(this.extractBiographicalDataToObject())
        .then(() => {
          this.extractBiographicalDataFromState();
          this.flashSuccess("Changes successfully saved.");
        })
        .catch(() => this.setDataToObject(oldBiographicalData))
        .finally(this.toggleLoadingBiographical);
    },

    // Modals
    showAddAddressModal() {
      this.$modal.show("AddEditAddressModal");
    },
    showEditAddressModal(address) {
      this.$modal.show("AddEditAddressModal", {
        address
      });
    },
    showAddEducationModal() {
      this.$modal.show("AddEditEducationModal");
    },
    showEditEducationModal(educationExperience) {
      this.$modal.show("AddEditEducationModal", {
        educationExperience
      });
    },
    showAddPersonalProjectModal() {
      this.$modal.show("AddEditPersonalProjectModal");
    },
    showEditPersonalProjectModal(personalProject) {
      this.$modal.show("AddEditPersonalProjectModal", {
        personalProject
      });
    },
    showAddSkillModal() {
      this.$modal.show("AddEditSkillModal");
    },
    showEditSkillModal(skill) {
      this.$modal.show("AddEditSkillModal", {
        skill
      });
    },
    showAddWorkExperienceModal() {
      this.$modal.show("AddEditWorkExperienceModal");
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

.address-item {
  cursor: pointer;
  transition: color 0.15s ease-in-out, background-color 0.15s ease-in-out,
    border-color 0.15s ease-in-out, box-shadow 0.15s ease-in-out,
    -webkit-box-shadow 0.15s ease-in-out;
}

.address-item:hover {
  background-color: #ececec;
}
</style>
