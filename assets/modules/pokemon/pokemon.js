//@ts-check
import { getRandomObjectKeyPair, titleCase } from "../../js/utils.js";
/** @typedef {import("../../js/utils.js").Character} Character */

fetch("/assets/modules/pokemon/pokemon.json")
	.then((response) => response.json())
	.then((data) => {
		/** @type {Character} */
		const allPokemon = data;
		let pokemonNames = Object.keys(data);

		const lookup = [
			{ key: "Type I", title: "Main Type", dataType: "boolean", matchType: "partial", matches: ["Type II"] },
			{ key: "Type II", title: "Second Type", dataType: "boolean", matchType: "partial", matches: ["Type I"] },
			{ key: "Evolution Stage", title: "Evolution", dataType: "boolean" },
			{ key: "Generation", title: "Generation", dataType: "boolean" },
			{ key: "Height (m)", title: "Height", dataType: "range" },
			{ key: "Weight (kg)", title: "Weight", dataType: "range" },
			{ key: "Catch Rate", title: "Catch Rate", dataType: "range" },
		];

		// Table Headers
		const table = document.getElementById("results-table");
		const tableHead = table.getElementsByTagName("thead")[0];
		const headerRow = tableHead.insertRow();
		headerRow.innerHTML = "<th>Pokemon</th>";
		for (const valueData of lookup) {
			headerRow.innerHTML += `<th>${valueData["title"]}</th>`;
		}

		const randomPokemon = getRandomObjectKeyPair(allPokemon);
		console.log(Object.keys(randomPokemon)[0]); // Name of the random pokemon
		const gameOne = new Game(randomPokemon, allPokemon, lookup);

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
				const suggestions = pokemonNames.filter((name) => name.toLowerCase().startsWith(inputValue));
				const maxSuggestions = 10;
				for (let i = 0; i < suggestions.length; i++) {
					if (i >= maxSuggestions) {
						break;
					}
					const listItem = document.createElement("li");
					listItem.textContent = suggestions[i];
					listItem.innerHTML = `<img src="assets/modules/pokemon/sprites/${
						allPokemon[suggestions[i]]["#"]
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
			pokemonNames = gameOne.submitGuess(guess, pokemonNames);
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

class Game {
	/**
	 * @param {Character} correctPokemon
	 * @param {Character} allPokemon
	 */
	constructor(correctPokemon, allPokemon, lookup) {
		this.lookup = lookup;
		this.pokemonGenerationClues = [
			{ First: 1, Last: 151, Title: "I", Number: 1, Game: "Red and Blue/Green" },
			{ First: 152, Last: 251, Title: "II", Number: 2, Game: "Gold and Silver" },
			{ First: 252, Last: 386, Title: "III", Number: 3, Game: "Ruby and Sapphire" },
			{ First: 387, Last: 493, Title: "IV", Number: 4, Game: "Diamond and Pearl" },
			{ First: 494, Last: 649, Title: "V", Number: 5, Game: "Black and White" },
			{ First: 650, Last: 721, Title: "VI", Number: 6, Game: "X and Y" },
			{ First: 722, Last: 809, Title: "VII", Number: 7, Game: "Sun and Moon" },
			{ First: 810, Last: 905, Title: "VIII", Number: 8, Game: "Sword and Shield" },
			{ First: 906, Last: 1008, Title: "IX", Number: 9, Game: "Legends: Arceus" },
		];
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
		this.correctPokemonValues["Generation"] = this.getGenerationClue(this.correctPokemonValues["#"])["Title"];
		/**
		 * @type {string}
		 * @private */
		this.correctPokemonSpritePath = `sprites/${correctPokemon["#"]}.png`;
		/** @type {Character} */
		this.allPokemon = allPokemon;
		/** @type {string[]} */
		this.allPokemonNames = Object.keys(allPokemon);
		/** @type {{name: string, spritePath: string, guessIsCorrect: boolean, guessValues:{[value : string]: string | number}, guessResults: {[value : string]: string}}[]} */
		this.guessedPokemonList = [];
	}

	get guessedCount() {
		return this.guessedPokemonList.length;
	}

	getGenerationClue(pokemonNumber) {
		for (const generation of this.pokemonGenerationClues) {
			if (generation.First <= pokemonNumber && pokemonNumber <= generation.Last) {
				return generation;
			}
		}
		return null;
	}

	/**
	 * TODO: Make this universal and move to utils.js
	 * @param {string} guessedPokemonName The name of the Pokemon guessed by the player
	 */
	submitGuess(guessedPokemonName, pokemonNames) {
		if (pokemonNames.includes(guessedPokemonName)) {
			pokemonNames.splice(pokemonNames.indexOf(guessedPokemonName), 1);
		}
		let guessedPokemonValues = this.allPokemon[guessedPokemonName];
		guessedPokemonValues["Generation"] = this.getGenerationClue(guessedPokemonValues["#"])["Title"];
		const guessedPokemonSpritePath = `../modules/pokemon/sprites/${guessedPokemonValues["#"]}.png`;
		let guessInfo = { name: guessedPokemonName, spritePath: guessedPokemonSpritePath };
		const guessIsCorrect = this.correctPokemonName === guessedPokemonName;
		/** @type {{[value : string]: string | number}} */
		let guessValues = {};
		/** @type {{[value : string]: string}} */
		let guessResults = {};

		for (const valueData of this.lookup) {
			// console.log(this.correctPokemonValues);

			const correctValue = this.correctPokemonValues[valueData["key"]];
			const guessedValue = guessedPokemonValues[valueData["key"]];
			guessValues[valueData["key"]] = guessedValue;
			if (valueData["dataType"] === "boolean") {
				const isGuessedValueCorrect = correctValue === guessedValue;
				if (isGuessedValueCorrect) {
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
				} else {
					guessResults[valueData["key"]] = "incorrect";
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
		this.drawResults(output);
		return pokemonNames;
	}

	/**
	 * TODO: Make this universal and move to utils.js
	 * TODO: Make it so it checks and adds to table instead of redrawing it everytime a guess is made
	 * @param {{ guessIsCorrect: boolean; guessValues: any; guessResults: any; name?: string; spritePath: string; }} guessedPokemon
	 */
	drawResults(guessedPokemon) {
		const table = document.getElementById("results-table");
		const tableBody = table.getElementsByTagName("tbody")[0];
		const row = tableBody.insertRow();
		row.style.height = "1px";
		const spriteCell = row.insertCell(0);
		spriteCell.classList.add("sprite-cell");
		spriteCell.setAttribute(
			"style",
			`--bg-image: url('${guessedPokemon.spritePath}'); background-color: var(${
				guessedPokemon.guessIsCorrect ? "--correct" : "--incorrect"
			});`
		);
		spriteCell.setAttribute("guess-result", guessedPokemon.guessIsCorrect ? "correct" : "incorrect");
		for (const [index, valueData] of this.lookup.entries()) {
			const key = valueData["key"];
			const value = guessedPokemon.guessValues[key];
			const cell = row.insertCell();

			const result = guessedPokemon.guessResults[key];
			if (result === "less" || result === "greater") {
				const content = document.createElement("div");
				content.classList.add("range-cell-wrapper");
				content.innerHTML = `<div class="range">${value ?? "None"}</div>`;
				content.innerHTML += `
				<svg class="${result}" width=100 height=100 >
					<polygon fill="red"
						points="75,0 25,0 25,50 0,50 50,100 100,50 75,50"/>
				</svg>`;
				cell.appendChild(content);
			} else {
				cell.innerHTML = value ?? "None";
			}
			cell.setAttribute("guess-result", result);
			cell.setAttribute("style", `height: inherit; width:inherit; background-color: var(--${result})`);
		}
	}
}
