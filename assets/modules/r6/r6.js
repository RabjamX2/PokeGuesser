//@ts-check
import { getRandomObjectKeyPair, titleCase, removeAccent } from "../../js/utils.js";
import Game from "../../js/utils.js";
/** @typedef {import("../../js/utils.js").Character} Character */

const gameInfo = {
	title: "Rainbow Six Siege",
	gameID: "r6",
	modulePath: "assets/modules/r6",
	spriteExtension: "svg",
};

fetch(`/assets/modules/${gameInfo.gameID}/data.json`)
	.then((response) => response.json())
	.then((data) => {
		/** @type {Character} */
		const allOperators = data;
		let operatorNames = Object.keys(data);

		/** @type {{ key: string; title: string, resultType: string; matchType?: string; matches?: string[]; }[]} */
		const lookup = [
			{ key: "Position", title: "Position", resultType: "boolean" },
			{ key: "Armor", title: "Armor", resultType: "boolean" },
			{ key: "Speed", title: "Speed", resultType: "boolean" },
			{ key: "Birthplace", title: "Birthplace", resultType: "boolean" },
			{ key: "Age", title: "Age", resultType: "range" },
			{ key: "Height (m)", title: "Height", resultType: "range" },
			{ key: "Weight (kg)", title: "Weight", resultType: "range" },
			{ key: "Role", title: "Role", resultType: "boolean", matchType: "partial", matches: ["Role 2"] },
			{ key: "Role 2", title: "Role 2", resultType: "boolean", matchType: "partial", matches: ["Role"] },
			{ key: "Release Season", title: "Season", resultType: "boolean" },
		];

		// Table Headers
		const table = document.getElementById("results-table");
		const tableHead = table.getElementsByTagName("thead")[0];
		const headerRow = tableHead.insertRow();
		headerRow.innerHTML = "<th>Operator</th>"; // ! Make Dynamic
		for (const valueData of lookup) {
			headerRow.innerHTML += `<th>${valueData["title"]}</th>`;
		}

		const randomOperator = getRandomObjectKeyPair(allOperators);
		// const randomOperator = { mira: allOperators["mira"] };
		console.log(Object.keys(randomOperator)[0]); // Name of the random pokemon
		const gameOne = new RainbowSix(gameInfo, randomOperator, allOperators, lookup);

		const inputField = document.getElementById("guess-input");
		const suggestionsList = document.getElementById("suggestionsList");
		inputField.addEventListener("focus", function () {
			suggestionsList.style.display = "block";
		});
		inputField.addEventListener("blur", function () {
			setTimeout(() => {
				suggestionsList.style.display = "none";
			}, 200);
		});
		inputField.addEventListener("keyup", function () {
			// @ts-ignore
			const inputValue = inputField.value;
			let formattedInput = removeAccent(inputValue.toLowerCase());

			suggestionsList.innerHTML = ""; // Clear previous suggestions

			if (formattedInput.length > 0) {
				const suggestions = operatorNames.filter((name) => name.startsWith(formattedInput));
				const maxSuggestions = 10;
				for (let i = 0; i < maxSuggestions; i++) {
					if (i >= suggestions.length) {
						break;
					}
					const listItem = document.createElement("li");

					listItem.innerHTML = `<div class="sprite" style="background-image: url('${gameInfo.modulePath}/sprites/${
						allOperators[suggestions[i]]["spriteID"]
					}.${gameInfo.spriteExtension}')"></div><span>${allOperators[suggestions[i]]["Name"]}</span>`;

					listItem.onclick = function () {
						// @ts-ignore
						inputField.value = allOperators[suggestions[i]]["Name"];
						inputField.focus(); // prevents the need to click the input field again after selecting a suggestion
						suggestionsList.style.display = "none";
					};

					suggestionsList.appendChild(listItem);
				}
				suggestionsList.style.display = "block"; // Show suggestions
			} else {
				suggestionsList.style.display = "none"; // Hide if input is empty
			}
		});

		const submitButton = document.getElementById("guess-input-button");
		function submitInputField() {
			const table = document.getElementById("results-table");
			// @ts-ignore
			const inputValue = inputField.value;
			let formattedInput = removeAccent(inputValue.toLowerCase());

			var operatorNameSet = new Set(operatorNames);
			if (operatorNameSet.has(formattedInput)) {
				console.log(`Submitting: ${formattedInput}`);
				// operatorNames = gameOne.submitGuess(formattedInput, operatorNames);
				operatorNames = gameOne.submitGuess(formattedInput, operatorNames);
				// @ts-ignore
				inputField.value = "";
				window.scrollBy({
					top: table.offsetHeight,
					behavior: "smooth",
				});
			} else {
				console.error(`Not found: ${formattedInput}`);
			}
		}
		submitButton.onclick = submitInputField;
		inputField.addEventListener("keydown", function (event) {
			if (event.key === "Enter") {
				submitInputField();
			}
		});
	})
	.catch((error) => {
		console.error("Error:", error);
	});

class RainbowSix extends Game {
	constructor(gameName, randomPokemon, allOperators, lookup) {
		super(gameName, randomPokemon, allOperators, lookup);
	}
}
