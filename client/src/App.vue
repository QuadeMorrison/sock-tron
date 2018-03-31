<template lang="pug">
  div(id="app")
    router-view
</template>

<script>
export default {
  name: 'App'
}
</script>

<style>
body {
  background: #001100;
}

#app {
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: white;
  margin-top: 20px;
}
</style>
