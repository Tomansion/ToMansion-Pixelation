<template>
  <transition-group
    name="color-box-transition"
    tag="div"
    class="palette-container"
  >
    <div
      v-for="savedColor in savedColors"
      :key="savedColor"
      :class="'color-box ' + (savedColor === color ? 'selected' : '')"
      :style="{ backgroundColor: savedColor }"
      @click="selectColor(savedColor)"
    ></div>
  </transition-group>
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
    this.loadSavedColors();
    this.addColor(this.color); // Add the initial prop color if not already in the palette
  },
  methods: {
    addColor(newColor) {
      // Limit the number of saved colors to 10
      if (this.savedColors.length >= 11) {
        this.savedColors.pop(); // Remove the last color
      }
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
  border-radius: 4px;
  width: 300px;
  box-shadow: 0px 2px 10px rgba(0, 0, 0, 0.2); /* Optional: shadow */
  display: flex;
  flex-wrap: wrap;
  justify-content: flex-start;
  gap: 7px;
  margin: 10px 0;
  padding: 10px;
  background-color: white;
}

.color-box {
  width: 40px;
  height: 40px;
  border-radius: 5px;
  cursor: pointer;
  box-shadow: 0px 2px 5px rgba(0, 0, 0, 1);
  transition: transform 0.2s ease;
}

.color-box.selected {
  border: 2px solid black;
}

.color-box:hover {
  transform: scale(1.1);
}

.color-box-transition-enter-active,
.color-box-transition-leave-active {
  transition: all 0.3s;
}

.color-box-transition-enter,
.color-box-transition-leave-to {
  opacity: 0;
  transform: translateY(-20px);
}
</style>
