<template lang="pug">
  div
    canvas#game_window(:width=`this.win_w + "px"` 
                     :height=`this.win_h + "px"` 
                     ref="game_window")
</template>

<script>
import keys from "../keys.js"

export default {
  name: 'tron',
  data () {
    return { 
      ctx: null,
		canv_players: [],
		grid_w: 0, grid_h: 0,
		win_w: 0,  win_h: 0,
		grid: 10,  pl_dim: 8,
    }
  },
  sockets: {
    connect() {
      console.log("Connected to server")
      // Mainly just for testing, enter the main room when you connect.
      this.$socket.emit('enter_room')
    },
    init_settings(settings) {
		// consistent naming :)
		this.grid   = settings.grid;
		this.grid_w = settings.grid_w;
		this.grid_h = settings.grid_h;

		this.win_w = this.grid_w * this.grid;
		this.win_h = this.grid_h * this.grid;

      this.ctx = this.$refs.game_window.getContext("2d")
    },
    update_players(players) {
		// Add the new point to the path.
		players.forEach(pl => {
		  let c_pl = this.canv_players[pl["num"]];
		  // Don't need to draw a line if not alive.
		  if (pl["alive"]) {
			 c_pl["path"].lineTo(this.grid_to_win(pl.x), this.grid_to_win(pl.y));
		  }
		});

		this.draw_reset();
		this.draw_grid();
		this.draw_loop(players);
    },
    start_game(players) {
		console.log("PL: ", players);

		players.forEach(pl => {
		  let c_pl = {};
		  let path = new Path2D();
		  path.moveTo(this.grid_to_win(pl.x), this.grid_to_win(pl.y));

		  c_pl["path"] = path;
		  c_pl["color"] = pl["color"];
		  this.canv_players[pl["num"]] = c_pl;
		});

		console.log("players: ", this.canv_players);
    }
  },
  methods: {
	 grid_to_win(c) {
		return c * this.grid-this.grid/2;
	 },
	 draw_grid() {
		this.ctx.save();

		this.ctx.strokeStyle = "rgba(100, 100, 100, .2)";
		//this.ctx.setLineDash([5, 2.5]);
		//this.ctx.lineDashOffset = 5;
		this.ctx.lineWidth = 2;

		this.ctx.beginPath();
		for (let i = 0; i < this.grid_w; i++) {
		  let x = i * this.grid;
		  this.ctx.moveTo(x, 0);
		  this.ctx.lineTo(x, this.win_h);
		}
		this.ctx.closePath();
		this.ctx.stroke();

		this.ctx.beginPath();
		for (let i = 0; i < this.grid_h; i++) {
		  let y = i * this.grid;
		  this.ctx.moveTo(0,          y);
		  this.ctx.lineTo(this.win_w, y);
		}
		this.ctx.closePath();
		this.ctx.stroke();

		this.ctx.restore();
	 },
	 draw_reset() {
		this.ctx.save();
		this.ctx.clearRect(0, 0, this.win_w, this.win_h);
		this.ctx.restore();
	 },
	 draw_loop(players) {
		this.ctx.save();

		// shadow
		this.ctx.shadowOffsetX = 0;
		this.ctx.shadowOffsetY = 0;
		this.ctx.shadowBlur = 3;
		this.ctx.shadowColor = '#000';

		// line style
		this.ctx.lineCap = 'round';
		this.ctx.lineJoin = 'miter';
		this.ctx.lineWidth = this.pl_dim; // was:   this.player.width;

		// draw it!
		this.canv_players.forEach((pl) => {
		  this.ctx.strokeStyle = pl["color"];
		  this.ctx.stroke(pl["path"]);
		});

		this.ctx.restore();
	 },
    key_handler(e) {
      let key = keys[e.which]
      if (key) this.$socket.emit('keydown', key)
    },
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
