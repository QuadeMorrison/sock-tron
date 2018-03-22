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
      pl_x: 0,
      pl_y: 0,
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
      this.window = settings.window
      this.window.width *= 10
      this.window.height *= 10
      this.player = {}
      this.player.width = 10
      this.player.height = 10
      this.context = this.$refs.game_window.getContext("2d")
    },
    update_players(players) {
      // In the future, we don't want drawing events here, to make it nice and smooth.
      this.draw_players(players)
    }
  },
  methods: {
    key_handler(e) {
      let key = keys[e.which]
      if (key) this.$socket.emit('keydown', key)
      this.max_width 
    },
    draw_players(players) {
      for (let i = 0; i < players.length; i++) {
        let pl = players[i]
        if (pl.alive) {
          this.context.fillStyle = pl.color
          this.context.fillRect(pl.x*10, pl.y*10, this.player.height, this.player.width)
        }
      }

      // I'm keeping this line for reference. I always forget my javascript.
      // Object.keys(this.position).forEach(x => { if (!isNaN(x)) { this.position[x].forEach(y => { }) } })
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
