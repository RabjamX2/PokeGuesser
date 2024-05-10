/** @typedef {{ [name: string]: any; }} Character */

/**
 * Returns a random key-value pair from the given object.
 * @param {Character}  allCharacters The object from which to select a random key-value pair.
 * @returns {Character} A random key-value pair from the given object.
 */
export function getRandomObjectKeyPair(allCharacters) {
	const keys = Object.keys(allCharacters);
	const randomIndex = Math.floor(Math.random() * keys.length);
	const randomKey = keys[randomIndex];

	return { [randomKey]: allCharacters[randomKey] };
}

/**
 * Converts a string to title case.
 *
 * @param {string} myString - The string to convert to title case.
 * @returns {string} The converted string in title case.
 */
export function titleCase(myString) {
	const myRegex = /\b(?<!')[a-z]/g;
	return myString.toLowerCase().replace(myRegex, function (x) {
		return x.toUpperCase();
	});
}

/**
 * Removes accents from a string.
 * @param {string} text - The string from which to remove accents.
 * @returns {string} The string without accents.
 */
export function removeAccent(text) {
	var on_accent = "öøüóőúéáàãäűíÖÜÓŐÚÉÁÀŰÍçÇ";
	var off_accent = "oouooueaaaauiOUOOUEAAUIcC";
	var idoff = -1,
		new_text = "";
	var lentext = text.toString().length - 1;

	for (let i = 0; i <= lentext; i++) {
		idoff = on_accent.search(text.charAt(i));
		if (idoff == -1) {
			new_text = new_text + text.charAt(i);
		} else {
			new_text = new_text + off_accent.charAt(idoff);
		}
	}
	return new_text;
}

export default class Game {
	/**
	 * @param {string} gameName
	 * @param {Character} correctCharacter
	 * @param {Character} allCharacters
	 * @param {{ key: string; title: string, resultType: string; matchType?: string; matches?: string[]; }[]} valueLookup
	 */
	constructor(gameInfo, correctCharacter, allCharacters, valueLookup) {
		/** @type {{ title: string; gameID: string; modulePath: string; spriteExtension: string;}} */ // !LEFT OFF HERE
		this.gameInfo = gameInfo;
		this.valueLookup = valueLookup;
		/**
		 * @type {Character}
		 * @private */
		this.correctCharacter = correctCharacter;
		/**
		 * @type {string}
		 * @private */
		this.correctCharacterName = Object.keys(correctCharacter)[0];
		/**
		 * @type {{[value: string]: string | number}}
		 * @private */
		this.correctValues = correctCharacter[this.correctCharacterName];
		/**
		 * @type {string}
		 * @private */
		this.correctSpritePath = `../modules/${this.gameInfo.gameName}/sprites/${this.correctValues.spriteID}.${this.gameInfo.spriteExtension}`;
		/** @type {Character} */
		this.allCharacters = allCharacters;
		/** @type {string[]} */
		this.allNames = Object.keys(allCharacters);
		/** @type {{name: string, spritePath: string, guessIsCorrect: boolean, guessValues:{[value : string]: string | number}, guessResults: {[value : string]: string}}[]} */
		this.guessedList = [];
	}

	get guessedCount() {
		return this.guessedList.length;
	}

	/**
	 * @param {string} guessedName The name of the Pokemon guessed by the player
	 * @param {string[]} namesNotGuessed The list of Pokemon names that have not been guessed
	 * @returns {string[]} The updated list of Pokemon names that have not been guessed
	 */
	submitGuess(guessedName, namesNotGuessed) {
		if (namesNotGuessed.includes(guessedName)) {
			namesNotGuessed.splice(namesNotGuessed.indexOf(guessedName), 1);
		}
		let guessedValues = this.allCharacters[guessedName];

		const guessedSpritePath = `assets/modules/${this.gameInfo.gameID}/sprites/${guessedValues.spriteID}.${this.gameInfo.spriteExtension}`;
		const guessIsCorrect = this.correctCharacterName === guessedName;
		let guessInfo = { name: guessedName, spritePath: guessedSpritePath, guessIsCorrect: guessIsCorrect };

		/** @type {{[value : string]: string | number}} */
		let guessValues = {};
		/** @type {{[value : string]: string}} */
		let guessResults = {};
		let guessTypes = {};

		for (const valueData of this.valueLookup) {
			// console.log(this.correctPokemonValues);

			const correctValue = this.correctValues[valueData["key"]];
			const guessedValue = guessedValues[valueData["key"]];
			guessValues[valueData["key"]] = guessedValue;
			guessTypes[valueData["key"]] = valueData["resultType"];
			if (valueData["resultType"] === "boolean") {
				const isGuessedValueCorrect = correctValue === guessedValue;
				if (isGuessedValueCorrect) {
					guessResults[valueData["key"]] = "correct";
				} else if (valueData["matchType"] === "partial") {
					let partialMatch = false;
					for (const match of valueData["matches"]) {
						partialMatch = guessedValue === this.correctValues[match];
						if (partialMatch) {
							break;
						}
					}
					guessResults[valueData["key"]] = partialMatch ? "partial" : "incorrect";
				} else {
					guessResults[valueData["key"]] = "incorrect";
				}
			} else if (valueData["resultType"] === "range") {
				if (correctValue === guessedValue) {
					guessResults[valueData["key"]] = "correct";
				} else if (correctValue > guessedValue) {
					guessResults[valueData["key"]] = "greater";
				} else if (correctValue < guessedValue) {
					guessResults[valueData["key"]] = "less";
				} else {
					console.error(`${guessedName}: ${valueData["key"]}: ${correctValue} == ${guessedValue}`);
					guessResults[valueData["key"]] = "error";
				}
			}
		}
		let output = {
			...guessInfo,
			guessValues: guessValues,
			guessResults: guessResults,
			guessTypes: guessTypes,
		};
		this.guessedList.push(output);
		this.drawResults(output);
		return namesNotGuessed;
	}

	/**
	 * TODO: Make it so it checks and adds to table instead of redrawing it everytime a guess is made
	 * @param {{ guessIsCorrect: boolean; guessValues: any; guessResults: any; name?: string; spritePath: string; }} guessedCharacter
	 */
	drawResults(guessedCharacter) {
		const table = document.getElementById("results-table");
		const tableBody = table.getElementsByTagName("tbody")[0];
		const row = tableBody.insertRow();
		row.style.height = "1px";
		const spriteCell = row.insertCell(0);
		spriteCell.classList.add("sprite-cell");
		spriteCell.setAttribute(
			"style",
			`background-color: var(${guessedCharacter.guessIsCorrect ? "--correct" : "--incorrect"});`
		);
		spriteCell.setAttribute("guess-result", guessedCharacter.guessIsCorrect ? "correct" : "incorrect");
		spriteCell.innerHTML = `<div class="sprite" style="background-image: url('${guessedCharacter.spritePath}')"></div>`;
		for (const [index, valueData] of this.valueLookup.entries()) {
			const key = valueData["key"];
			const value = guessedCharacter.guessValues[key];
			const cell = row.insertCell();

			const result = guessedCharacter.guessResults[key];
			if (guessedCharacter.guessTypes[key] === "range") {
				cell.classList.add("range-cell");
				const content = document.createElement("div");
				content.classList.add("range");
				content.setAttribute(
					"style",
					`background-image: url('assets/images/${result === "greater" ? "downArrow" : "upArrow"}.svg')`
				);
				content.innerHTML = `${value ?? "None"}`;
				cell.appendChild(content);
			} else {
				cell.innerHTML = value ?? "None";
			}

			cell.setAttribute("guess-result", result);
			cell.setAttribute("style", `height: inherit; width:inherit; background-color: var(--${result})`);
		}
	}
}
