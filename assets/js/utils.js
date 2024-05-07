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
