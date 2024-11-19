<template>
  <v-container>
    <div class="color-picker-container">
      <v-color-picker
        v-model="color"
        mode="rgba"
        hide-mode-switch
        flat
        show-swatches
      ></v-color-picker>
    </div>
  </v-container>
</template>

<script>
export default {
  name: "RightAlignedColorPicker",
  data() {
    return {
      color: "#ffffff", // Default color
    };
  },
  props: {
    colorIn: {
      type: String,
      required: true,
    },
  },
  watch: {
    color(newColor) {
      // Emit the color change event
      this.$emit("colorChange", newColor);
    },
    colorIn(newColor) {
      if (newColor !== this.color) this.color = newColor;
    },
  },
};
</script>

<style scoped>
.color-picker-container {
  position: absolute;
  top: 40%;
  right: 0;
  transform: translateY(-50%);
  width: 300px;
  z-index: 1000; /* Ensure it stays on top */
  box-shadow: 0px 2px 10px rgba(0, 0, 0, 0.2); /* Optional: shadow */
}
</style>
