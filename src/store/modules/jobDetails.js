import { doQuery, doDelete, executeString, doEditFromObject } from "@/link";

const state = {
  details: {
    id: null,
    location: "",
    position: "",
    company: "",
    url: "",
    events: [],
    description: "",
    coverLetter: "",
  },
  cv: {
    address: null,
    education: [],
    skills: [],
    workHistory: [],
    projects: [],
  },
  cvHtml: "",
};

const getters = {};

const actions = {
  getJob({ commit }, jobId) {
    return doQuery(`job(id: "${jobId}") {
        id, company, position, location, url, description, coverLetter, events { id, date, eventType, eventDate, comment }
    }`).then((res) => commit("updateJob", res.data.job));
  },
  updateJob({ commit }, { id, jobData }) {
    return doEditFromObject("job", id, jobData).then((res) =>
      commit("updateJob", res.data.editJob.job)
    );
  },
  createEvent({ commit }, { jobId, eventData }) {
    console.log(jobId, eventData);
    return executeString(
      `mutation CreateEvent($jobId: ID!, $eventData: EventInput!) {
        createEvent(jobId: $jobId, eventData: $eventData) {
          event { id, ${Object.keys(eventData).join(", ")} }
        }
    }`,
      { eventData, jobId }
    ).then((res) => commit("addEvent", res.data.createEvent.event));
  },
  deleteEvent({ commit }, eventId) {
    return doDelete("event", eventId).then(() =>
      commit("removeEvent", eventId)
    );
  },
  editEvent({ commit }, { id, eventData }) {
    return doEditFromObject("event", id, eventData).then((res) =>
      commit("updateEvent", res.data.editEvent.event)
    );
  },
  getCVItems({ commit }, jobId) {
    return doQuery(`cv(id: "${jobId}") {
      address, education, skills, workHistory, projects
    }`).then((res) => commit("setCV", res.data.cv));
  },
  getCVHTML({ commit }, jobId) {
    return doQuery(`cvHtml(id: "${jobId}")`).then((res) =>
      commit("setCVHTML", res.data.cvHtml)
    );
  },
  selectCVItems({ commit }, { jobId, addIds, removeIds }) {
    return executeString(
      `mutation SelectCvItems($jobId: ID!, $addIds: [ID]!, $removeIds: [ID]!) {
        selectCvItems(jobId: $jobId, addIds: $addIds, removeIds: $removeIds) {
          cv { address, education, skills, workHistory, projects }
        }
    }`,
      { jobId, addIds, removeIds }
    ).then((res) => commit("setCV", res.data.selectCvItems.cv));
  },
};

const mutations = {
  updateJob: (state, job) => (state.details = { ...state.details, ...job }),
  setCV: (state, cv) => (state.cv = cv),
  setCVHTML: (state, cvHtml) => (state.cvHtml = cvHtml),
  addEvent: (state, event) => state.details.events.push(event),
  removeEvent: (state, eventID) =>
    (state.details.events = state.details.events.filter(
      (x) => x.id !== eventID
    )),
  updateEvent: (state, event) => {
    const idx = state.details.events.findIndex((x) => x.id === event.id);
    if (idx >= 0) {
      state.details.events.splice(idx, 1, event);
    }
  },
};

export default {
  state,
  getters,
  actions,
  mutations,
};
