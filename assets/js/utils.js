export function getRandomObjectKeyPair(allObjects) {
	const keys = Object.keys(allObjects);
	const randomIndex = Math.floor(Math.random() * keys.length);
	const randomKey = keys[randomIndex];

	return { [randomKey]: allObjects[randomKey] };
}
