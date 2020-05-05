const state = {
  biographical: {
    firstName: "Darko",
    lastName: "Trifunovski",
    email: "dtrifuno@gmail.com",
    phoneNumber: "(832) 367-3567",
    websiteUrl: "https://trifunovski.me",
    githubUrl: "https://github.com/dtrifuno",
    linkedUrl: "https://www.linkedin.com/in/darko-trifunovski/",
  },
  addresses: [
    {
      id: 1,
      lineOne: "548 West Briar Place Apt. 2E",
      lineTwo: "Chicago, IL, 60657",
      lineThree: "",
    },
    {
      id: 2,
      lineOne: "11714 Cardinal Hills Court",
      lineTwo: "Cypress, TX, 77433",
      lineThree: "",
    },
  ],
  education: [
    {
      id: 11,
      school: "University of Illinois at Chicago",
      location: "Chicago, IL",
      degreeAndField: "Doctor of Philosophy in Mathematics",
      gpa: "3.7/4.0",
      dateFrom: "2013-08",
      dateTo: "2020-12",
      description: `Thesis: Rankin-Selberg L-functions of the Unitary Similitude Group of Order Two
        Relevant Coursework: Computer Networking, Mathematical Foundations of Data Science, Statistical Techniques for Machine Learning, Software Vulnerability Analysis, Computational Finance`,
    },
    {
      id: 12,
      school: "Reed College",
      location: "Portland, OR",
      degreeAndField: "Bachelor of Arts in Mathematics",
      gpa: "3.8/4.0",
      dateFrom: "2009-08",
      dateTo: "2013-05",
      description: `Thesis: Computing the Extreme Core of Siegel Modular Forms, Advisor: Jerry Shurman
         Phi Beta Kappa
         Relevant Coursework: Algorithms and Data Structures, Parallel Computing, Distributed Systems, Theory of Computation, Programming Languages`,
    },
  ],
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
  //
  async createAddress({ commit }, address) {
    commit("addAddress", address);
  },
  async editAddress({ commit }, address) {
    commit("updateAddress", address);
  },
  async deleteAddress({ commit }, addressID) {
    commit("removeAddress", addressID);
  },
  //
  async createEducationExperience({ commit }, educationExperience) {
    commit("addEducationExperience", educationExperience);
  },
  async editEducationExperience({ commit }, educationExperience) {
    commit("updateEducationExperience", educationExperience);
  },
  async deleteEducationExperience({ commit }, educationID) {
    commit("removeEducationExperience", educationID);
  },
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
