//@ts-check
import { getRandomObjectKeyPair, titleCase } from "../../js/utils.js";
/** @typedef {import("../../js/utils.js").Character} Character */

fetch("assets/modules/pokemon/data.json")
    .then((response) => response.json())
    .then((data) => {
        /** @type {Character} */
        const allPokemon = data;
        let pokemonNames = Object.keys(data);

        const lookup = [
            { key: "Type I", title: "Main Type", resultType: "boolean", matchType: "partial", matches: ["Type II"] },
            { key: "Type II", title: "Second Type", resultType: "boolean", matchType: "partial", matches: ["Type I"] },
            { key: "Evolution Stage", title: "Evolution", resultType: "boolean" },
            { key: "Generation", title: "Generation", resultType: "boolean" },
            { key: "Height (m)", title: "Height", resultType: "range" },
            { key: "Weight (kg)", title: "Weight", resultType: "range" },
            { key: "Catch Rate", title: "Catch Rate", resultType: "range" },
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
                    listItem.innerHTML = `<div class="sprite" style="background-image:url('assets/modules/pokemon/sprites/${allPokemon[suggestions[i]]["#"]}.png')"></div><span>${titleCase(suggestions[i])}</span>`;
                    listItem.onclick = function () {
                        // @ts-ignore
                        inputField.value = suggestions[i]; // keep lowercase to match data keys
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
            const guess = inputField.value.toLowerCase().trim();
            if (!pokemonNames.includes(guess)) return; // ignore invalid entries
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

        const giveUpButton = document.getElementById("give-up-button");
        giveUpButton.onclick = function () {
            const { name, spritePath } = gameOne.answer;
            const wrapper = document.querySelector(".guess-wrapper");
            wrapper.innerHTML = `
                <div class="reveal-card">
                    <div class="reveal-sprite" style="background-image:url('${spritePath}')"></div>
                    <div class="reveal-text">
                        <span class="reveal-label">The answer was</span>
                        <span class="reveal-name">${titleCase(name)}</span>
                    </div>
                    <button class="reveal-new-game" onclick="location.reload()">Play Again</button>
                </div>
            `;
        };
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
        this.correctPokemonValues["Generation"] = this.getGenerationClue(this.correctPokemonValues["#"])?.Title ?? "?";
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

    get answer() {
        return {
            name: this.correctPokemonName,
            spritePath: `assets/modules/pokemon/sprites/${this.correctPokemonValues["#"]}.png`,
        };
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
        guessedPokemonValues["Generation"] = this.getGenerationClue(guessedPokemonValues["#"])?.Title ?? "?";
        const guessedPokemonSpritePath = `assets/modules/pokemon/sprites/${guessedPokemonValues["#"]}.png`;
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
            if (valueData["resultType"] === "boolean") {
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
            } else if (valueData["resultType"] === "range") {
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
        const spriteCell = row.insertCell(0);
        spriteCell.classList.add("sprite-cell");
        spriteCell.setAttribute(
            "style",
            `background-color: var(${guessedPokemon.guessIsCorrect ? "--correct" : "--incorrect"});`,
        );
        spriteCell.setAttribute("guess-result", guessedPokemon.guessIsCorrect ? "correct" : "incorrect");
        spriteCell.innerHTML = `<div class="sprite" style="background-image:url('${guessedPokemon.spritePath}')"></div>`;
        for (const [index, valueData] of this.lookup.entries()) {
            const key = valueData["key"];
            const value = guessedPokemon.guessValues[key];
            const cell = row.insertCell();

            const result = guessedPokemon.guessResults[key];
            if (result === "less" || result === "greater") {
                cell.classList.add("range-cell");
                const content = document.createElement("div");
                content.classList.add("range");
                const arrowUp = `<svg viewBox="0 0 24 24" fill="white" width="24" height="24"><path d="M12 4l8 10H4z"/></svg>`;
                const arrowDown = `<svg viewBox="0 0 24 24" fill="white" width="24" height="24"><path d="M12 20l-8-10h16z"/></svg>`;
                const arrow = result === "greater" ? arrowUp : arrowDown;
                content.innerHTML = `<span class="range-value">${value ?? "None"}</span>${arrow}`;
                cell.appendChild(content);
            } else {
                cell.innerHTML = value ?? "None";
            }
            cell.setAttribute("guess-result", result);
            cell.style.backgroundColor = `var(--${result})`;
        }
    }
}
