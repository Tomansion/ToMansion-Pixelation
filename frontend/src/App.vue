<script setup lang="ts"></script>

<template>
  <v-app>
    <v-main>
      <!-- App bar -->
      <div id="bar">
        <v-icon>mdi-square-opacity</v-icon>
        <a
          href="https://github.com/Tomansion/ToMansion-Pixelation"
          target="_blank"
          >ToMansion Pixelation - Yet Another r/Place clone</a
        >
      </div>

      <!-- Username displayer -->
      <div id="username" v-show="appStore.username">
        {{ appStore.username }}
      </div>

      <!-- Username Form -->
      <UsernameForm />

      <!-- The place -->
      <ThePlace />

      <!-- App messenger -->
      <AppMessenger />
    </v-main>
  </v-app>
</template>

<script>
import UsernameForm from "@/components/UsernameForm.vue";
import ThePlace from "@/components/ThePlace.vue";
import AppMessenger from "@/components/AppMessenger.vue";
import { mapStores } from "pinia";
import appStore from "@/store/app";

export default {
  computed: {
    ...mapStores(appStore, ["username"]),
  },
};
</script>

<style scoped>
body,
html {
  margin: 0;
  padding: 0;
  font-family: "Roboto", sans-serif;
  background-color: #222222;

  height: 100vh !important;
  width: 100vw !important;
  overflow: hidden !important;
}
#bar {
  position: absolute;
  background-color: white;
  padding: 10px 20px 10px 10px;
  top: 10px;
  margin: 10px;
  border-radius: 5px;
  font-size: 20px;
  display: flex;
  gap: 10px;
  box-shadow: 0px 2px 10px rgba(0, 0, 0, 0.2);
}

#bar a {
  color: black;
  text-decoration: none;
}

#username {
  position: absolute;
  top: 53px;
  background-color: white;
  padding: 5px 10px;
  margin: 10px;
  border-radius: 5px;
  min-width: 60px;
  height: 30px;
}
</style>
