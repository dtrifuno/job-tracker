import {
  doQuery,
  doDelete,
  executeString,
  doEditFromObject,
} from "@/link";

const state = {
  details: {
    location: "",
    position: "",
    company: "",
    url: "",
    events: [],
    description: "",
    coverLetter: "",
  },
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
  createEvent({ commit }, {jobId, eventData}) {
    console.log(jobId, eventData)
    return executeString(
      `mutation CreateEvent($jobId: ID!, $eventData: EventInput!) {
        createEvent(jobId: $jobId, eventData: $eventData) {
          event { id, ${Object.keys(eventData).join(", ")} }
        }
    }`,
      { eventData, jobId }
    )
    .then((res) =>
      commit("addEvent", res.data.createEvent.event))
  },
  deleteEvent({ commit }, eventId) {
    return doDelete("event", eventId).then(() =>
      commit("removeEvent", eventId)
    );
  },
  editEvent({ commit }, { id, eventData }) {
    return doEditFromObject("event", id, eventData).then((res) =>
      commit("updateEvent", res.data.editEvent.event)
    )
  },
};

const mutations = {
  updateJob: (state, job) => (state.details = { ...state.details, ...job }),
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
