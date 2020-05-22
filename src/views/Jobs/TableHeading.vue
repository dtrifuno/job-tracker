<template>
    <th scope="col" @click="onClick">
      <div class="heading-content">
        {{ title }}
        <i v-if="sortBy.key !== category" class="fas fa-sort" />
        <i v-else-if="sortBy.ascending" class="fas fa-sort-up" />
        <i v-else class="fas fa-sort-down" />
      </div>
    </th>
</template>

<script>
import { mapState, mapActions } from "vuex";

export default {
  name: "SortingIcon",
  props: ["title", "category"],
  computed: {
    ...mapState({ sortBy: state => state.jobs.sortBy })
  },
  methods: {
    ...mapActions(["sortTableBy"]),
    onClick() {
      this.sortTableBy(this.category)
    }
  }
};
</script>

<style scoped>
.heading-content {
  cursor: pointer;
  user-select: none;
}
</style>