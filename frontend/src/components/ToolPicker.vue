<template>
  <div class="actions">
    <v-btn
      icon
      @click="tool = 'cursor'"
      :class="'toolToggle ' + (tool === 'cursor' ? 'active' : '')"
    >
      <v-icon>mdi-cursor-move</v-icon>
    </v-btn>
    <v-btn
      icon
      @click="tool = 'pencil'"
      :class="'toolToggle ' + (tool === 'pencil' ? 'active' : '')"
    >
      <v-icon>mdi-pencil</v-icon>
    </v-btn>
    <v-btn
      icon
      @click="tool = 'eyedropper'"
      :class="'toolToggle ' + (tool === 'eyedropper' ? 'active' : '')"
    >
      <v-icon>mdi-eyedropper</v-icon>
    </v-btn>
    <v-btn icon @click="$emit('home')">
      <v-icon>mdi-home</v-icon>
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
  watch: {
    tool(newTool) {
      this.$emit("toolChange", newTool);
    },
  },
};
</script>

<style scoped>
.actions {
  padding: 10px;
  display: flex;
  gap: 10px;
  width: 300px;
}

button.toolToggle.active {
  background-color: #afafaf;
}
</style>
