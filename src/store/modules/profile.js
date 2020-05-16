import {
  doQuery,
  executeString,
  doCreateFromObject,
  doEditFromObject,
  doDelete,
} from "@/link";

const state = {
  isProfileLoaded: false,
  biographicalData: {
    firstName: "",
    lastName: "",
    email: "",
    phoneNumber: "",
    websiteUrl: "",
    githubUrl: "",
    linkedinUrl: "",
  },
  addresses: [],
  education: [],
  skills: [],
  workHistory: [],
  projects: [],
};

const getters = {
  sortedEducation(state) {
    const sorted = [...state.education].sort(
      (x, y) => -x.dateFrom.localeCompare(y.dateFrom)
    );
    return sorted;
  },
  sortedWorkHistory(state) {
    const sorted = [...state.workHistory].sort(
      (x, y) => -x.dateFrom.localeCompare(y.dateFrom)
    );
    return sorted;
  },
  groupedSkills(state) {
    const grouped = {};
    for (const object of state.skills) {
      const { category } = object;
      if (grouped[category] !== undefined) {
        grouped[category].push({ ...object });
      } else {
        grouped[category] = [{ ...object }];
      }
    }

    const categories = Object.getOwnPropertyNames(grouped);
    const sortedCategories = [...categories].sort((x, y) => x.localeCompare(y));

    for (const category of sortedCategories) {
      grouped[category] = [...grouped[category]].sort((x, y) =>
        x.skill.localeCompare(y.skill)
      );
    }

    return { sortedCategories, sortedSkills: grouped };
  },
};

const actions = {
  // Biographical data actions
  getProfile({ commit }) {
    return doQuery(`
      profile {
        firstName, lastName, email, phoneNumber, websiteUrl,
        githubUrl, linkedinUrl
      },
      addresses {
        id, lineOne, lineTwo, lineThree
      },
      education {
        id, school, location, degreeAndField, gpa, dateFrom,
        dateTo, description
      },
      skills {
        id, skill, category
      },
      workHistory {
        id, company, position, location, dateFrom, dateTo, description
      },
      personalProjects {
        id, projectName, url, description
      }
    `).then((res) => {
      commit("setIsLoaded", true);
      commit("setBiographicalData", res.data.profile);
      commit("setAddresses", res.data.addresses);
      commit("setEducation", res.data.education);
      commit("setSkills", res.data.skills);
      commit("setWorkHistory", res.data.workHistory);
      commit("setProjects", res.data.personalProjects);
    });
  },
  editBiographicalData({ commit }, biographicalDataData) {
    return executeString(
      `mutation EditBiographicalData($biographicalDataData: BiographicalDataInput!) {
        editBiographicalData(biographicalDataData: $biographicalDataData) {
         profile { firstName, lastName, email, phoneNumber, websiteUrl, githubUrl, linkedinUrl }
        }
  }`,
      { biographicalDataData }
    ).then((res) => {
      commit("setBiographicalData", res.data.editBiographicalData.profile);
    });
  },

  // Address actions
  createAddress({ commit }, { addressData }) {
    return doCreateFromObject("address", addressData).then((res) =>
      commit("addAddress", res.data.createAddress.address)
    );
  },
  editAddress({ commit }, { id, addressData }) {
    return doEditFromObject("address", id, addressData).then((res) =>
      commit("updateAddress", res.data.editAddress.address)
    );
  },
  deleteAddress({ commit }, addressId) {
    return doDelete("address", addressId).then(() =>
      commit("removeAddress", addressId)
    );
  },

  // Education experience actions
  createEducationExperience({ commit }, { educationExperienceData }) {
    return doCreateFromObject(
      "educationExperience",
      educationExperienceData
    ).then((res) =>
      commit(
        "addEducationExperience",
        res.data.createEducationExperience.educationExperience
      )
    );
  },
  editEducationExperience({ commit }, { id, educationExperienceData }) {
    return doEditFromObject(
      "educationExperience",
      id,
      educationExperienceData
    ).then((res) =>
      commit(
        "updateEducationExperience",
        res.data.editEducationExperience.educationExperience
      )
    );
  },
  deleteEducationExperience({ commit }, educationId) {
    return doDelete("educationExperience", educationId).then(() =>
      commit("removeEducationExperience", educationId)
    );
  },

  // Skill actions
  async createSkill({ commit }, { skillData }) {
    return doCreateFromObject("skill", skillData).then((res) =>
      commit("addSkill", res.data.createSkill.skill)
    );
  },
  async editSkill({ commit }, { id, skillData }) {
    return doEditFromObject("skill", id, skillData).then((res) =>
      commit("updateSkill", res.data.editSkill.skill)
    );
  },
  async deleteSkill({ commit }, skillId) {
    return doDelete("skill", skillId).then(() =>
      commit("removeSkill", skillId)
    );
  },

  // Work experience actions
  async createWorkExperience({ commit }, { workExperienceData }) {
    return doCreateFromObject(
      "workExperience",
      workExperienceData
    ).then((res) =>
      commit("addWorkExperience", res.data.createWorkExperience.workExperience)
    );
  },
  async editWorkExperience({ commit }, { id, workExperienceData }) {
    return doEditFromObject(
      "workExperience",
      id,
      workExperienceData
    ).then((res) =>
      commit("updateWorkExperience", res.data.editWorkExperience.workExperience)
    );
  },
  async deleteWorkExperience({ commit }, workId) {
    return doDelete("workExperience", workId).then(() =>
      commit("removeWorkExperience", workId)
    );
  },

  // Personal projects actions
  async createPersonalProject({ commit }, { personalProjectData }) {
    return doCreateFromObject(
      "personalProject",
      personalProjectData
    ).then((res) =>
      commit(
        "addPersonalProject",
        res.data.createPersonalProject.personalProject
      )
    );
  },
  async editPersonalProject({ commit }, { id, personalProjectData }) {
    return doEditFromObject(
      "personalProject",
      id,
      personalProjectData
    ).then((res) =>
      commit(
        "updatePersonalProject",
        res.data.editPersonalProject.personalProject
      )
    );
  },
  async deletePersonalProject({ commit }, projectId) {
    return doDelete("personalProject", projectId).then(() =>
      commit("removePersonalProject", projectId)
    );
  },
};

