const state = {
  notification: {},
};

const getters = {};

const actions = {
  flashError: ({ commit }, errorMsg) =>
    commit("setNotification", {
      msg: errorMsg,
      type: "error",
    }),
  flashWarning: ({ commit }, warningMsg) =>
    commit("setNotification", {
      msg: warningMsg,
      type: "warning",
    }),
  flashSuccess: ({ commit }, msg) =>
    commit("setNotification", {
      msg,
      type: "success",
    }),
};

const mutations = {
  setNotification: (state, { msg, type }) => {
    state.notification = {
      msg,
      type,
    };
  },
};

export default {
  state,
  getters,
  actions,
  mutations,
};
