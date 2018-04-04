/**
 *  @param field - Which field of the object-to-validate to validate.
 *  @param name  - The human-readable name of the field.
 *  @param validatorFunction - a function that gets the state of the field to check and the state
 *   > This function then returns a function that generates the name of the error.
 *  @return An object with the field-name-key set to an error message.
 */
export const validator = (field, name, validatorFunction) => {
	return state =>
		{
    		const errorMessageFunc = validatorFunction(state[field], state);
			if (errorMessageFunc) {
				return { [field]: errorMessageFunc(name) };
			}
			return null;
		}
	};

/**
 * @param state The current state of said object
 * @param validators A list of validator objects
 * @returns an object with as key-value-pairs field-names and errors.
 */
export const validate = (state, validators) => {
	return validators.reduce((memo, runner) => ({ ...memo, ...runner(state) }), {});
};
