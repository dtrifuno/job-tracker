<template>
  <div id="app">
    <!--- Modals -->
    <AddEditAddressModal />
    <AddEditEducationModal />
    <AddEditEventModal />
    <AddJobModal />
    <AddEditPersonalProjectModal />
    <AddEditSkillModal />
    <AddEditWorkExperienceModal />
    <DeleteModal />

    <Header />
    <Notification />
    <router-view />
    <Footer />
  </div>
</template>

<script>
import Header from "./components/layout/Header";
import Footer from "./components/layout/Footer";
import Notification from "./components/layout/Notification";

import AddJobModal from "./modals/AddJobModal";
import AddEditAddressModal from "./modals/AddEditAddressModal";
import AddEditEducationModal from "./modals/AddEditEducationModal";
import AddEditEventModal from "./modals/AddEditEventModal";
import AddEditPersonalProjectModal from "./modals/AddEditPersonalProjectModal";
import AddEditSkillModal from "./modals/AddEditSkillModal";
import AddEditWorkExperienceModal from "./modals/AddEditWorkExperienceModal";
import DeleteModal from "./modals/DeleteModal";

export default {
  name: "App",
  components: {
    Header,
    Notification,
    Footer,
    AddJobModal,
    AddEditAddressModal,
    AddEditEducationModal,
    AddEditEventModal,
    AddEditPersonalProjectModal,
    AddEditSkillModal,
    AddEditWorkExperienceModal,
    DeleteModal,
  },
};
</script>

<style>
html {
  position: relative;
  min-height: 100%;
}

body {
  margin-bottom: 80px;
}
</style>
