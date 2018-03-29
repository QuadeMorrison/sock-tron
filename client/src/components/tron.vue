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
		win_w: 500,  win_h: 500,
		grid: 10,  pl_dim: 8,
		win_list: null, FPS: 30,
		count_down: 0, searching: false,
		recv_delta: 0, last_time: (new Date()).getTime(),
		delta_inc: 0, frame_delta: 0
    }
  },
  created: function() {
	 window.setInterval(this.draw, 1000 / this.FPS)
  },
  sockets: {
    connect() {
      console.log("Connected to server")
      // Mainly just for testing, enter the main room when you connect.
      this.$socket.emit('enter_room')
    },
	 game_over(players) {
		this.win_list = players;
		this.delta_inc = 0;
		this.frame_delta = 0;
	 },
	 game_starts_in(count_down) {
		this.count_down = count_down;
	 },
    init_settings(settings) {
		// consistent naming
		this.grid   = settings.grid;
		this.grid_w = settings.grid_w;
		this.grid_h = settings.grid_h;

		this.win_w = this.grid_w * this.grid;
		this.win_h = this.grid_h * this.grid;

      this.ctx = this.$refs.game_window.getContext("2d")
    },
    update_players(players) {
		// Figure out time difference.
		let cur_time = (new Date()).getTime();
		this.recv_delta = cur_time - this.last_time;
		this.delta_inc = 1000 / this.FPS / this.recv_delta;
		this.frame_delta = 0;
		this.last_time = cur_time;

		// Add the new point to the path.
		players.forEach(pl => {
		  let c_pl = this.canv_players[pl["num"]];

		  // Don't need to draw a line if not alive.
		  if (c_pl.alive) {
			 c_pl.cur_x = c_pl.next_x;
			 c_pl.cur_y = c_pl.next_y;
			 c_pl["path"].lineTo(c_pl.next_x, c_pl.next_y);
			 c_pl.next_x = this.grid_to_win(pl.x);
			 c_pl.next_y = this.grid_to_win(pl.y);
		  }

		  c_pl.alive = pl["alive"]
		});
    },
	 searching_for_players() {
		this.searching = true;
	 },
    start_game(players) {
		this.count_down = 0;
		this.searching = false;

		players.forEach(pl => {
		  let c_pl = {};
		  c_pl.color = pl["color"];
		  c_pl.next_x = this.grid_to_win(pl.x);
		  c_pl.next_y = this.grid_to_win(pl.y);
		  c_pl.cur_x = c_pl.next_x;
		  c_pl.cur_y = c_pl.next_y;
		  c_pl.alive = pl.alive

		  let path = new Path2D();
		  path.moveTo(c_pl.next_x, c_pl.next_y);
		  c_pl.path = path;

		  this.canv_players[pl["num"]] = c_pl;
		});
    }
  },
  methods: {
	 grid_to_win(c) {
		return c * this.grid-this.grid/2;
	 },
	 draw() {
		this.draw_reset();
		this.draw_grid();
		this.draw_players();
		if (this.count_down > 0) { this.draw_count_down(); }
		else if (this.win_list != null) { this.draw_win(); }
		else if (this.searching) { this.draw_text("Locating Socks..."); }
	 },
	 // Draws text centered.
	 draw_text(text, color) {
		if (!color) {
		  color = "white";
		}
		let size = 60
		this.ctx.save();
		this.ctx.font = size + 'px sans-serif';

		let tm = this.ctx.measureText(text);
		let tx = this.win_w/2 - tm.width/2;

		this.ctx.shadowOffsetX = 0;
		this.ctx.shadowOffsetY = 0;
		this.ctx.shadowBlur = 10;
		this.ctx.shadowColor = 'black';
		this.ctx.fillStyle = color;

		this.ctx.fillText(text, tx, this.win_h/2);
		this.ctx.restore();
	 },
	 draw_count_down() {
		this.draw_text(this.count_down.toString());
	 },
	 draw_win() {
		// First, get the length.
		let color = "white";
		let end_text = " Wins!";
		if (this.win_list.length > 1) {
		  end_text = " Win!";
		} else {
		  color = this.win_list[0]["color"];
		}

		let name_list = this.win_list.map((pl) => pl.num)
		let text = name_list.join(" & ") + end_text;
		this.draw_text(text, color);
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
	 draw_players() {
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
		  let path = pl["path"]

		  // If we are playing the game, then guess the next position.
		  if (pl.alive && this.win_list == null) {
			 path = new Path2D(path);
			 let x = (pl.next_x - pl.cur_x)*this.frame_delta;
			 let y = (pl.next_y - pl.cur_y)*this.frame_delta;
		  
			 path.lineTo(pl.cur_x + x, pl.cur_y + y)
		  }
		  this.ctx.stroke(path);
		});
		
		this.frame_delta += this.delta_inc;
		if (this.frame_delta > 1) {
		  this.frame_delta = 1
		}
		console.log(this.frame_delta, this.delta_inc, this.recv_delta)

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
