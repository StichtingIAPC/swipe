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
		if (types[action.type] === 'toggle') {
			return !state;
		} else if (typeof types[action.type] !== 'undefined') {
			return types[action.type];
		}
		return state;
	};

export const collectReducers = (...reducers) =>
	(state, action) => reducers.reduce((_state, reducer) => reducer(_state, action), state);

export const resetFieldReducer = (types, defaultValue) =>
	(state = defaultValue, action) => types.includes(action.type) ? defaultValue : state;
