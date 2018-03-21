<template lang="pug">
  div(id="app")
    h1 Sock Tron
    router-view
</template>

<script>
export default {
  name: 'App'
}
</script>

<style>
body {
  background: black;
}

#app {
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: white;
  margin-top: 60px;
}
</style>
