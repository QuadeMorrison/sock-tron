<template lang="pug">
  canvas#game_window(:width=`this.window.width + "px"` 
                     :height=`this.window.height + "px"` 
                     ref="game_window")
</template>

<script>
import keys from "../keys.js"

export default {
  name: 'tron',
  data () {
    return { 
      context: null,
      position: { x: 0, y: 0 },
      window: { height: 500, width: 500 },
      player: { height: 10, width: 10 }
    }
  },
  sockets: {
    connect() {
      console.log("Connected to server")
      this.$socket.emit("init_game", this.window, this.player)

      // init canvas
      this.context = this.$refs.game_window.getContext("2d")
    },
    update_position(position) {
      this.position = position
      this.draw_player()
    }
  },
  methods: {
    key_handler(e) {
      let key = keys[e.which]
      if (key) this.$socket.emit('keydown', key, this.position)
    },
    draw_player() {
      this.context.fillRect(this.position.x, this.position.y, 10, 10)
    }
  },
  mounted() {
    // Vue's keydown event only really works for input elements
    // so we have to bind the event the old fashioned way
    window.addEventListener('keydown', this.key_handler)  
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
#game_window {
  border: black solid 1px;
}
</style>
