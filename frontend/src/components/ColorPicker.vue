<template>
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
  emits: ["colorChange"],
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
.color-picker-container {
  width: 300px;
  box-shadow: 0px 2px 10px rgba(0, 0, 0, 0.2); /* Optional: shadow */
}
</style>
