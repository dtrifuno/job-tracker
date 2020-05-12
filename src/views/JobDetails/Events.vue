<template>
<div class="py-3 p-2">
  <table class="table table-sm table-hover">
    <thead>
      <tr>
        <th style="width: 10%">Date</th>
        <th style="width: 18%">Event</th>
        <th style="width: 72%"></th>
      </tr>
    </thead>
    <tbody>
      <tr v-for="event in events" :key="event.id" @click="() => showEditEventModal(event)" class="event-row">
        <td>{{ toLocaleDateString(event.date) }}</td>
        <td>{{ statusCodeToMsg(event.eventType) }}</td>
        <td>{{ extractAdditonalDataFromEvent(event) }}</td>
      </tr>
    </tbody>
  </table>
</div>
</template>

<script>
import {
  statusCodeToMsg,
  toLocaleDateString,
  extractAdditonalDataFromEvent
} from "@/utils";

export default {
  name: "Events",
  props: {
    events: Array
  },
  methods: {
    statusCodeToMsg,
    toLocaleDateString,
    extractAdditonalDataFromEvent,
    showEditEventModal(event) {
      this.$modal.show("AddEditEventModal", {
        event
      });
    }
  }
};
</script>

<style scoped>
.event-row {
  cursor: pointer;
}
</style>