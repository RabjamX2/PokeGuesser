//@ts-check
import { getRandomObjectKeyPair } from "../../js/utils.js";
/** @typedef {import("../../js/utils.js").Character} Character */

fetch("/assets/modules/pokemon/pokemon.json")
	.then((response) => response.json())
	.then((data) => {
		// * This is where main code should go
		/** @type {Character} */
		const allPokemon = data;
		const pokemonNames = Object.keys(data);

		const randomPokemon = getRandomObjectKeyPair(allPokemon);
		console.log(Object.keys(randomPokemon)[0]);
		const gameOne = new Game(randomPokemon, allPokemon);
		gameOne.submitGuess(pokemonNames[0]);
		gameOne.drawResults();

		const inputField = document.getElementById("guess-input");
		const suggestionsList = document.getElementById("suggestionsList");

		inputField.addEventListener("keyup", function () {
			// @ts-ignore
			const inputValue = inputField.value.toLowerCase();
			suggestionsList.innerHTML = ""; // Clear previous suggestions

			if (inputValue.length > 0) {
				const suggestions = pokemonNames.filter((name) => name.toLowerCase().startsWith(inputValue));

				suggestions.forEach((suggestion) => {
					const listItem = document.createElement("li");
					listItem.textContent = suggestion;
					suggestionsList.appendChild(listItem);
				});

				suggestionsList.style.display = "block"; // Show suggestions
			} else {
				suggestionsList.style.display = "none"; // Hide if input is empty
			}
		});
	})
	.catch((error) => {
		console.error("Error:", error);
	});

class Game {
	/**
	 * @param {Character} correctPokemon
	 * @param {Character} allPokemon
	 */
	constructor(correctPokemon, allPokemon) {
		/**
		 * @type {Character}
		 * @private */
		this.correctPokemon = correctPokemon;
		/**
		 * @type {string}
		 * @private */
		this.correctPokemonName = Object.keys(correctPokemon)[0];
		/**
		 * @type {{[value: string]: string | number}}
		 * @private */
		this.correctPokemonValues = correctPokemon[this.correctPokemonName];
		/**
		 * @type {string}
		 * @private */
		this.correctPokemonSpritePath = `sprites/${correctPokemon["#"]}.png`;
		/** @type {Character} */
		this.allPokemon = allPokemon;
		/** @type {string[]} */
		this.allPokemonNames = Object.keys(allPokemon);
		/**
		 * guessValues: {"Type I": "Fire", "Type II": None, "Evolution Stage": 0, ...}
		 * guessResults: {"Type I": "partial", "Type II": "false", "Evolution Stage": "Greater", ...}
		 *
		 * @type {{name: string, spritePath: string, guessIsCorrect: boolean, guessValues:{[value : string]: string | number}, guessResults: {[value : string]: string}}[]}
		 *
		 */
		this.guessedPokemonList = [];

		this.lookup = [
			{ key: "Type I", title: "Main Type", dataType: "boolean", matchType: "partial", matches: ["Type II"] },
			{ key: "Type II", title: "Second Type", dataType: "boolean", matchType: "partial", matches: ["Type I"] },
			{ key: "Evolution Stage", title: "Evolution Stage", dataType: "range" },
			{ key: "Height (m)", title: "Height", dataType: "range" },
			{ key: "Weight (kg)", title: "Weight", dataType: "range" },
			{ key: "Catch Rate", title: "Catch Rate", dataType: "range" },
		];
	}

	get guessedCount() {
		return this.guessedPokemonList.length;
	}

	/**
	 * TODO: Make this universal and move to utils.js
	 * @param {string} guessedPokemonName The name of the Pokemon guessed by the player
	 */
	submitGuess(guessedPokemonName) {
		const guessedPokemonValues = this.allPokemon[guessedPokemonName];
		const guessedPokemonSpritePath = `assets/modules/pokemon/sprites/${guessedPokemonValues["#"]}.png`;
		let guessInfo = { name: guessedPokemonName, spritePath: guessedPokemonSpritePath };
		const guessIsCorrect = this.correctPokemonName === guessedPokemonName;
		/** @type {{[value : string]: string | number}} */
		let guessValues = {};
		/** @type {{[value : string]: string}} */
		let guessResults = {};

		for (const valueData of this.lookup) {
			console.log(this.correctPokemonValues);
			const correctValue = this.correctPokemonValues[valueData["key"]];
			const guessedValue = guessedPokemonValues[valueData["key"]];
			guessValues[valueData["key"]] = guessedValue;
			if (valueData["dataType"] === "boolean") {
				const isGuessCorrect = correctValue === guessedValue;
				if (isGuessCorrect) {
					guessResults[valueData["key"]] = "correct";
				} else if (valueData["matchType"] === "partial") {
					let partialMatch = false;
					for (const match of valueData["matches"]) {
						partialMatch = correctValue === guessedPokemonValues[match];
						if (partialMatch) {
							break;
						}
					}
					guessResults[valueData["key"]] = partialMatch ? "partial" : "incorrect";
				}
			} else if (valueData["dataType"] === "range") {
				if (correctValue === guessedValue) {
					guessResults[valueData["key"]] = "correct";
				} else if (correctValue > guessedValue) {
					guessResults[valueData["key"]] = "greater";
				} else if (correctValue < guessedValue) {
					guessResults[valueData["key"]] = "less";
				} else {
					console.error(`${guessedPokemonName}: ${valueData["key"]}: ${correctValue} == ${guessedValue}`);
					guessResults[valueData["key"]] = "error";
				}
			}
		}
		let output = {
			...guessInfo,
			guessIsCorrect: guessIsCorrect,
			guessValues: guessValues,
			guessResults: guessResults,
		};
		this.guessedPokemonList.push(output);
		return output;
	}

	/**
	 * TODO: Make this universal and move to utils.js
	 * TODO: Make it so it checks and adds to table instead of redrawing it everytime a guess is made
	 */
	drawResults() {
		const table = document.getElementById("results-table");
		const tableHead = table.getElementsByTagName("thead")[0];
		const headerRow = tableHead.insertRow();
		const name = headerRow.insertCell();
		name.innerHTML = "Pokemon";
		for (const valueData of this.lookup) {
			const cell = headerRow.insertCell();
			cell.innerHTML = valueData["title"];
		}
		const tableBody = table.getElementsByTagName("tbody")[0];
		for (const guessedPokemon of this.guessedPokemonList) {
			const row = tableBody.insertRow();
			const spriteCell = row.insertCell(0);
			spriteCell.innerHTML = `<img src="${guessedPokemon.spritePath}" alt="${guessedPokemon.name}" style="width: 50px; height: 50px;">`;
			for (const [index, valueData] of this.lookup.entries()) {
				const key = valueData["key"];
				const value = guessedPokemon.guessValues[key];
				const cell = row.insertCell();
				cell.innerHTML = value.toString();
				const result = guessedPokemon.guessResults[key];
			}
		}
	}

	dropdown() {}
}
