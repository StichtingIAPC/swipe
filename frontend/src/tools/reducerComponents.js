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
	(state = defaultValue, action) => types.includes(action.type) ? defaultValue : state;

const subMerge = (resultObject, objectA, objectB, mergeFunction) => {
	const keys = {};

	for (const key in objectA) {
		if (objectA.hasOwnProperty(key)) {
			keys[key] = true;
		}
	}
	for (const key in objectB) {
		if (objectB.hasOwnProperty(key)) {
			keys[key] = true;
		}
	}
	for (const key in keys) {
		if (!objectA.hasOwnProperty(key)) {
			resultObject[key] = objectB[key];
		} else if (!objectB.hasOwnProperty(key) || objectA[key] == objectB[key]) {
			resultObject[key] = objectA[key];
		} else if (typeof objectA[key] === 'object' && typeof objectB[key] === 'object' && !Array.isArray(objectA[key]) && !Array.isArray(objectB[key])) {
			resultObject[key] = {};
			subMerge(resultObject[key], objectA[key], objectB[key], mergeFunction);
		} else {
			resultObject[key] = mergeFunction(objectA[key], objectB[key]);
		}
	}
};

/**
 * Recursively merges two objects and executes given function if it can't merge intuitively.
 *
 * Examples:
 * Invoking this function with `{a: 1}` and `{b: 2}` would return `{a: 1, b: 2}`.
 * Invoking this function with `{a: [1]}` and `{a: [2], b: 2}` would call the merge function on `a`.
 * By default, it would concatinate the objects and return `{a: '12', b: 2}` as the merged object.
 *
 * @param objectA Object you want to merge with objectB.
 * @param objectB Object you want to merge with objectA.
 * @param mergeFunction Function that will get executed, in case function encounters non-intuitively mergable objects [arrays, functions, other incompatible types] function
 * will receive two parameters and its return value will be placed where the two parameters would have been inserted.
 * By default this function is simply `(a, b) => a + b`
 */
export const mergeObjects = (objectA, objectB, mergeFunction = (a, b) => a + b) => {
	const resultObject = {};

	subMerge(resultObject, objectA, objectB, mergeFunction);
	return resultObject;
};
