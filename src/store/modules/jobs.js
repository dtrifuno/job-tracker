import { doQuery, doDelete, executeString } from "@/link";
import { compareStatusCodes } from "@/utils";

const state = {
  jobs: [],
  sortBy: {
    key: "dateCreated",
    ascending: false,
  },
  jobSearchString: "",
};

const getters = {
  sortedAndFilteredJobs: (state, getters) => {
    const { key, ascending } = state.sortBy;
    const sortedJobs = [...getters.filteredJobs]
    if (key === "status") {
      sortedJobs.sort((a, b) => compareStatusCodes(a.status, b.status))
    } else {
      sortedJobs.sort((a, b) => a[key].localeCompare(b[key]))
    }

    if (!ascending) {
      sortedJobs.reverse();
    }
    return sortedJobs;
    
  },

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
  fetchJobs({ commit }) {
    return doQuery(`
      jobs {
        id, company, position, location, status, dateCreated, dateUpdated
      }
    `).then((res) => {
      commit("setJobs", res.data.jobs);
    });
  },
  sortTableBy({ commit, state }, category) {
    const sortBy = {
      key: category,
      ascending:
        state.sortBy.key !== category ? true : !state.sortBy.ascending,
    };
    commit("setSortBy", sortBy);
  },
  createJob({ commit }, { date, jobData }) {
    return executeString(
      `mutation CreateJob($date: String!, $jobData: JobInput!) {
        createJob(date: $date, jobData: $jobData) {
          job { id, company, position, location, status, dateCreated, dateUpdated }
        }
    }`,
      { jobData, date }
    ).then((res) => commit("addJob", res.data.createJob.job));
  },
  deleteJob({ commit }, jobId) {
    return doDelete("job", jobId).then(() => commit("removeJob", jobId));
  },
};

const mutations = {
  setJobs: (state, jobs) => (state.jobs = jobs),
  setSortBy: (state, sortBy) => (state.sortBy = sortBy),
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