const mutations = {
  // Profile mutations
  setIsLoaded: (state, value) => state.isProfileLoaded = value,
  setAddresses: (state, addresses) => (state.addresses = addresses),
  setEducation: (state, education) => (state.education = education),
  setSkills: (state, skills) => (state.skills = skills),
  setWorkHistory: (state, workHistory) => (state.workHistory = workHistory),
  setProjects: (state, projects) => (state.projects = projects),
  setBiographicalData: (state, biographicalData) =>
    (state.biographicalData = {
      ...state.biographicalData,
      ...biographicalData,
    }),

  // Address mutations
  addAddress: (state, address) => state.addresses.unshift(address),
  updateAddress: (state, address) => {
    const idx = state.addresses.findIndex((x) => x.id === address.id);
    if (idx >= 0) {
      state.addresses.splice(idx, 1, address);
    }
  },
  removeAddress: (state, addressId) =>
    (state.addresses = state.addresses.filter((x) => x.id !== addressId)),

  // Education experience mutations
  addEducationExperience: (state, educationExperience) =>
    state.education.unshift(educationExperience),
  updateEducationExperience: (state, educationExperience) => {
    const idx = state.education.findIndex(
      (x) => x.id === educationExperience.id
    );
    if (idx >= 0) {
      state.education.splice(idx, 1, educationExperience);
    }
  },
  removeEducationExperience: (state, educationID) =>
    (state.education = state.education.filter((x) => x.id !== educationID)),

  // Work experience mutations
  addWorkExperience: (state, workExperience) =>
    state.workHistory.unshift(workExperience),
  updateWorkExperience: (state, workExperience) => {
    const idx = state.workHistory.findIndex((x) => x.id === workExperience.id);
    if (idx >= 0) {
      state.workHistory.splice(idx, 1, workExperience);
    }
  },
  removeWorkExperience: (state, workID) =>
    (state.workHistory = state.workHistory.filter((x) => x.id !== workID)),

  // Skill mutations
  addSkill: (state, skill) => state.skills.unshift(skill),
  updateSkill: (state, skill) => {
    const idx = state.skills.findIndex((x) => x.id === skill.id);
    if (idx >= 0) {
      state.skills.splice(idx, 1, skill);
    }
  },
  removeSkill: (state, skillId) =>
    (state.skills = state.skills.filter((x) => x.id !== skillId)),

  // Personal project mutations
  addPersonalProject: (state, personalProject) =>
    state.projects.unshift(personalProject),
  updatePersonalProject: (state, personalProject) => {
    const idx = state.projects.findIndex((x) => x.id === personalProject.id);
    if (idx >= 0) {
      state.projects.splice(idx, 1, personalProject);
    }
  },
  removePersonalProject: (state, projectID) =>
    (state.projects = state.projects.filter((x) => x.id !== projectID)),
};

export default {
  state,
  getters,
  actions,
  mutations,
};
