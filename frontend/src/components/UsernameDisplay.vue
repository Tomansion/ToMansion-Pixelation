<template>
  <transition name="move-up">
    <div id="username" v-show="username">
      {{ username }}
    </div>
  </transition>
</template>

<script>
export default {
  props: {
    username: {
      type: String,
    },
  },
};
</script>

<style lang="css">
#username {
  position: absolute;
  bottom: 10px;
  left: 0px;
  background-color: white;
  padding: 5px 10px;
  border-radius: 5px;
  min-width: 60px;
  height: 30px;
}

.move-up-enter-active,
.move-up-leave-active {
  transition:
    transform 1s,
    width 1s,
    height 1s;
}

.move-up-enter,
.move-up-leave-to {
  transform: translateY(130%) translateX(-50%);
}

.move-up-enter-to,
.move-up-leave {
  transform: translateY(0);
}
</style>
