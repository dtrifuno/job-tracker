const state = {
  isAuthenticated: true,
};

const getters = {};

const actions = {
  logout({ commit }) {
    commit("clearAuthentication");
  },
};

const mutations = {
  clearAuthentication: (state) => (state.isAuthenticated = false),
};

export default {
  state,
  getters,
  actions,
  mutations,
};
