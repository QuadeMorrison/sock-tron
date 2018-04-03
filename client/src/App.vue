<template lang="pug">
  div(id="app")
    audio(autoplay)
      source(src="/static/heroic_demise.mp3" type="audio/mpeg")
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
  display: grid;
}

html {
  min-width: 100%;
  min-height: 100%;
  display: grid;
  background: #001100;
}

#app {
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: white;
}
</style>
