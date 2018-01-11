export const setFieldReducer = (types, defaultValue, fieldName = 'value') => {
	return (state = defaultValue, action) => {
		if (types.includes(action.type)) {
			return action[fieldName];
		}
		return state;
	};
};

//
export const objectControlReducer = (setFieldTypes, defaultValue) => {
	return (state = defaultValue, action) => {
		if (setFieldTypes.includes(action.type) && state[action.field] !== action.value) {
			return {
				...state,
				[action.field]: action.value,
			};
		}
		return state;
	};
};

// give an object of actionType=>boolean for setting this boolean in a composed state
export const booleanControlReducer = (types, defaultValue) => {
	return (state = defaultValue, action) => {
		if (typeof types[action.type] !== 'undefined') {
			return types[action.type];
		}
		return state;
	};
};

export const collectReducers = (...reducers) => {
	return (state, action) => reducers.reduce((_state, reducer) => reducer(_state, action), state);
};

export const resetFieldReducer = (types, defaultValue) => {
	return (state = defaultValue, action) => types.includes(action.type) ? defaultValue : state;
};

