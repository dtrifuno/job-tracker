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
    descriptionHtml: "",
  },
  cv: {
    address: null,
    education: [],
    skills: [],
    workHistory: [],
    projects: [],
  },
  cvHtml: "",
  coverLetter: {
    recipientName: "",
    lineOne: "",
    lineTwo: "",
    lineThree: "",
    city: "",
    date: "",
    subjectLine: "",
    openingSalutation: "",
    coverLetterBody: "",
    closingSalutation: "",
  },
  coverLetterHtml: "",
};

const getters = {};

const actions = {
  getJob({ commit }, jobId) {
    commit("setLoadingJobDetails", true, { root: true });
    commit("setLoadingJobDescription", true, { root: true });
    commit("setLoadingEvents", true, { root: true });
    return doQuery(`job(id: "${jobId}") {
        id, company, position, location, url, description, descriptionHtml,
        events {
           id, date, eventType, eventDate, comment
          }
        }`)
      .then((res) => commit("updateJob", res.data.job))
      .finally(() => {
        commit("setLoadingJobDetails", false, { root: true });
        commit("setLoadingJobDescription", false, { root: true });
        commit("setLoadingEvents", false, { root: true });
      });
  },
  updateJob({ commit }, { id, jobData }) {
    commit("setLoadingJobDetails", true, { root: true });
    return doEditFromObject("job", id, jobData)
      .then((res) => commit("updateJob", res.data.editJob.job))
      .finally(() => commit("setLoadingJobDetails", false, { root: true }));
  },
  updateJobDescription({ commit }, { id, description }) {
    commit("setLoadingJobDescription", true, { root: true });
    return executeString(
      `mutation EditJob($id: ID!, $jobData: JobInput!) {
        editJob(id: $id, jobData: $jobData) {
          job { description, descriptionHtml }
        }
    }`,
      { id, jobData: { description } }
    )
      .then((res) => commit("updateJob", res.data.editJob.job))
      .finally(() => commit("setLoadingJobDescription", false, { root: true }));
  },
  createEvent({ commit }, { jobId, eventData }) {
    commit("setLoadingEvents", true, { root: true });
    return executeString(
      `mutation CreateEvent($jobId: ID!, $eventData: EventInput!) {
        createEvent(jobId: $jobId, eventData: $eventData) {
          event { id, ${Object.keys(eventData).join(", ")} }
        }
    }`,
      { eventData, jobId }
    )
      .then((res) => commit("addEvent", res.data.createEvent.event))
      .finally(() => commit("setLoadingEvents", false, { root: true }));
  },
  deleteEvent({ commit }, eventId) {
    commit("setLoadingEvents", true, { root: true });
    return doDelete("event", eventId)
      .then(() => commit("removeEvent", eventId))
      .finally(() => commit("setLoadingEvents", false, { root: true }));
  },
  editEvent({ commit }, { id, eventData }) {
    commit("setLoadingEvents", true, { root: true });
    return doEditFromObject("event", id, eventData)
      .then((res) => commit("updateEvent", res.data.editEvent.event))
      .finally(() => commit("setLoadingEvents", false, { root: true }));
  },
  getCV({ commit }, jobId) {
    commit("setLoadingCV", true, { root: true });
    return doQuery(`
      cv(id: "${jobId}") { address, education, skills, workHistory, projects },
      cvHtml(id: "${jobId}")
    `)
      .then((res) => {
        commit("setCv", res.data.cv);
        commit("setCvHtml", res.data.cvHtml);
      })
      .finally(() => commit("setLoadingCV", false, { root: true }));
  },
  updateCV({ commit }, { jobId, addIds, removeIds }) {
    commit("setLoadingCV", true, { root: true });
    return executeString(
      `mutation UpdateCv($jobId: ID!, $addIds: [ID]!, $removeIds: [ID]!) {
        updateCv(jobId: $jobId, addIds: $addIds, removeIds: $removeIds) {
          cv { address, education, skills, workHistory, projects },
          cvHtml
        }
    }`,
      { jobId, addIds, removeIds }
    )
      .then((res) => {
        commit("setCv", res.data.updateCv.cv);
        commit("setCvHtml", res.data.updateCv.cvHtml);
      })
      .finally(() => commit("setLoadingCV", false, { root: true }));
  },

  getCoverLetter({ commit }, jobId) {
    commit("setLoadingCoverLetter", true, { root: true });
    return doQuery(`
      coverLetter(id: "${jobId}") {
        recipientName, lineOne, lineTwo, lineThree, city,
        date, subjectLine, openingSalutation, coverLetterBody,
        closingSalutation
      },
      coverLetterHtml(id: "${jobId}")
    `)
      .then((res) => {
        commit("setCoverLetter", res.data.coverLetter);
        commit("setCoverLetterHtml", res.data.coverLetterHtml);
      })
      .finally(() => commit("setLoadingCoverLetter", false, { root: true }));
  },

  updateCoverLetter({ commit }, { jobId, coverLetterData }) {
    commit("setLoadingCoverLetter", true, { root: true });
    return executeString(
      `mutation UpdateCoverLetter($jobId: ID!, $coverLetterData: CoverLetterInput!) {
        updateCoverLetter(jobId: $jobId, coverLetterData: $coverLetterData) {
          coverLetter {
            recipientName, lineOne, lineTwo, lineThree, city,
            date, subjectLine, openingSalutation, coverLetterBody,
            closingSalutation
          },
          coverLetterHtml
        }
    }`,
      { jobId, coverLetterData }
    )
      .then((res) => {
        commit("setCoverLetter", res.data.updateCoverLetter.coverLetter);
        commit("setCoverLetterHtml", res.data.updateCoverLetter.coverLetterHtml);
      })
      .finally(() => commit("setLoadingCoverLetter", false, { root: true }));
  },
};

const mutations = {
  updateJob: (state, job) => (state.details = { ...state.details, ...job }),
  setCv: (state, cv) => (state.cv = cv),
  setCvHtml: (state, cvHtml) => (state.cvHtml = cvHtml),
  setCoverLetter: (state, coverLetter) =>
    (state.coverLetter = { ...state.coverLetter, ...coverLetter }),
  setCoverLetterHtml: (state, coverLetterHtml) =>
    (state.coverLetterHtml = coverLetterHtml),
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
