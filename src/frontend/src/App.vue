<template>
  <!-- <div id="app">
    <div id="nav">
      <router-link to="/">Home</router-link> |
      <router-link to="/about">About</router-link>
    </div>
    <router-view />
  </div> -->
  <v-app>
    
    <v-main class="align-content-start">
      <app-bar></app-bar>
      <app-navigation></app-navigation>
      <router-view transition="slide-x-transition"></router-view>
    </v-main>
  </v-app>
</template>

<script>
import AppNavigation from '@/components/AppNavigation';
import AppBar from '@/components/AppBar';
export default {
  name: 'App',
  components: {
    AppNavigation,
    AppBar
  }
};
</script>

<style>/*
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: start;
  color: #2c3e50;
}
* {
  box-sizing: border-box;
}
html {
  font-family: sans-serif;
}
body {
  margin: 0;
}
section {
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.26);
  margin: auto auto;
  max-width: 100rem;
  padding: 0.1rem;
  border-radius: 12px;
}*/

</style>
