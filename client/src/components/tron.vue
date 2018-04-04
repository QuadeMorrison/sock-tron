<template lang="pug">
div(v-if="game_ready")
  canvas#game_window(:width=`this.win_w + "px"`
		:height=`this.win_h + "px"`
		  ref="game_window")
  div(v-show="win_list != null")
    pre.button.play_again(@click="play_button")
      | ██████╗ ██╗      █████╗ ██╗   ██╗     █████╗  ██████╗  █████╗ ██╗███╗   ██╗
      | ██╔══██╗██║     ██╔══██╗╚██╗ ██╔╝    ██╔══██╗██╔════╝ ██╔══██╗██║████╗  ██║
      | ██████╔╝██║     ███████║ ╚████╔╝     ███████║██║  ███╗███████║██║██╔██╗ ██║
      | ██╔═══╝ ██║     ██╔══██║  ╚██╔╝      ██╔══██║██║   ██║██╔══██║██║██║╚██╗██║
      | ██║     ███████╗██║  ██║   ██║       ██║  ██║╚██████╔╝██║  ██║██║██║ ╚████║
      | ╚═╝     ╚══════╝╚═╝  ╚═╝   ╚═╝       ╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═╝╚═╝╚═╝  ╚═══╝
div(v-else)
  img(src="/static/sock-logo.gif")
  pre#start_game.button(@click="start_game_button")
    template(v-if='show_line') &nbsp
    | ███████╗████████╗ █████╗ ██████╗ ████████╗     ██████╗  █████╗ ███╗   ███╗███████╗
    | ██╔════╝╚══██╔══╝██╔══██╗██╔══██╗╚══██╔══╝    ██╔════╝ ██╔══██╗████╗ ████║██╔════╝
    | ███████╗   ██║   ███████║██████╔╝   ██║       ██║  ███╗███████║██╔████╔██║█████╗
    | ╚════██║   ██║   ██╔══██║██╔══██╗   ██║       ██║   ██║██╔══██║██║╚██╔╝██║██╔══╝
    | ███████║   ██║   ██║  ██║██║  ██║   ██║       ╚██████╔╝██║  ██║██║ ╚═╝ ██║███████╗
    | ╚══════╝   ╚═╝   ╚═╝  ╚═╝╚═╝  ╚═╝   ╚═╝        ╚═════╝ ╚═╝  ╚═╝╚═╝     ╚═╝╚══════╝
    pre(v-show='show_line')
      br
      br
    pre(v-show='blink' :style='{ "font-size": "20px" }')
      br
      | By Quade and Alan
      br
      br
      br
  pre
    | Music by:&nbsp
    a(href="https://opengameart.org/users/matthewpablo") matthewpablo
    |  | See on:&nbsp
    a(href="https://github.com/QuadeMorrison/sock-tron") GitHub

</template>

<script>
import keys from "../keys.js"

