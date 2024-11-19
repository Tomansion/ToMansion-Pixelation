<script setup lang="ts">
</script>

<template>
  <v-app>
    <v-main>
      <!-- App bar -->
      <div id="bar">
        <v-app-bar :elevation="2">
          <v-app-bar-title style="cursor: pointer">
            <v-icon>mdi-square-opacity</v-icon>
            ToMansion Pixelation - Yet Another r/Place clone
          </v-app-bar-title>
        </v-app-bar>
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
#bar {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
}
</style>
