<template lang="pug">
  div
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
      position: null,
      background: 'black',
      num: 0,
      window: { height: 500, width: 500 },
      player: { height: 10, width: 10 }
    }
  },
  sockets: {
    connect() {
      console.log("Connected to server")
      if (this.context) {
        //this.context.clearRect(0, 0, this.window.width, this.window.height);
      }
    },
    init_settings(settings) {
      console.log('test')
      this.window = settings.window
      this.window.width *= 10
      this.window.height *= 10
      this.player = {}
      this.player.width = 10
      this.player.height = 10
      this.context = this.$refs.game_window.getContext("2d")
    },
    move_player(position) {
      this.position = position
      this.draw_player()
    }
  },
  methods: {
    key_handler(e) {
      let key = keys[e.which]
      if (key) this.$socket.emit('keydown', key)
      this.max_width 
    },
    draw_player() {
      Object.keys(this.position).forEach(x => {
        if (!isNaN(x)) {
          this.position[x].forEach(y => {
            this.context.fillStyle = this.position.color
            this.context.fillRect(x*10, y*10, this.player.height, this.player.width)
          })
        }
      })
    }
  },
  mounted() {
    // Vue's keydown event only really works for input elements
    // so we have to bind the event the old fashioned way
    window.addEventListener('keydown', this.key_handler)  
  },
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
#game_window {
  border: white solid 1px;
  background: #111;
}
</style>