export default {
  name: 'tron',
  data () {
	 return {
	   ctx: null,
	   canv_players: [],
	   pl_num: 0,
	   grid_dim: 0,
	   game_ready: false,
	   win_w: 0,  win_h: 0,
	   grid: 10,  pl_dim: 8,
	   win_list: null, FPS: 30,
	   count_down: 0, searching: true,
	   recv_delta: 0, last_time: (new Date()).getTime(),
	   delta_inc: 0, frame_delta: 0,
	   start_draw_players: false,
	   blink: true,
	   show_line: true,
	   random_show: 1500,
	   settings: {},
	   text_draw_size: 100,
	   text_min_size: 15
	 }
  },
  created() {
	 window.setInterval(this.draw, 1000 / this.FPS)
    window.setInterval(() => {
      this.blink = !this.blink
      this.random_show = Math.random * 1500 + 500;
    }, 1000)
    window.setInterval(() => this.show_line = !this.show_line, this.random_show)
  },
  sockets: {
	 connect() {
		console.log("Connected to server")
		this.reset_state();
	 },
	 game_over(players) {
		this.win_list = players;
		this.delta_inc = 0;
		this.frame_delta = 0;
	 },
	 game_starts_in(data) {
		this.start_draw_players = false
		this.canv_players = []
		this.count_down = data.count_down;
		this.settings = data.settings
		this.scale_window()
		this.init_players(data.players)
		this.start_draw_players = true
	 },
	 init_settings(settings) {
		// consistent naming
		this.settings = settings
		this.scale_window()
	 },
	 player_num(num) {
		this.pl_num = num
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
	 restart_search() {
		this.count_down = 0
		this.searching = true;
		this.canv_players = []
	 },
	 start_game(players) {
		this.count_down = 0;
		this.searching = false;
		this.init_players(players)
	 },
  },
  methods: {
	 init_players(players) {
		players.forEach(pl => {
		  let c_pl = {};
		  c_pl.color = pl["color"];
		  c_pl.next_x = this.grid_to_win(pl.x);
		  c_pl.next_y = this.grid_to_win(pl.y);
		  c_pl.cur_x = c_pl.next_x;
		  c_pl.cur_y = c_pl.next_y;
		  c_pl.num = pl.num;
		  c_pl.alive = pl.alive;

		  let path = new Path2D();
		  path.moveTo(c_pl.next_x, c_pl.next_y);
		  c_pl.path = path;

		  this.canv_players[pl["num"]] = c_pl;
		});
	 },
	 start_game_button() {
		this.game_ready = true;
		this.$socket.emit('enter_room')
	 },
	 grid_to_win(c) {
		return c * this.grid-this.grid/2;
	 },
	 play_button() {
		this.game_ready = true;
		this.$socket.emit('enter_room')
		this.reset_state()
	 },
	 reset_state() {
		console.log('STATE RESET');
		this.canv_players = [];
		this.pl_num = 0;
		this.win_list = null;
		this.start_draw_players = false;
		this.count_down = 0;
		this.searching = true;
	 },
	 draw() {
		if (this.ctx) {
		  this.draw_reset();
		  this.draw_grid();
		  if (this.start_draw_players) {
			 this.draw_players();
		  }

		  if (this.count_down > 0) {
			 this.draw_count_down();
			 this.draw_text_on_head("you");
		  } else if (this.win_list != null) {
			 this.draw_game_over();
		  } else if (this.searching) {
			 this.draw_text("Locating Socks...");
		  }
		}
	 },
	 // Draws text centered.
	 draw_text(text, options = {}) {
		let color = options.color || "white";

		let size = options.size || this.text_draw_size
		this.ctx.save();

		// Cool TECH font
		this.ctx.font = size + 'px \'Share Tech\'';

		// For Text Fill
		this.ctx.fillStyle = color;

		// For Text Outline (Looks like part of the shadow.
		this.ctx.strokeStyle = '#000';
		this.ctx.lineWidth = 2;

		// Align to the middle vertically.
		this.ctx.textBaseline = 'middle';

		// Shadow!
		this.ctx.shadowOffsetX = 0;
		this.ctx.shadowOffsetY = 0;
		this.ctx.shadowBlur = 10;
		this.ctx.shadowColor = '#000';

		let tm = this.ctx.measureText(text);
		let tx = (options.x || this.win_w/2) - tm.width/2;
		let ty = options.y || this.win_h/2;

		if (tx <= 0) tx = 0
		if (tx >= this.win_w-tm.width) tx = this.win_w-tm.width;

		if (ty <= size/2) ty = size/2;
		if (ty >= this.win_h-size/2) ty = this.win_h-size/2;

		this.ctx.strokeText(text, tx, ty);
		this.ctx.fillText(text, tx, ty);

		this.ctx.restore();
	 },
	 draw_count_down() {
		this.draw_text(this.count_down.toString());
	 },
	 draw_game_over() {
		let head_text   = "win";
		let result_text = "You Won";
		let lost = true; // Gets set to false if you aren't in the list.

		if (this.win_list.length > 1) {

		  head_text = "tie";
		  result_text = "You Tied";
		}

		this.win_list.forEach(pl => {
		  if (pl.num == this.pl_num) { lost = false }
		  this.draw_text_on_head(head_text, pl.num);
		});

		// Only if YOU lost.
		if (lost) {
		  this.draw_text_on_head("lose", this.pl_num);
		  result_text = "You Lost";
		}

		// game over text
		this.draw_text(result_text);
	 },
	 draw_text_on_head(message, pl_num=this.pl_num) {
		let pl = this.canv_players[pl_num];
		let size = this.text_draw_size / 3;
		if (size < this.text_min_size) size = this.text_min_size;
		let color = "white"; // pl.color
		let x = pl.cur_x;
		let y = pl.cur_y-this.grid;

		this.draw_text(message, { x, y, size, color });
	 },
	 draw_grid() {
		this.ctx.save();

		this.ctx.strokeStyle = "rgba(100, 100, 100, .2)";
		//this.ctx.setLineDash([5, 2.5]);
		//this.ctx.lineDashOffset = 5;
		this.ctx.lineWidth = 2;

		this.ctx.beginPath();
		for (let i = 0; i < this.grid_dim; i++) {
		  let x = i * this.grid;
		  this.ctx.moveTo(x, 0);
		  this.ctx.lineTo(x, this.win_h);
		}
		this.ctx.closePath();
		this.ctx.stroke();

		this.ctx.beginPath();
		for (let i = 0; i < this.grid_dim; i++) {
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
		this.ctx.lineWidth = this.pl_dim;

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

		this.ctx.restore();
	 },
	 ok() {
		return false;
	 },
	 scale_window() {
		let settings = this.settings
		this.grid = settings.grid;

		// scale the grid
		let smaller_dim = Math.min(window.innerHeight, window.innerWidth)
		let win_size_in_percent = 0.95
		let dim = Math.ceil(smaller_dim * win_size_in_percent / this.grid)
		this.grid = dim / settings.grid_dim * this.grid

		this.grid_dim = settings.grid_dim
		this.text_draw_size = this.grid * 4

		// scale the player
		this.pl_dim = this.grid * 0.8

		this.win_w = this.grid_dim * this.grid;
		this.win_h = this.grid_dim * this.grid;
	 },
	 key_handler(e) {
		let key = keys[e.which]
		if (key) this.$socket.emit('keydown', key)
	 },
	 scale_logo() {
	 },
	 scale() {
		this.scale_window()
	 }
  },
  mounted() {
	 // Vue's keydown event only really works for input elements
	 // so we have to bind the event the old fashioned way
	 window.addEventListener('keydown', this.key_handler)
	 window.addEventListener('resize', this.scale)
  },
  updated() {
	 // Set the context.
	 if (this.$refs.game_window) {
		this.ctx = this.$refs.game_window.getContext("2d")
	 }
  },
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
@media (max-width: 1024px), (max-height: 800px){
    img {
	height: 600px;
      }
}

@media (max-width: 800px), (max-height: 600px){
    img {
	height: 400px;
      }
}

#game_window {
  border: white solid 1px;
  background: #111;
  margin: auto;
}

.play_again {
  position: absolute !important;
  margin-left: auto;
  margin-right: auto;
  text-align: center;
  left: 0;
  right: 0;
  top: 100px;
}

div {
  height: 100%;
  display: grid;
}

button {
  margin: auto;
}

img {
  margin: auto;
}

pre {
  text-align: left;
  margin: 0 auto;
  line-height: 0.80 !important;
}

.button:hover {
  cursor: pointer;
  color: #CC0814;
}

@media (max-width: 800px), (max-height: 600px){
  #start_game {
    font-size: 10px;
  }
}

a {
  color: cyan;
}

a:visited {
  color: cyan;
}
</style>
