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

      <!-- Username Form -->
      <UsernameForm />

      <!-- The place -->
      <ThePlace />

      <!-- App messenger -->
      <AppMessenger />
    </v-main>
  </v-app>
</template>

<style>
body,
html {
  margin: 0;
  padding: 0;
  font-family: "Roboto", sans-serif;
  background-color: #222222;
}
#bar {
  position: absolute;
  background-color: white;
  padding: 10px 20px 10px 10px;
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
</style>
