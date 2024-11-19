<template>
  <!-- vuetify Loading animation -->
  <div v-if="loadingPlace" id="loading">
    <v-progress-circular indeterminate color="primary"></v-progress-circular>
  </div>

  <!-- Color picker -->
  <div id="tools">
    <ToolPicker @toolChange="(tool) => (selectedTool = tool)" />

    <ColorPicker
      :colorIn="selectedColor"
      @colorChange="(col) => (selectedColor = col)"
    />
    <ColorPalette
      :color="selectedColor"
      @colorSelected="(col) => (selectedColor = col)"
    />
  </div>

  <div id="grid"></div>
</template>

<script>
import axios from "axios";
import { mapStores } from "pinia";
import messagesStore from "@/store/messages";
import Phaser from "phaser";
import ColorPicker from "./ColorPicker.vue";
import ColorPalette from "./ColorPalette.vue";

const placeUpdateEventName = "newPixelUpdate";

export default {
  name: "ThePlace",
  data() {
    return {
      isTrue: true,
      loadingPlace: true,

      place: null,
      game: null,
      cells: null,
      selectedColor: "#ffffff",
      selectedTool: "",
    };
  },
  mounted() {
    // Get the place from the server
    this.getPlace();

    // Listen for websocket updates
    this.$websocket.onMessage(placeUpdateEventName, (newSquare) => {
      console.log("Received place update", newSquare);
      console.log(this.game);
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

      this.game = new Phaser.Game(config);

      let camera;
      const place = this.place;
      const cells = [];

      const drawPixel = (x, y) => {
        const url = "/api/place";
        const data = {
          username: "test",
          x,
          y,
          color: this.selectedColor,
        };

        axios
          .post(url, data)
          .then((response) => {
            console.log("Successfully posted pixel");
          })
          .catch((error) => {
            console.log("Error posting pixel");
            console.log(error);
          });
      };
      function preload() {}
      function create() {
        const gridWidth = 100;
        const gridHeight = 100;
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

            cell.on("pointerover", () => {
              cell.setStrokeStyle(4, 0xaaaaaa);
            });

            cell.on("pointerout", () => {
              cell.setStrokeStyle();
            });

            // Sent /post request on click on cell
            cell.on("pointerdown", () => {
              console.log("Clicked on cell", x, y);
              drawPixel(x, y);
            });

            cells.push(cell);
          }
        }

        const gridContainer = this.add.container(0, 0, cells);
        gridContainer.setSize(gridWidth * cellSize, gridHeight * cellSize);

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
            camera.scrollX = startDragX - pointer.x;
            camera.scrollY = startDragY - pointer.y;
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
          camera.scrollX -= speed;
        } else if (this.cursors.right.isDown) {
          camera.scrollX += speed;
        }

        if (this.cursors.up.isDown) {
          camera.scrollY -= speed;
        } else if (this.cursors.down.isDown) {
          camera.scrollY += speed;
        }
      }

      this.cells = cells;
      // Wait for game created event
      this.game.events.on("ready", () => {
        console.log("Game created");
        this.loadingPlace = false;
      });
    },
    updatePixel(pixel) {
      const { x, y, color } = pixel;
      const cellNumber = x * 100 + y;

      if (this.cells && this.cells[cellNumber]) {
        const cell = this.cells[cellNumber];
        cell.fillColor = Phaser.Display.Color.HexStringToColor(color).color;
      } else {
        console.log(`Cell at (${x}, ${y}) not found`);
      }
    },
  },
  computed: {
    ...mapStores(messagesStore),
  },
  beforeUnmount() {
    this.$websocket.offMessage(placeUpdateEventName);
  },
};
</script>

<style lang="css">
#grid {
  margin: 0 auto;
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
