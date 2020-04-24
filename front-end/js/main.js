const game_url = "http://127.0.0.1:5000/"

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
			div.style.width = "75px";
			div.style.height = "75px";

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

function updateTable(table){
	let Http = new XMLHttpRequest();
	Http.open("GET", game_url);
	Http.send();

	Http.onreadystatechange = (e) => {
		if (Http.readyState == 4 && Http.status == 200){
			console.log("here")
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
						}

						if (assets.hasOwnProperty(to_use)){
							div.innerHTML += '<p style="font-size: 60px; margin-top: 0px;" id=p_' + i + "." + j + '>' + assets[to_use] + '</p>';
						}
					}
				}
			}
		}
	}
}

let table = document.querySelector("table");
format(table)
generateBoard(table)
updateTable(table)
