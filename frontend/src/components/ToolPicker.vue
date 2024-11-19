<template>
  <div class="actions">
    <v-btn
      icon
      @click="tool = 'cursor'"
      :class="'color-picker-toggle ' + (tool === 'cursor' ? 'active' : '')"
    >
      <v-icon>mdi-cursor-move</v-icon>
    </v-btn>
    <v-btn
      icon
      @click="tool = 'pencil'"
      :class="'color-picker-toggle ' + (tool === 'pencil' ? 'active' : '')"
    >
      <v-icon>mdi-pencil</v-icon>
    </v-btn>
  </div>
</template>

<script>
export default {
  name: "RightAlignedColorPicker",
  data() {
    return {
      tool: "cursor",
    };
  },
  emits: ["toolChange"],
};
</script>

<style scoped>
.actions {
  padding: 10px;
  display: flex;
  gap: 10px;
}

button.color-picker-toggle.active {
  background-color: #afafaf;
}
</style>
