export const replaceField = (actionType, defaultValue, fieldName = 'objects') =>
	(state = defaultValue, action) => action.type === actionType ? action[fieldName] : state;

export const booleanField = (boolObj, defaultValue) =>
	(state = defaultValue, action) => typeof boolObj[action.type] === 'undefined' ? state : boolObj[action.type];

export const reSetField = (setter, resetter, defaultValue, fieldName) =>
	(state = defaultValue, action) => {
		if (action.type === resetter)
			return defaultValue;
		 else if (action.type === setter)
			return action[fieldName];

		return state;
	};
