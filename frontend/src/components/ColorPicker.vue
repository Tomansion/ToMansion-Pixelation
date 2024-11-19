<template>
  <div class="color-picker-container">
    <v-color-picker
      v-model="color"
      mode="rgb"
      show-swatches
      :swatches="swatches"
      :swatches-max-height="isOnMobile ? 200 : 300"
      :hide-canvas="isOnMobile"
      :hide-inputs="isOnMobile"
      :hide-mode-switch="isOnMobile"
      :hide-sliders="isOnMobile"
    ></v-color-picker>
  </div>
</template>

<script>
export default {
  name: "RightAlignedColorPicker",
  data() {
    return {
      color: "#ffffff", // Default color
      swatches: [
        [
          "#6d001a",
          "#be0039",
          "#ff4500",
          "#ffa800",
          "#ffd635",
          "#fff8b8",
          "#00a368",
          "#00cc78",
        ],
        [
          "#7eed56",
          "#00756f",
          "#009eaa",
          "#00ccc0",
          "#51e9f4",
          "#3690ea",
          "#2450a4",
          "#493ac1",
        ],
        [
          "#6a5cff",
          "#94b3ff",
          "#811e9f",
          "#b44ac0",
          "#e4abff",
          "#ff99aa",
          "#ff3881",
          "#de107f",
        ],
        [
          "#6d482f",
          "#9c6926",
          "#ffb470",
          "#000000",
          "#515252",
          "#898d90",
          "#d4d7d9",
          "#ffffff",
        ],
      ],
      waitEvent: null,
      windowWidth: window.innerWidth,
    };
  },
  props: {
    colorIn: {
      type: String,
      required: true,
    },
  },
  emits: ["colorChange"],
  mounted() {
    window.addEventListener("resize", this.handleResize);
  },
  methods: {
    colorOut(newColor) {
      this.$emit("colorChange", newColor);
    },
    handleResize() {
      this.windowWidth = window.innerWidth;
    },
  },
  computed: {
    isOnMobile() {
      return this.windowWidth < 800;
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

  beforeUnmount() {
    window.removeEventListener("resize", this.handleResize);
  },
};
</script>

<style scoped>
.color-picker-container {
  width: 300px;
  box-shadow: 0px 2px 10px rgba(0, 0, 0, 0.2); /* Optional: shadow */
}
</style>
