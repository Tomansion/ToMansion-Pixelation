import { defineStore } from "pinia";

const useAppStore = defineStore("app", {
  state: () => ({
    session: null,
    username: null,
  }),
  actions: {
    setSession(data) {
      this.session = data;
    },
    setUsername(data) {
      this.username = data;
      console.log("Username set to", this.username);
    },
  },
});

export default useAppStore;
