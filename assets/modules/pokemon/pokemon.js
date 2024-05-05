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
		// gameOne.submitGuess(pokemonNames[0]);
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
		/** @type {Character} */
		this.allPokemon = allPokemon;
		/** @type {Character[]} */
		this.guessedPokemonList = [];

		this.lookup = ["Type I", "Type II", "Evolution Stage", "Height (m)", "Weight (kg)", "Catch Rate"];
	}

	get guessedCount() {
		return this.guessedPokemonList.length;
	}

	// compareRange(guessedValue, key) {
	// 	const correctValue = this.correctPokemon[];
	// 	if (correctValue === guessedValue) {
	// 		return "True";
	// 	} else if (correctValue > guessedValue) {
	// 		return "Greater";
	// 	} else if (correctValue < guessedValue) {
	// 		return "Less";
	// 	} else {
	// 		return "Error";
	// 	}
	// }

	// compareBoolean(guessedValue, key) {
	// 	return this.correctPokemon[betterPokemonDataKeysDict[key]["key"]] === guessedValue;
	// }

	/**
	 * @param {string} guessedPokemonName The name of the Pokemon guessed by the player
	 */
	submitGuess(guessedPokemonName) {
		const result = {};
		const guessedPokemon = this.allPokemon[guessedPokemonName];

		const guessedPokemonSpritePath = `sprites/${guessedPokemon["#"]}.png`;
		console.log(guessedPokemonSpritePath);

		result["Correct"] = this.correctPokemon === guessedPokemon;

		for (const key of this.lookup) {
			const value = this.correctPokemon[key];
			const guessedValue = guessedPokemon[key];

			if (value["data_type"] === "range") {
				result[key] = {
					data_type: value["data_type"],
					guessed_value: guessedValue,
					// result: this.compareRange(guessedValue, key),
				};
			} else if (value["data_type"] === "boolean") {
				result[key] = {
					data_type: value["data_type"],
					guessed_value: guessedValue,
					// result: this.compareBoolean(guessedValue, key),
				};
			}
		}

		this.guessedPokemonList.push({
			guess_number: this.guessedPokemonList.length + 1,
			guess_pokemon: guessedPokemon.name,
			sprite: guessedPokemonSpritePath,
			results: result,
		});
	}
}
