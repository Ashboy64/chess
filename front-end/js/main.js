// Assumes that the user is always playing black

const game_url = "http://127.0.0.1:5000/"
const prefix = "https://github.com/Ashboy64/chess/blob/master/images/Chess_"

var assets = {
	"black bishop": "&#9821",
	"white bishop": "&#9815",
	"black king": "&#9818",
	"white king": "&#9812",
	"black knight": "&#9822",
	"white knight": "&#9816",
	"black pawn": "&#9823",
	"white pawn": "&#9817",
	"black queen": "&#9819",
	"white queen": "&#9813",
	"black rook": "&#9820",
	"white rook": "&#9814"
};

var selected = null;
var table = document.querySelector("table");

// var assets = {
// 	"black bishop": prefix + "bdt60.png",
// 	"white bishop": prefix + "blt60.png",
// 	"black king": prefix + "kdt60.png",
// 	"white king": prefix + "klt60.png",
// 	"black knight": prefix + "ndt60.png",
// 	"white knight": prefix + "nlt60.png",
// 	"black pawn": prefix + "pdt60.png",
// 	"white pawn": prefix + "plt60.png",
// 	"black queen": prefix + "qdt60.png",
// 	"white queen": prefix + "qlt60.png",
// 	"black rook": prefix + "rdt60.png",
// 	"white rook": prefix + "rlt60.png"
// };

function format(table){
	table.style.marginLeft = "auto"
	table.style.marginRight = "auto"
	table.style.verticalAlgin = "middle"
}

function generateBoard(table) {
	for (let i = 0; i < 8; i++) {
		let row = table.insertRow();
		for (let j = 0; j < 8; j++) {
			let cell = row.insertCell();

			let div = document.createElement("div");
			div.id = "div_" + i + "." + j
			div.className = "unoccupied";
			div.style.width = "75px";
			div.style.height = "75px";
			div.style.border = "1px solid white"
			div.onclick = function () {
				return onClick(this.id)
			};

			if ((i + j) % 2 == 0){
				div.style.background = "#e1e2e3"
			} else {
				div.style.background = "#636363"
			}
			div.style.float = "left"

			cell.appendChild(div)
		}
	}
}

function stepOpponent(){
	let Http = new XMLHttpRequest();
	Http.open("GET", game_url + "opponent_step");
	Http.send();

	Http.onreadystatechange = (e) => {
		if (Http.readyState == 4 && Http.status == 200){

				if (JSON.parse(Http.responseText)["user_checkmated"]){
					alert("You Lost!")
					updateTable(table)
					stepOpponent()
				}

			updateTable(table)
		}
	}
}

function onClick(id){
	let div = document.getElementById(id)

	if (selected == null && div.innerHTML != '' && div.className == "black") {
		div.style.border = "1px solid red"
		selected = id.slice(4).split(".")
	} else if (selected != null) {

		let Http = new XMLHttpRequest();
		Http.open("GET", game_url + "take_action" + formatParams({
			"type": 0,
			"new": [selected, id.slice(4).split(".")]
		}));
		Http.send();

		Http.onreadystatechange = (e) => {
			if (Http.readyState == 4 && Http.status == 200){
				let worked = JSON.parse(Http.responseText)["worked"]
				if (worked){
					document.getElementById("div_" + selected.join(".")).style.border = "1px solid white";
					selected = null;
					updateTable(table)

					if (JSON.parse(Http.responseText)["opp_checkmated"]){
						alert("You Won!")
						updateTable(table)
					}

					stepOpponent()
				} else {
					alert("Please enter a valid move.")
					document.getElementById("div_" + selected.join(".")).style.border = "1px solid white";
					selected = null
				}
			}
		}

	}
}

function updateTable(table){
	let Http = new XMLHttpRequest();
	Http.open("GET", game_url);
	Http.send();

	Http.onreadystatechange = (e) => {
		if (Http.readyState == 4 && Http.status == 200){
			let game_state = JSON.parse(Http.responseText)

			if (game_state != undefined){
				for (let i = 0; i < 8; i++){
					for (let j = 0 ; j < 8; j++){
						let div = document.getElementById("div_" + i + "." + j);
						let to_use = game_state[i][j].slice(2);

						if (game_state[i][j][0] == '0'){
							to_use = "white " + to_use;
						} else if (game_state[i][j][0] == '1') {
							to_use = "black " + to_use;
						} else {
							div.innerHTML = '';
							div.className = "unoccupied";
						}

						if (assets.hasOwnProperty(to_use)){
							div.innerHTML = '<p style="font-size: 60px; margin-top: 0px;" id=p_' + i + "." + j + '>' + assets[to_use] + '</p>';
							div.className = to_use.slice(0, 5)
							// div.innerHTML += '<img src="' + assets[to_use] + '"/>';
						}
					}
				}
			}
		}
	}
}

function formatParams( params ){
  return "?" + Object
        .keys(params)
        .map(function(key){
          return key+"="+encodeURIComponent(params[key])
        })
        .join("&")
}

format(table)
generateBoard(table)
updateTable(table)
stepOpponent()
