export const setFieldReducer = (types, defaultValue, fieldName = 'value') =>
	(state = defaultValue, action) => {
		let tempAction = action;

		if (types.includes(action.type)) {
			for (const field of fieldName.split('.')) {
				tempAction = tempAction[field];
			}
			return tempAction;
		}
		return state;
	};

//
export const objectControlReducer = (setFieldTypes, defaultValue) =>
	(state = defaultValue, action) => {
		if (setFieldTypes.includes(action.type) && state[action.field] !== action.value) {
			return {
				...state,
				[action.field]: action.value,
			};
		}
		return state;
	};

export const pathControlReducer = (setFieldTypes, defaultValue) =>
	(state = defaultValue, action) => {
		if (setFieldTypes.includes(action.type) && state[action.field] !== action.value) {
			const fields = action.field.split('.');

			if (fields.reduce((s = {}, f) => s[f], state) === action.value) {
				return state;
			}

			const newState = Object.assign({}, state);
			let temp = newState;

			// eslint-disable-next-line
			for (let i = 0; i < fields.length; i++) {
				if (i === fields.length - 1) {
					if (temp[fields[i]] === action.value) {
						return state;
					}
					temp[fields[i]] = action.value;
					return newState;
				}
				temp[fields[i]] = Object.assign({}, temp[fields[i]]);
				if (!temp[fields[i]]) {
					temp[fields[i]] = {};
				}
				temp = temp[fields[i]];
			}

			return {
				...state,
				[action.field]: action.value,
			};
		}
		return state;
	};


// give an object of actionType=>boolean for setting this boolean in a composed state
export const booleanControlReducer = (types, defaultValue) =>
	(state = defaultValue, action) => {
		if (typeof types[action.type] !== 'undefined') {
			return types[action.type];
		}
		return state;
	};

export const collectReducers = (...reducers) =>
	(state, action) => reducers.reduce((_state, reducer) => reducer(_state, action), state);

export const resetFieldReducer = (types, defaultValue) =>
	(state = defaultValue, action) => {
		if (types.includes(action.type)) {
			return defaultValue;
		}
		return state;
	};

export const idToObjectMappingReducer = (types, defaultValue, fieldName, idFieldName) =>
	(state = defaultValue, action) => {
		if (types.includes(action.type)) {
			const object = action[fieldName];

			return {
				...state,
				[object[idFieldName]]: object,
			};
		}
		return state;
	};

export const multiIdToObjectMappingReducer = (types, defaultValue, fieldName, idFieldName) =>
	(state = defaultValue, action) => {
		if (types.includes(action.type)) {
			const objects = action[fieldName];

			return objects.reduce((result, object) => ({
				...result,
				[object[idFieldName]]: object,
			}), state);
		}
		return state;
	};

export const reducerMappedById = (identifier, wrappedReducer, defaultValue) =>
	(state = defaultValue, action) => {
		const id = action[identifier];

		if (typeof id !== 'undefined') {
			const currentValue = state[id];
			const newValue = wrappedReducer(state[id], action);

			if (currentValue === newValue) {
				return state;
			}
			return {
				...state,
				[id]: newValue,
			};
		}

		return state;
	};
