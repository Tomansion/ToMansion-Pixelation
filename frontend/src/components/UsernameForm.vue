<template>
  <v-dialog v-model="displayModal" max-width="500px" persistent>
    <!-- Set username form -->
    <v-form @submit.prevent>
      <v-card style="padding: 10px">
        <v-card-title
          >Tell us your Username <br> and start placing pixels</v-card-title
        >
        <v-card-text>
          <v-text-field
            v-model="newUsername"
            label="Username"
            outlined
            dense
            ref="usernameInput"
          />
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="primary" type="submit" @click="setUsername"
            >Join the place</v-btn
          >
        </v-card-actions>
      </v-card>
    </v-form>

    <!-- Error message -->
    <v-fade-transition>
      <v-alert
        v-if="errorMessage"
        type="error"
        dense
        dismissible
        class="mt-4"
        @click="errorMessage = ''"
      >
        {{ errorMessage }}
      </v-alert>
    </v-fade-transition>
  </v-dialog>
</template>

<script>
import { mapStores } from "pinia";
import messagesStore from "@/store/messages";
import appStore from "@/store/app";

export default {
  name: "UsernameForm",
  emits: ["usernameProvided"],
  data() {
    return {
      newUsername: "",
      isUsernameProvided: true,

      errorMessage: "",
      successMessage: "",
    };
  },

  mounted() {
    // Look for the username in local storage
    const username = localStorage.getItem("username");
    if (username && username.length > 0) {
      this.newUsername = username;
      this.setUsername();
    } else {
      this.newUsername = "";
      this.isUsernameProvided = false;

      // Wait for the next tick to focus the input
      this.$nextTick(() => {
        // Focus the username input is mounted and select the text
        this.$refs.usernameInput.focus();
        this.$refs.usernameInput.select();
      });
    }
  },
  methods: {
    setUsername() {
      // Validate the username field
      this.errorMessage = "";
      if (!this.newUsername) {
        this.errorMessage = "Please enter a username >:(";
        return;
      }

      // Save the username in local storage
      localStorage.setItem("username", this.newUsername);

      // Store the username in the app store
      this.appStore.setUsername(this.newUsername);

      // Emit the usernameProvided event
      this.$emit("usernameProvided");

      // Success message
      this.messagesStore.addMessage({
        type: "success",
        message: "Welcome to the place! " + this.newUsername + "!",
      });

      // Clear the error message
      this.errorMessage = "";

      // Clear the username field
      this.newUsername = "";
      this.isUsernameProvided = true;
    },
  },
  computed: {
    displayModal() {
      return !this.isUsernameProvided;
    },
    ...mapStores(messagesStore),
    ...mapStores(appStore),
  },
};
</script>
