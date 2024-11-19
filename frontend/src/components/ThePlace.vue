<template>
  <!-- vuetify Loading animation -->
  <div v-if="loadingPlace" id="loading">
    <v-progress-circular indeterminate color="primary"></v-progress-circular>
  </div>

  <!-- Color picker -->
  <div id="tools">
    <ToolPicker
      @toolChange="(tool) => (selectedTool = tool)"
      @home="centerCamera"
    />

    <Transition name="fade">
      <ColorPicker
        v-if="selectedTool === 'pencil' || selectedTool === 'eyedropper'"
        :colorIn="selectedColor"
        @colorChange="(col) => (selectedColor = col)"
      />
    </Transition>

    <Transition name="fade">
      <ColorPalette
        v-if="selectedTool === 'pencil' || selectedTool === 'eyedropper'"
        :color="selectedColor"
        @colorSelected="(col) => (selectedColor = col)"
      />
    </Transition>
  </div>

  <!-- Username Display -->
  <UsernameDisplay :username="focusedCellUsername" />

  <div id="grid"></div>
</template>

<script>
import axios from "axios";
import { mapStores } from "pinia";
import messagesStore from "@/store/messages";
import appStore from "@/store/app";
import Phaser from "phaser";
import ColorPicker from "./ColorPicker.vue";
import ColorPalette from "./ColorPalette.vue";

const placeUpdateEventName = "newPixelUpdate";
const gridWidth = 30;
const gridHeight = 30;

