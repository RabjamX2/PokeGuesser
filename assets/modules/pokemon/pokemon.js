import { getRandomObjectKeyPair } from "/assets/js/utils.js";

fetch("/assets/modules/pokemon/pokemon.json")
	.then((response) => response.json())
	.then((data) => {
		const allPokemon = data;
		const pokemonNames = Object.keys(data);

		console.log(getRandomObjectKeyPair(allPokemon));
	})
	.catch((error) => {
		console.error("Error fetching JSON:", error);
	});

class Game {
	constructor(correctPokemon) {
		this.correctPokemon = correctPokemon;
		this.guessedPokemonList = [];
	}

	compareRange(guessedValue, key) {
		const correctValue = this.correctPokemon[betterPokemonDataKeysDict[key]["key"]];
		if (correctValue === guessedValue) {
			return "True";
		} else if (correctValue > guessedValue) {
			return "Greater";
		} else if (correctValue < guessedValue) {
			return "Less";
		} else {
			return "Error";
		}
	}

	compareBoolean(guessedValue, key) {
		return this.correctPokemon[betterPokemonDataKeysDict[key]["key"]] === guessedValue;
	}

	submitGuess(guessedPokemonName) {
		const result = {};
		const guessedPokemon = new Pokemon(pokemonData[guessedPokemonName]);
		const guessedPokemonNumber = guessedPokemon.number;

		// Assuming "assets/sprites/" exists, adjust path if needed
		const guessedPokemonSpritePath = `assets/sprites/${guessedPokemonNumber}.png`;

		result["Correct"] = this.correctPokemon.number === guessedPokemon.number;

		for (const key in betterPokemonDataKeysDict) {
			const value = betterPokemonDataKeysDict[key];
			const guessedValue = guessedPokemon[key];

			if (value["data_type"] === "range") {
				result[key] = {
					data_type: value["data_type"],
					guessed_value: guessedValue,
					result: this.compareRange(guessedValue, key),
				};
			} else if (value["data_type"] === "boolean") {
				result[key] = {
					data_type: value["data_type"],
					guessed_value: guessedValue,
					result: this.compareBoolean(guessedValue, key),
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

class Pokemon {
	constructor(pokemonTuple) {
		this.name = pokemonTuple[0];
		this.data = pokemonTuple[1];
	}

	// Simulating Python's __getattr__ behavior
	get(key) {
		return this.data[betterPokemonDataKeysDict[key]["key"]];
	}

	key(key) {
		return this.data[betterPokemonDataKeysDict[key]["key"]];
	}
}
