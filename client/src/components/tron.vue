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
      ctx: null,
      canvas: null,
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
      if (this.ctx) {
        //this.ctx.clearRect(0, 0, this.window.width, this.window.height);
      }
      // Mainly just for testing, enter the main room when you connect.
      this.$socket.emit('enter_room', "main_room")
    },
    init_settings(settings) {
      this.window = settings.window
      this.window.width *= 10
      this.window.height *= 10

      this.player = {}
      this.player.width = 10
      this.player.height = 10
      this.ctx = this.$refs.game_window.getContext("2d")
		this.draw_loop();
    },
    update_players(players) {
      // In the future, we don't want drawing events here, to make it nice and smooth.

      this.draw_players(players)
    }
  },
  methods: {
	 init_draw() {

	 },
	 animation_loop() {


	 },
	 draw_loop() {
		this.ctx.save();
		this.ctx.clearRect(0, 0, this.window.width, this.window.height);

		// shadow
		this.ctx.shadowOffsetX = 1;
		this.ctx.shadowOffsetY = 1;
		this.ctx.shadowBlur = 5;
		this.ctx.shadowColor = 'black';

		// line style
		this.ctx.lineCap = 'round';
		this.ctx.lineJoin = 'round';
		this.ctx.lineWidth = this.player.width;

		var tron = new Path2D();
		tron.moveTo(20, 100);
		tron.lineTo(90, 100);
		tron.lineTo(90, 70);
		tron.lineTo(120, 70);
		tron.lineTo(120, 60);
		tron.lineTo(30, 60);

		// color
		this.ctx.strokeStyle = 'red'

		// draw it!
		this.ctx.stroke(tron);

		this.ctx.restore();
	 },
    key_handler(e) {
      let key = keys[e.which]
      if (key) this.$socket.emit('keydown', key)
    },
    draw_players(players) {
      for (let i = 0; i < players.length; i++) {
        let pl = players[i]
        if (pl.alive) {
          this.ctx.fillStyle = pl.color
          this.ctx.fillRect(pl.x*10, pl.y*10, this.player.height, this.player.width)
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
