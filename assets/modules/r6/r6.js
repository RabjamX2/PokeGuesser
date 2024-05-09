//@ts-check
import { getRandomObjectKeyPair, titleCase } from "../../js/utils.js";
import Game from "../../js/utils.js";
/** @typedef {import("../../js/utils.js").Character} Character */

const gameInfo = {
	title: "Rainbow Six Siege",
	gameId: "r6",
	modulePath: "assets/modules/r6",
	spriteID: "Name (formatted)",
};

fetch("/assets/modules/r6/r6.json")
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
			const inputValue = inputField.value.toLowerCase();
			suggestionsList.innerHTML = ""; // Clear previous suggestions

			if (inputValue.length > 0) {
				const suggestions = operatorNames.filter((name) => name.toLowerCase().startsWith(inputValue));
				const maxSuggestions = 10;
				for (let i = 0; i < suggestions.length; i++) {
					if (i >= maxSuggestions) {
						break;
					}
					const listItem = document.createElement("li");
					listItem.textContent = suggestions[i];
					listItem.innerHTML = `<img src="${gameInfo.modulePath}/sprites/${
						allOperators[suggestions[i]][gameInfo.spriteID]
					}.png" alt="" style="fit"/><span>${suggestions[i]}</span>`;
					listItem.onclick = function () {
						// @ts-ignore
						inputField.value = suggestions[i];
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
			const guess = titleCase(inputField.value);
			operatorNames = gameOne.submitGuess(guess, operatorNames);
			// @ts-ignore
			inputField.value = "";
			window.scrollBy({
				top: table.offsetHeight,
				behavior: "smooth",
			});
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
