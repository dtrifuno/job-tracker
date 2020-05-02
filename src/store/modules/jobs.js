/* eslint-disable */

const state = {
  jobs: [],
  jobSearchString: "",
};

const getters = {
  filteredJobs: (state) => {
    const { jobSearchString } = state;
    const fragments = jobSearchString.toLowerCase().split(/[\s,]+/);
    return state.jobs.filter((job) => {
      const jobString = Object.values(job)
        .join(" ")
        .toLowerCase();
      for (const fragment of fragments) {
        if (!jobString.includes(fragment)) {
          return false;
        }
      }
      return true;
    });
  },
};

const actions = {
  async fetchJobs({ commit }) {
    const response = [
      {
        id: 1,
        company: "McDonalds",
        position: "Clown",
        location: "Remote",
        status: "Rejected",
        date_updated: "April 3, 2020",
        date_created: "April 3, 2020",
      },
      {
        id: 2,
        company: "Cryptids Inc.",
        position: "Bigfoot Hunter",
        location: "Chicago, IL",
        status: "Interview Scheduled",
        date_created: "April 13, 2020",
        date_updated: "April 23, 2020",
      },
      {
        id: 3,
        company: "TSM",
        position: "TFT Pro",
        location: "Los Angeles, CA",
        status: "Offer Made",
        date_created: "April 11, 2020",
        date_updated: "April 25, 2020",
      },
      {
        id: 4,
        company: "North Macedonian Government",
        position: "Witch Doctor Apprentice",
        location: "Skopje",
        status: "Rejected",
        date_created: "April 6, 2020",
        date_updated: "April 9, 2020",
      },
    ];
    commit("setJobs", response);
  },
  async createJob({ commit }, job) {},
  async updateJob({ commit }, job) {},
  async deleteJob({ commit }, jobID) {
    commit("removeJob", jobID);
  },
};

const mutations = {
  setJobs: (state, jobs) => (state.jobs = jobs),
  updateJobSearchString: (state, newJobSearchString) =>
    (state.jobSearchString = newJobSearchString),
  addJob: (state, job) => state.jobs.unshift(job),
  removeJob: (state, jobID) =>
    (state.jobs = state.jobs.filter((x) => x.id !== jobID)),
  clearJobs: (state) => {
    state.jobs = [];
    state.jobSearchString = "";
  },
};

export default {
  state,
  getters,
  actions,
  mutations,
};
