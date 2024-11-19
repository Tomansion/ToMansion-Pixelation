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

  <div class="color-picker-container">
    <v-color-picker
      v-model="color"
      mode="rgba"
      hide-mode-switch
      flat
      show-swatches
    ></v-color-picker>
  </div>
</template>

<script>
export default {
  name: "RightAlignedColorPicker",
  data() {
    return {
      tool: "cursor",
      color: "#ffffff", // Default color
      waitEvent: null,
    };
  },
  props: {
    colorIn: {
      type: String,
      required: true,
    },
  },
  emits: ["colorChange", "toolChange"],
  methods: {
    colorOut(newColor) {
      this.$emit("colorChange", newColor);
    },
  },
  watch: {
    color(newColor) {
      // Emit the color change event
      // Wait for the user to stop changing the color
      clearTimeout(this.waitEvent);
      this.waitEvent = setTimeout(() => {
        this.colorOut(newColor);
      }, 300);
    },
    colorIn(newColor) {
      if (newColor !== this.color) this.color = newColor;
    },
  },
};
</script>

<style scoped>
.actions {
  padding: 10px;
  display: flex;
  gap: 10px;
}
.color-picker-container {
  width: 300px;
  box-shadow: 0px 2px 10px rgba(0, 0, 0, 0.2); /* Optional: shadow */
}

button.color-picker-toggle.active {
  background-color: #afafaf;
}
</style>
