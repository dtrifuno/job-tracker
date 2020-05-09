import { doMutation } from "@/link";

const state = {
  username: null,
  token: localStorage.getItem("token"),
  isAuthenticated: false,
  isLoading: false,
};

const getters = {};

const actions = {
  login({ commit }, { username, password }) {
    return doMutation(
      `login(username: "${username}", password: "${password}") {
          token
      }`
    )
      .then((res) => {
        const token = res.data.login.token;
        localStorage.setItem("token", token);
        commit("setAuthentication", { username, token });
      })
      .catch((error) => console.log(error));
  },
  createUser({ commit }, { username, password }) {
    return doMutation(`
      createUser(username: "${username}", password: "${password}") {
        user {
          username
        },
        token
      }`).then((res) => {
      const { username } = res.data.createUser.user;
      const token = res.data.createUser.token;
      localStorage.setItem("token", token);
      commit("setAuthentication", { username, token });
    });
  },
  logout({ commit }) {
    commit("clearAuthentication");
  },
};

const mutations = {
  clearAuthentication: (state) => {
    state.username = null;
    state.token = null;
    state.isAuthenticated = false;
    state.isLoading = false;
  },
  setAuthentication: (state, { username, token }) => {
    state.username = username;
    state.token = token;
    state.isAuthenticated = true;
    state.isLoading = false;
  },
  loading: (state) => {
    state.isLoading = true;
  },
  loaded: (state) => {
    state.isLoading = false;
  },
};

export default {
  state,
  getters,
  actions,
  mutations,
};
