const state = {
  biographical: {
    firstName: "Darko",
    lastName: "Trifunovski",
    email: "dtrifuno@gmail.com",
    phoneNumber: "(832) 367-3567",
    websiteUrl: "https://trifunovski.me",
    githubUrl: "https://github.com/dtrifuno",
    linkedUrl: "https://www.linkedin.com/in/darko-trifunovski/",
  },
  addresses: [
    {
      id: 1,
      lineOne: "548 West Briar Place Apt. 2E",
      lineTwo: "Chicago, IL, 60657",
      lineThree: "",
    },
    {
      id: 2,
      lineOne: "11714 Cardinal Hills Court",
      lineTwo: "Cypress, TX, 77433",
      lineThree: "",
    },
  ],
  education: [
    {
      id: 11,
      school: "University of Illinois at Chicago",
      location: "Chicago, IL",
      degreeAndField: "Doctor of Philosophy in Mathematics",
      gpa: "3.7/4.0",
      dateFromTo: "Aug. 2013 -- Dec. 2020",
      description: `Thesis: Rankin-Selberg L-functions of the Unitary Similitude Group of Order Two
        Relevant Coursework: Computer Networking, Mathematical Foundations of Data Science, Statistical Techniques for Machine Learning, Software Vulnerability Analysis, Computational Finance`,
    },
    {
      id: 12,
      school: "Reed College",
      location: "Portland, OR",
      degreeAndField: "Bachelor of Arts in Mathematics",
      gpa: "3.8/4.0",
      dateFromTo: "Aug. 2009 -- May 2013",
      description: `Thesis: Computing the Extreme Core of Siegel Modular Forms, Advisor: Jerry Shurman
         Phi Beta Kappa
         Relevant Coursework: Algorithms and Data Structures, Parallel Computing, Distributed Systems, Theory of Computation, Programming Languages`,
    },
  ],
  workHistory: [
    {
      company: "University of Illinois at Chicago",
      position: "Graduate Teaching Assistant",
      location: "Chicago, IL",
      dateFromTo: "Aug. 2013 -- July 2019",
      description: `Led discussion sections for calculus, differential equations and linear algebra courses.
        Taught developmental summer courses for incoming freshmen.
        Provided drop-in tutoring at the UIC Mathematical Sciences Learning Center.`,
    },
  ],
  projects: [
    {
      projectName: "Tabla",
      url: "trifunovski.me/tabla",
      description: `A web-based Kanban-style project management board.
        Backend is written in Python, using the Flask web framework and MongoDB.
        Frontend is written in JavaScript using the VueUI framework.`,
    },
    {
      projectName: "OFCjs",
      url: "trifunovski.me/ofcjs",
      description: `A web open-face Chinese poker game that allows the user to play against another player.
      The backend is written in JavaScript as a Node.js application, while the frontend uses the ReactUI framework.`,
    },
  ],
};

const getters = {};

const actions = {};

const mutations = {};

export default {
  state,
  getters,
  actions,
  mutations,
};
