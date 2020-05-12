import { doQuery, doDelete, executeString } from "@/link";

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
  fetchJobs({ commit }) {
    return doQuery(`
      jobs {
        id, company, position, location, status, dateCreated, dateUpdated
      }
    `).then((res) => {
      commit("setJobs", res.data.jobs);
    });
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
  setJobs: (state, jobs) => state.jobs = jobs,
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
