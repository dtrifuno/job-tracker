<template>
  <div class="card row">
    <div class="card-header py-2">
      <h4 class="float-left my-1">Customized CV</h4>
      <div class="float-right">
        <button
          v-if="!isEdit & !isLoading"
          class="btn btn-outline-primary btn-sm mx-2"
          @click="$router.push({ name: 'print-page', params: { id: jobId, html: cvHtml } })"
        >Print</button>
        <button
          class="btn btn-outline-primary btn-sm"
          @click="onClick"
          :disabled="isLoading"
        >{{ isEdit ? "Save" : "Edit" }}</button>
      </div>
    </div>
    <div class="card-body">
      <Spinner v-if="isLoading" />
      <div class="p-2" v-else-if="!isEdit">
        <div v-html="cvHtml"></div>
      </div>
      <div v-else>
        <div>
          <small
            class="form-text text-muted"
          >Select all skills and experiences relevant to this position.</small>
          <div class="card">
            <div class="p-2">
              <section>
                <fieldset class="form-group">
                  <h5>Address</h5>
                  <ul class="list-group">
                    <li
                      class="list-group-item"
                      v-for="addressItem in profile.addresses"
                      :key="addressItem.id"
                    >
                      <div class="form-check">
                        <label class="form-check-label">
                          <input
                            type="radio"
                            class="form-check-input"
                            name="addressRadios"
                            :value="addressItem.id"
                            v-model="address"
                          />
                          {{ addressToString(addressItem) }}
                        </label>
                      </div>
                    </li>
                    <li class="list-group-item">
                      <div class="form-check">
                        <label class="form-check-label">
                          <input
                            type="radio"
                            class="form-check-input"
                            name="addressRadios"
                            :value="null"
                            v-model="address"
                          />
                          None
                        </label>
                      </div>
                    </li>
                  </ul>
                </fieldset>

                <fieldset class="form-group">
                  <h5>Education</h5>
                  <ul class="list-group">
                    <li
                      class="list-group-item d-flex justify-content-between align-items-center"
                      v-for="school in sortedEducation"
                      :key="school.id"
                    >
                      <div class="form-check">
                        <label class="form-check-label">
                          <input
                            class="form-check-input"
                            type="checkbox"
                            :value="school.id"
                            v-model="education"
                          />
                          {{ school.degreeAndField }} at
                          <span
                            class="text-uppercase"
                          >{{ school.school }}</span>
                        </label>
                      </div>
                      <span
                        class="font-italic"
                      >{{ toMonthYearString(school.dateFrom) }} – {{ toMonthYearString(school.dateTo) }}</span>
                    </li>
                  </ul>
                </fieldset>

                <fieldset class="form-group">
                  <h5>Skills</h5>
                  <table class="table table-bordered table-sm">
                    <thead>
                      <tr>
                        <th style="width: 14%" scope="col">Category</th>
                        <th style="width: 86%" scope="col">Skills</th>
                      </tr>
                    </thead>
                    <tbody>
                      <tr v-for="category in groupedSkills.sortedCategories" :key="category">
                        <th style="vertical-align: middle">{{category}}</th>
                        <td class="p-1">
                          <div
                            class="form-check form-check-inline skill-box btn p-2 py-1 m-1"
                            v-for="skill in groupedSkills.sortedSkills[category]"
                            :key="skill.id"
                          >
                            <input
                              class="form-check-input"
                              type="checkbox"
                              :id="skill.id"
                              :value="skill.id"
                              v-model="skills"
                            />
                            <label class="form-check-label" :for="skill.id">{{ skill.skill }}</label>
                          </div>
                        </td>
                      </tr>
                    </tbody>
                  </table>
                </fieldset>

                <fieldset class="form-group">
                  <h5>Work History</h5>
                  <ul class="list-group">
                    <li
                      class="list-group-item d-flex justify-content-between align-items-center"
                      v-for="job in sortedWorkHistory"
                      :key="job.id"
                    >
                      <div class="form-check">
                        <label class="form-check-label">
                          <input
                            class="form-check-input"
                            type="checkbox"
                            :value="job.id"
                            v-model="workHistory"
                          />
                          {{ job.position }} at
                          <span
                            class="text-uppercase"
                          >{{ job.company }}</span>
                        </label>
                      </div>
                      <span
                        class="font-italic"
                      >{{ toMonthYearString(job.dateFrom) }} – {{ toMonthYearString(job.dateTo) }}</span>
                    </li>
                  </ul>
                </fieldset>

                <fieldset class="form-group">
                  <h5>Personal Projects</h5>
                  <ul class="list-group">
                    <li
                      class="list-group-item"
                      v-for="project in profile.projects"
                      :key="project.id"
                    >
                      <div class="form-check">
                        <label class="form-check-label">
                          <input
                            class="form-check-input"
                            type="checkbox"
                            :value="project.id"
                            v-model="projects"
                          />
                          {{ project.projectName }}
                        </label>
                      </div>
                    </li>
                  </ul>
                </fieldset>
              </section>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { mapState, mapActions, mapGetters } from "vuex";

import { toMonthYearString, addressToString } from "@/utils";
import Spinner from "@/components/Spinner";

export default {
  name: "CustomizedCV",
  components: {
    Spinner
  },
  props: ["jobId"],
  data() {
    return {
      isEdit: false,
      address: null,
      education: [],
      skills: [],
      workHistory: [],
      projects: []
    };
  },
  computed: {
    ...mapState({
      isLoading: state => state.spinners.job.isLoadingCV,
      profile: state => state.profile,
      cv: state => state.jobDetails.cv,
      cvHtml: state => state.jobDetails.cvHtml
    }),
    ...mapGetters(["sortedEducation", "sortedWorkHistory", "groupedSkills"])
  },
  created() {
    this.getCV(this.jobId).then(() => {
      this.setDataFromObject(this.cv);
    });
  },
  methods: {
    addressToString,
    toMonthYearString,
    ...mapActions(["getCV", "updateCV"]),
    setDataFromObject(data) {
      for (const [field, value] of Object.entries(data)) {
        this[field] = value;
      }
    },
    getDiffCV() {
      const addIds = [];
      if (this.address && this.address != this.cv.address) {
        addIds.push(this.address);
      }
      for (const section of [
        "education",
        "skills",
        "workHistory",
        "projects"
      ]) {
        for (const itemId of this[section]) {
          if (!this.cv[section].includes(itemId)) {
            addIds.push(itemId);
          }
        }
      }

      const removeIds = [];
      if (this.cv.address && this.cv.address != this.address) {
        removeIds.push(this.cv.address);
      }
      for (const section of [
        "education",
        "skills",
        "workHistory",
        "projects"
      ]) {
        for (const itemId of this.cv[section]) {
          if (!this[section].includes(itemId)) {
            removeIds.push(itemId);
          }
        }
      }
      return { addIds, removeIds };
    },
    onClick() {
      if (this.isEdit) {
        const { addIds, removeIds } = this.getDiffCV();
        this.updateCV({ addIds, removeIds, jobId: this.jobId }).then(
          () => (this.isEdit = false)
        );
      } else {
        this.isEdit = true;
      }
    }
  }
};
</script>

<style scoped>
.skill-box {
  transition: color 0.15s ease-in-out, background-color 0.15s ease-in-out,
    border-color 0.15s ease-in-out, box-shadow 0.15s ease-in-out,
    -webkit-box-shadow 0.15s ease-in-out;
}

.skill-box:hover {
  background-color: #ececec;
}
</style>