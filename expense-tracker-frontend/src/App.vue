<template>
  <div id="app">
    <div class="container">
      <app-main></app-main>
    </div>
  </div>
</template>

<script>
import Main from './components/Main'
export default {
  name: 'App',
  components: {
    'app-main': Main
  },
  created() {
    this.$store.dispatch('tryAutoLogin')
  }
}
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
