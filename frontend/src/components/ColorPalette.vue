<template>
  <v-container>
    <div class="palette-container">
      <div
        v-for="savedColor in savedColors"
        :key="savedColor"
        class="color-box"
        :style="{ backgroundColor: savedColor }"
        @click="selectColor(savedColor)"
      ></div>
    </div>
  </v-container>
</template>

<script>
export default {
  name: "ColorPalette",
  props: {
    color: {
      type: String,
      required: true,
    },
  },
  data() {
    return {
      savedColors: [],
    };
  },
  watch: {
    color(newColor) {
      this.addColor(newColor);
    },
  },
  mounted() {
    // this.loadSavedColors();
    this.addColor(this.color); // Add the initial prop color if not already in the palette
  },
  methods: {
    addColor(newColor) {
      const index = this.savedColors.indexOf(newColor);
      if (index !== -1) {
        // If color exists, move it to the top
        this.savedColors.splice(index, 1);
      }
      this.savedColors.unshift(newColor); // Add to the top
      this.saveToLocalStorage(); // Save updated palette
    },
    selectColor(color) {
      this.$emit("colorSelected", color);
    },
    loadSavedColors() {
      const storedColors = JSON.parse(
        localStorage.getItem("savedColors") || "[]",
      );
      this.savedColors = Array.isArray(storedColors) ? storedColors : [];
    },
    saveToLocalStorage() {
      localStorage.setItem("savedColors", JSON.stringify(this.savedColors));
    },
  },
};
</script>

<style scoped>
.palette-container {
  position: absolute;
  background: white;
  padding: 10px;
  border-radius: 5px;
  top: 70%;
  right: 0;
  transform: translateY(-50%);
  width: 300px;
  z-index: 1000; /* Ensure it stays on top */
  box-shadow: 0px 2px 10px rgba(0, 0, 0, 0.2); /* Optional: shadow */
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
  margin: 10px 0;
}

.color-box {
  width: 40px;
  height: 40px;
  border-radius: 5px;
  cursor: pointer;
  box-shadow: 0px 2px 5px rgba(0, 0, 0, 0.2);
  transition: transform 0.2s ease;
}

.color-box:hover {
  transform: scale(1.1);
}
</style>
