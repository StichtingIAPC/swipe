/**
 *  @param field - Which field of the object-to-validate to validate.
 *  @param name  - The human-readable name of the field.
 *  @param validatorFunction - a function that gets the state of the field to check and the state
 *   > This function then returns a function that generates the name of the error.
 *  @return An object with the field-name-key set to an error message.
 */
export const validator = (field, name, validatorFunction) => state => {
	const errorMessageFunc = validatorFunction(state[field], state);

	if (errorMessageFunc) {
		return {[field]: errorMessageFunc(name)};
	}
	return null;
};

/**
 * @param state The current state of said object
 * @param validators A list of validator objects
 * @returns an object with as key-value-pairs field-names and errors.
 */
export const validate = (state, validators) => validators.reduce((memo, runner) => ({
	...memo,
	...runner(state),
}), {});

/**
 * @param state A part of the state that's a validation-result-object.
 * @returns {boolean} Does this thing contain an error?
 */
export const hasError = (state) => {
	for (let [key, value] of Object.entries(state)) {
		if (value.type === 'error') {
			return true;
		}
	}
	return false;
};

/**
 * Asserts that something is indeed a valid money string
 * @param str String: the string
 * @returns boolean
 */
export const isMoney = (str) => {
	return str.match("^[0-9]{1,16}(\\.[0-9]{1,5})?$");
};