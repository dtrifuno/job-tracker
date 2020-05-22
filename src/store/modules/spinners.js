const state = {
  profile: {
    isProfileLoaded: false,
    isLoadingBiographical: false,
    isLoadingAddresses: false,
    isLoadingEducation: false,
    isLoadingSkills: false,
    isLoadingWorkHistory: false,
    isLoadingPersonalProjects: false,
  },

  isLoadingJobs: false,

  job: {
    isLoadingJobDetails: false,
    isLoadingEvents: false,
    isLoadingJobDescription: false,
    isLoadingCV: false,
    isLoadingCoverLetter: false,
  },
};

const getters = {};

const actions = {};

const mutations = {
  setLoadingProfile: (state, value) => {
    state.profile = {
      ...state.profile,
      isLoadingBiographical: value,
      isLoadingAddresses: value,
      isLoadingEducation: value,
      isLoadingSkills: value,
      isLoadingWorkHistory: value,
      isLoadingPersonalProjects: value,
    };
  },
  setProfileLoaded: (state, value) => (state.profile.isProfileLoaded = value),
  setLoadingBiographical: (state, value) =>
    (state.profile.isLoadingBiographical = value),
  setLoadingAddresses: (state, value) =>
    (state.profile.isLoadingAddresses = value),
  setLoadingEducation: (state, value) =>
    (state.profile.isLoadingEducation = value),
  setLoadingSkills: (state, value) => (state.profile.isLoadingSkills = value),
  setLoadingWorkHistory: (state, value) =>
    (state.profile.isLoadingWorkHistory = value),
  setLoadingPersonalProjects: (state, value) =>
    (state.profile.isLoadingPersonalProjects = value),

  setLoadingJobs: (state, value) => (state.isLoadingJobs = value),

  setLoadingJobDetails: (state, value) =>
    (state.job.isLoadingJobDetails = value),
  setLoadingEvents: (state, value) => (state.job.isLoadingEvents = value),
  setLoadingJobDescription: (state, value) =>
    (state.job.isLoadingJobDescription = value),
  setLoadingCV: (state, value) => (state.job.isLoadingCV = value),
  setLoadingCoverLetter: (state, value) =>
    (state.job.isLoadingCoverLetter = value),
};

export default {
  state,
  getters,
  actions,
  mutations,
};
