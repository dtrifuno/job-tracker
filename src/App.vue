<template>
  <div id="app">
    <!--- Modals -->
    <AddEditAddressModal />
    <AddEditEducationModal />
    <AddJobModal />
    <AddEditPersonalProjectModal />
    <AddEditSkillModal />
    <AddEditWorkExperienceModal />
    <DeleteModal />

    <Header />
    <router-view />
    <Footer />
  </div>
</template>

<script>
import Header from "./components/layout/Header";
import Footer from "./components/layout/Footer";

import AddJobModal from "./modals/AddJobModal";
import AddEditAddressModal from "./modals/AddEditAddressModal";
import AddEditEducationModal from "./modals/AddEditEducationModal";
import AddEditPersonalProjectModal from "./modals/AddEditPersonalProjectModal";
import AddEditSkillModal from "./modals/AddEditSkillModal";
import AddEditWorkExperienceModal from "./modals/AddEditWorkExperienceModal";
import DeleteModal from "./modals/DeleteModal";

export default {
  name: "App",
  components: {
    Header,
    Footer,
    AddJobModal,
    AddEditAddressModal,
    AddEditEducationModal,
    AddEditPersonalProjectModal,
    AddEditSkillModal,
    AddEditWorkExperienceModal,
    DeleteModal
  }
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
