<template>
  <div>
    <Bouncer bounceTo="login" />
    <div class="cv-container">
      <div v-html="cvHtml" />
    </div>
  </div>
</template>

<script>
import Bouncer from "@/components/Bouncer";

export default {
  name: "PrintCV",
  components: { Bouncer },
  data() {
    return {
      cvHtml: ""
    };
  },
  created() {
    this.cvHtml = this.$route.params.cvHtml;
  }
};
</script>

<style lang="scss">
$muted: lighten(#000, 60%) !default;
$accent-color: #0394de;

.cv-container {
  font-size: 11pt;
}

.cv-header {
  display: flex;
  flex-direction: column;
  align-items: center;
  margin-bottom: 0.2in;

  .cv-name {
    display: flex;
    justify-content: center;

    h1 {
      font-size: 38pt;
      text-transform: none;
      margin-bottom: 0;
    }
  }

  .cv-address {
    font-style: italic;
    font-size: 12pt;
    color: $muted;
  }

  .cv-contact-line {
    margin-top: 0.2rem;
  }
}

.cv-contact-list {
  list-style-type: none;
  padding: 0;

  li {
    display: inline;
  }

  li:not(:last-child)::after {
    content: "|";
    margin: 0 0.45em;
  }
}

.cv-entry-row {
  display: flex;
  justify-content: space-between;
}

.cv-section {
  padding: 0.75rem 0;
}

.cv-section-title {
  font-size: 20pt;
  text-transform: none !important;
  color: $accent-color;

  display: table;
  white-space: nowrap;
  &:after {
    border-top: 1.5px solid rgba(0, 0, 0, 0.35);
    content: "";
    display: table-cell;
    position: relative;
    top: 0.8em;
    width: 97.5%;
  }
  &:after {
    left: 0.75%;
  }
}

.cv-school-name,
.cv-project-name,
.cv-company-name {
  font-size: 14pt;
  font-weight: bold;
}

.cv-school-location,
.cv-job-location {
  font-size: 13pt;
  color: $accent-color;
}

.cv-degree,
.cv-position-name {
  font-size: 14pt;
  font-variant: small-caps;
}

.cv-entry-dates {
  font-style: italic;
  font-size: 13pt;
  color: $muted;
}

.cv-description {
  ul {
    padding-left: 1.3rem;
  }
}

a {
  color: $accent-color;
}

.cv-category {
  text-transform: none;
  font-weight: bold;
  font-size: 13pt;
  text-align: right;
}

.cv-skills-list {
  font-size: 12pt;
  list-style-type: none;
  text-transform: none;
  font-weight: normal;
  padding: 0 0 0 0.5rem;
  margin: auto 0;

  li {
    display: inline;
  }

  li:not(:last-child)::after {
    content: ", ";
    margin: 0 0;
  }
}

@media print {
  a {
    text-decoration: none !important;
  }

  .cv-container {
    margin: 0.7in 1in;
  }
}

@media screen {
  .cv-container {
    max-width: 60rem;
    margin: 0 auto;
  }
}
</style>