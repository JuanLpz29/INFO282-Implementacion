<script setup>
// This starter template is using Vue 3 <script setup> SFCs
// Check out https://v3.vuejs.org/api/sfc-script-setup.html#sfc-script-setup
import HelloWorld from "./components/lol/HelloWorld.vue";
import MenuVue from "./components/lol/Menu.vue";
import LayoutOne from "./layouts/LayoutOne.vue";
</script>

<template>
  <div class="xdd">
    <!-- <img alt="Vue logo" src="./assets/logo.png" /> -->
    <!-- <HelloWorld msg="Hello Vue 3 + Vite" /> -->
    <layout-one />
    <!-- <menu-vue/> -->
  </div>
</template>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #19392cff;

  margin-top: 10px;
}
.xdd {
  content: "";
  background-image: url("./assets/nn2.png");
  background-color: #bdbdbd;
  background-repeat: no-repeat;
  background-size: cover;
  /* background: rgb(192, 248, 231);
  background: linear-gradient(
    90deg,
    rgba(192, 248, 231, 1) 32%,
    rgba(100, 182, 194, 1) 100%
  ); */
}

.q-page {
  min-height: 0px;
}

.chido {
  color: #afd8ca;
  /* -webkit-text-stroke: 0.5px white; */
}
.color1 {
  background-color: #64b6c2ff;
}
.color2 {
  background-color: #588798ff;
}
.color3 {
  background-color: #c0f8e7ff;
}
.color4 {
  background-color: #19392cff;
}
.color5 {
  background-color: #c0f8e7ff;
}

.texto {
  color: black;
}
</style>
