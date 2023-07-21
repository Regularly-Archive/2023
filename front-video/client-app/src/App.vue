<template>
  <div id="app">
    <img alt="Vue logo" src="./assets/logo.png" />
    <header>
      <my-router-link to="/home">首页</my-router-link>
      -
      <my-router-link to="/generalVideo">普通视频</my-router-link>
      -
      <my-router-link to="/stramingVideo">流式视频</my-router-link>
      -
      <my-router-link to="/flvVideo">FLV视频</my-router-link>
    </header>
    <router-view />
  </div>
</template>

<script>
import MyRouterLink from "./components/MyRouterLink.vue";

export default {
  name: "App",
  components: {
    MyRouterLink,
  },
};
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}
</style>
