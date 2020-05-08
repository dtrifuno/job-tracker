import {
  doQuery,
  doCreateFromObject,
  doDelete,
  doEditFromObject,
} from "@/link";

const state = {
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
  skills: [
    { skill: "C++", category: "Languages" },
    { skill: "Python", category: "Languages" },
    { skill: "JavaScript", category: "Languages" },
    { skill: "PostgreSQL", category: "Databases" },
    { skill: "SQLite", category: "Databases" },
    { skill: "MongoDB", category: "Databases" },
  ],
  workHistory: [
    {
      company: "University of Illinois at Chicago",
      position: "Graduate Teaching Assistant",
      location: "Chicago, IL",
      dateFrom: "2013-08",
      dateTo: "2019-07",
      description: `Led discussion sections for calculus, differential equations and linear algebra courses.
        Taught developmental summer courses for incoming freshmen.
        Provided drop-in tutoring at the UIC Mathematical Sciences Learning Center.`,
    },
  ],
  projects: [
    {
      id: 7,
      projectName: "Tabla",
      url: "trifunovski.me/tabla",
      description: `A web-based Kanban-style project management board.
        Backend is written in Python, using the Flask web framework and MongoDB.
        Frontend is written in JavaScript using the VueUI framework.`,
    },
    {
      id: 11,
      projectName: "OFCjs",
      url: "trifunovski.me/ofcjs",
      description: `A web open-face Chinese poker game that allows the user to play against another player.
      The backend is written in JavaScript as a Node.js application, while the frontend uses the ReactUI framework.`,
    },
  ],
};

const getters = {};

const actions = {
  // Biographical data actions
  getProfile({ commit }) {
    return doQuery(`
      profile {
        firstName,
        lastName,
        email,
        phoneNumber,
        websiteUrl,
        githubUrl,
        linkedinUrl,
      },
      addresses {
        id,
        lineOne,
        lineTwo,
        lineThree
      },
      education {
        id,
        school,
        location,
        degreeAndField,
        gpa,
        dateFrom,
        dateTo,
        description
      }
    `).then((res) => {
      commit("setBiographicalData", res.data.profile);
      commit("setAddresses", res.data.addresses);
      commit("setEducation", res.data.education);
    });
  },
  editBiographicalData({ commit }, biographicalData) {
    doEditFromObject("editBiographicalData", "profile", biographicalData).then(
      (res) => {
        commit("setBiographicalData", res.data.editBiographicalData.profile);
      }
    );
  },

  // Address actions
  async createAddress({ commit }, addressData) {
    return doCreateFromObject("address", addressData)
      .then((res) => commit("addAddress", res.data.createAddress.address))
      .catch((err) => console.log(err));
  },
  async editAddress({ commit }, {id, addressData}) {
    console.log({id, addressData})
    return doEditFromObject("address", id, addressData).then((res) =>
      commit("updateAddress", res.data.editAddress.address)
    );
  },
  async deleteAddress({ commit }, addressId) {
    return doDelete("deleteAddress", addressId).then(() =>
      commit("removeAddress", addressId)
    );
  },

  // Education experience actions
  createEducationExperience({ commit }, educationExperienceData) {
    return doCreateFromObject("educationExperience", educationExperienceData).then((res) =>
      commit(
        "addEducationExperience",
        res.data.createEducationExperience.educationExperience
      )
    );
  },
  editEducationExperience({ commit }, {id, educationExperienceData}) {
    return doEditFromObject("educationExperience", id, educationExperienceData).then((res) =>
      commit(
        "updateEducationExperience",
        res.data.editEducationExperience.educationExperience
      )
    );
  },
  async deleteEducationExperience({ commit }, educationId) {
    return doDelete("deleteEducationExperience", educationId).then(() =>
      commit("removeEducationExperience", educationId)
    );
  },

  // Skills actions

  //
  async createWorkExperience({ commit }, workExperience) {
    commit("addWorkExperience", workExperience);
  },
  async editWorkExperience({ commit }, workExperience) {
    commit("updateWorkExperience", workExperience);
  },
  async deleteWorkExperience({ commit }, workID) {
    commit("removeWorkExperience", workID);
  },

  //
  async createPersonalProject({ commit }, personalProject) {
    commit("addPersonalProject", personalProject);
  },
  async editPersonalProject({ commit }, personalProject) {
    commit("updatePersonalProject", personalProject);
  },
  async deletePersonalProject({ commit }, projectID) {
    commit("removePersonalProject", projectID);
  },
};

const mutations = {
  addAddress: (state, address) => state.addresses.unshift(address),
  setAddresses: (state, addresses) => (state.addresses = addresses),
  setEducation: (state, education) => (state.education = education),
  setBiographicalData: (state, biographicalData) =>
    (state.biographicalData = {
      ...state.biographicalData,
      ...biographicalData,
    }),
  updateAddress: (state, address) => {
    const idx = state.addresses.findIndex((x) => x.id === address.id);
    if (idx >= 0) {
      state.addresses.splice(idx, 1, address);
    }
  },
  removeAddress: (state, addressId) =>
    (state.addresses = state.addresses.filter((x) => x.id !== addressId)),
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
  //
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
