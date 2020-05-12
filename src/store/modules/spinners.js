const state = {
  profile: {
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
  setProfileLoading: (state) => {
    const profileIsLoading = {
      isLoadingBiographical: true,
      isLoadingAddresses: true,
      isLoadingEducation: true,
      isLoadingSkills: true,
      isLoadingWorkHistory: true,
      isLoadingPersonalProjects: true,
    };
    state.profile = { ...state.profile, ...profileIsLoading };
  },
  unsetProfileLoading: (state) => {
    const profileIsNotLoading = {
      isLoadingBiographical: false,
      isLoadingAddresses: false,
      isLoadingEducation: false,
      isLoadingSkills: false,
      isLoadingWorkHistory: false,
      isLoadingPersonalProjects: false,
    };
    state.profile = { ...state.profile, ...profileIsNotLoading };
  },
  toggleLoadingBiographical: (state) =>
    (state.profile.isLoadingBiographical = !state.profile
      .isLoadingBiographical),
  toggleLoadingAddresses: (state) =>
    (state.profile.isLoadingAddresses = !state.profile.isLoadingAddresses),
  toggleLoadingEducation: (state) =>
    (state.profile.isLoadingEducation = !state.profile.isLoadingEducation),
  toggleLoadingSkills: (state) =>
    (state.profile.isLoadingSkills = !state.profile.isLoadingSkills),
  toggleLoadingWorkHistory: (state) =>
    (state.profile.isLoadingWorkHistory = !state.profile.isLoadingWorkHistory),
  toggleLoadingPersonalProjects: (state) =>
    (state.profile.isLoadingPersonalProjects = !state.profile
      .isLoadingPersonalProjects),

  toggleLoadingJobs: (state) => (state.isLoadingJobs = !state.isLoadingJobs),

  unsetJobLoading: (state) => {
    const jobIsNotLoading = {
      isLoadingJobDetails: false,
      isLoadingEvents: false,
      isLoadingJobDescription: false,
      isLoadingCV: false,
      isLoadingCoverLetter: false,
    };
    state.job = { ...state.job, ...jobIsNotLoading };
  },
  setJobLoading: (state) => {
    const jobIsLoading = {
      isLoadingJobDetails: true,
      isLoadingEvents: true,
      isLoadingJobDescription: true,
      isLoadingCV: true,
      isLoadingCoverLetter: true,
    };
    state.job = { ...state.job, ...jobIsLoading };
  },
  toggleLoadingJobDetails: (state) =>
    (state.job.isLoadingJobDetails = !state.job.isLoadingJobDetails),
  toggleLoadingEvents: (state) =>
    (state.job.isLoadingEvents = !state.job.isLoadingEvents),
  toggleLoadingJobDescription: (state) =>
    (state.job.isLoadingJobDescription = !state.job.isLoadingJobDescription),
  toggleLoadingCV: (state) => (state.job.isLoadingCV = !state.job.isLoadingCV),
  toggleLoadingCoverLetter: (state) =>
    (state.job.isLoadingCoverLetter = !state.job.isLoadingCoverLetter),
};

export default {
  state,
  getters,
  actions,
  mutations,
};
