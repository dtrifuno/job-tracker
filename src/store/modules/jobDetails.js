const state = {
  job: {},
  events: [],
  description: "",
  coverLetter: "",
};

const getters = {};

const actions = {
  /*
  async getJob({ commit }, jobId) {},
  async editDescription({ commit, state }, description) {
    commit("setDescription", description);
  },
  */
  async createEvent({ commit }, event) {
    commit("addEvent", event);
  },
  async deleteEvent({ commit }, eventID) {
    commit("removeEvent", eventID);
  },
  async editEvent({ commit }, event) {
    commit("updateEvent", event);
  },
};

const mutations = {
  setJob: (state, job) => (state.job = job),
  setDescription: (state, description) => (state.description = description),
  addEvent: (state, event) => state.events.push(event),
  removeEvent: (state, eventID) =>
    (state.events = state.events.filter((x) => x.id !== eventID)),
  updateEvent: (state, event) => {
    const idx = state.events.findIndex((x) => x.id === event.id);
    if (idx >= 0) {
      state.events.splice(idx, 1, event);
    }
  },
};

export default {
  state,
  getters,
  actions,
  mutations,
};