export default {
  name: "ThePlace",
  data() {
    return {
      isTrue: true,
      loadingPlace: true,
      loadingPlacement: false,

      place: null,
      cells: null,
      camera: null,
      selectedColor: "#000000",
      selectedTool: "cursor",
      previouslySelectedPixel: null,
      focusedCellUsername: null,
    };
  },
  mounted() {
    // Get the place from the server
    this.getPlace();

    // Listen for websocket updates
    this.$websocket.onMessage(placeUpdateEventName, (newSquare) => {
      // Update the pixel
      this.updatePixel(newSquare);
    });
  },
  methods: {
    getPlace() {
      const url = "/api/place";

      axios
        .get(url)
        .then((response) => {
          this.place = response.data;
          this.displayGrid();
        })
        .catch((error) => {
          console.log("Error loading place");
          console.log(error);
          this.messagesStore.addMessage({
            type: "error",
            message: "Error loading place :'(",
          });
        });
    },

    displayGrid() {
      if (!this.place) return;

      const config = {
        parent: "grid",
        type: Phaser.AUTO,
        width: window.innerWidth, // Full width
        height: window.innerHeight, // Full height
        backgroundColor: "#222222",
        scene: {
          preload: preload,
          create: create,
          update: update,
        },
        physics: {
          default: "arcade",
          arcade: {
            debug: false,
          },
        },
      };

      const game = new Phaser.Game(config);

      const place = this.place;
      const cells = [];
      let camera;

      const hoverOnPixel = (cell, x, y) => {
        // Highlight the cell
        if (
          this.selectedTool === "pencil" ||
          this.selectedTool === "eyedropper"
        )
          cell.setStrokeStyle(4, 0xaaaaaa);

        // Show username
        const username = place.pixels[x][y].username;
        this.focusedCellUsername = username;
      };
      const hoverOutPixel = (cell) => {
        if (
          this.selectedTool === "pencil" ||
          this.selectedTool === "eyedropper"
        )
          cell.setStrokeStyle(0);
      };
      const selectPixel = (x, y) => {
        // Prevent selecting the same pixel multiple times
        if (
          this.previouslySelectedPixel &&
          this.previouslySelectedPixel.x === x &&
          this.previouslySelectedPixel.y === y
        )
          return;

        this.previouslySelectedPixel = { x, y };

        if (this.selectedTool === "pencil" && !this.loadingPlacement) {
          // Draw pixel
          const url = "/api/place";
          const data = {
            username: this.appStore.username,
            x,
            y,
            color: this.selectedColor,
          };
          this.loadingPlacement = true;
          axios
            .post(url, data)
            .then((response) => {})
            .catch((error) => {})
            .finally(() => {
              this.loadingPlacement = false;
            });
        } else if (this.selectedTool === "eyedropper") {
          // Get pixel color
          const pixel = place.pixels[x][y];
          this.selectedColor = pixel.color;
        }
      };
      const drag = (startX, startY, x, y) => {
        if (!this.camera) return;
        if (this.selectedTool !== "cursor") return;
        this.camera.scrollX = startX - x;
        this.camera.scrollY = startY - y;
      };
      const selectNone = () => {
        this.previouslySelectedPixel = null;
        this.focusedCellUsername = null;
      };
      function preload() {}
      function create() {
        const cellSize = 30;

        for (let x = 0; x < gridWidth; x++) {
          for (let y = 0; y < gridHeight; y++) {
            const cell = this.add
              .rectangle(
                x * cellSize,
                y * cellSize,
                cellSize,
                cellSize,
                Phaser.Display.Color.HexStringToColor(place.pixels[x][y].color)
                  .color,
              )
              .setOrigin(0);

            cell.setInteractive();

            cell.on("pointerdown", () => selectPixel(x, y));

            cell.on("pointerover", () => hoverOnPixel(cell, x, y));

            cell.on("pointerout", () => hoverOutPixel(cell));

            cell.on("pointermove", (pointer) => {
              if (pointer.isDown) {
                selectPixel(x, y);
              }
            });

            cells.push(cell);
          }
        }

        const gridContainer = this.add.container(0, 0, cells);
        gridContainer.setSize(gridWidth * cellSize, gridHeight * cellSize);
        gridContainer.setInteractive();
        gridContainer.on("pointerover", () => selectNone());

        // Set up camera
        camera = this.cameras.main;
        camera.zoom = 0.5;

        // Enable dragging with pointer
        let isDragging = false;
        let startDragX = 0;
        let startDragY = 0;

        this.input.on("pointerdown", (pointer) => {
          isDragging = true;
          startDragX = pointer.x + camera.scrollX;
          startDragY = pointer.y + camera.scrollY;
        });

        this.input.on("pointermove", (pointer) => {
          if (isDragging) {
            drag(startDragX, startDragY, pointer.x, pointer.y);
          }
        });

        this.input.on("pointerup", () => {
          isDragging = false;
        });

        // Zoom with the mouse wheel
        this.input.on("wheel", (pointer, gameObjects, deltaX, deltaY) => {
          camera.zoom += deltaY > 0 ? -0.025 : 0.025;
          camera.zoom = Phaser.Math.Clamp(camera.zoom, 0.1, 4);
        });

        // Set up arrow keys for movement
        this.cursors = this.input.keyboard.createCursorKeys();
      }
      function update() {
        const speed = 15;

        // Apply movement
        if (this.cursors.left.isDown) {
          this.camera.scrollX -= speed;
        } else if (this.cursors.right.isDown) {
          this.camera.scrollX += speed;
        }

        if (this.cursors.up.isDown) {
          this.camera.scrollY -= speed;
        } else if (this.cursors.down.isDown) {
          this.camera.scrollY += speed;
        }
      }

      this.cells = cells;

      // Wait for game created event
      game.events.on("ready", () => {
        this.loadingPlace = false;
        this.camera = camera;
        this.centerCamera();
      });

      // Resize the game when the window resizes
      window.addEventListener("resize", () => {
        game.scale.resize(window.innerWidth, window.innerHeight);
        this.centerCamera();
      });
    },
    updatePixel(pixel) {
      const { x, y, color, username } = pixel;

      // Update the phaser grid
      const cellNumber = x * gridWidth + y;
      if (this.cells && this.cells[cellNumber]) {
        const cell = this.cells[cellNumber];
        cell.fillColor = Phaser.Display.Color.HexStringToColor(color).color;
      } else {
        console.log(`Cell at (${x}, ${y}) not found`);
      }

      // Update the place data
      this.place.pixels[x][y].color = color;
      this.place.pixels[x][y].username = username;
    },
    centerCamera() {
      // Center the camera
      if (this.camera && this.place) {
        const gridWidth = this.place.pixels.length; // Number of columns
        const gridHeight = this.place.pixels[0].length; // Number of rows
        const cellSize = 30; // Ensure this matches your cell size

        const centerX = (gridWidth * cellSize) / 2 - this.camera.width / 2;
        const centerY =
          (gridHeight * cellSize) / 2 - this.camera.height / 2 - 30;

        this.camera.scrollX = centerX;
        this.camera.scrollY = centerY;
        this.camera.zoom = 0.9;
      } else {
        console.log("Camera or place not found");
      }
    },
  },
  computed: {
    ...mapStores(messagesStore),
    ...mapStores(appStore),
  },
  watch: {
    selectedTool(newTool) {
      this.focusedCellUsername = null;
      this.previouslySelectedPixel = null;
    },
    selectedColor(newColor) {
      this.focusedCellUsername = null;
      this.previouslySelectedPixel = null;
    },
  },
  beforeUnmount() {
    this.$websocket.offMessage(placeUpdateEventName);
  },
};
</script>

<style lang="css">
#grid {
  margin: 0 auto;
  height: 100vh !important;
  width: 100vw !important;
  overflow: hidden !important;
}

#loading {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
}

#tools {
  position: absolute;
  top: 0;
  left: 100%;
  transform: translate(-100%, 0%);
  padding: 10px;
  gap: 10px;
}
</style>
