const initialState = {
	labelTypes: null,
	fetching: false,
	fetchError: null,
	inputError: null,
};

export default function labelTypeReducer(state = initialState, action) {
	if (action.type === 'LABEL_TYPE_FETCH_START')		 		{
		return {
			...state,
			fetching: true,
			inputError: null,
		};
	}
	if (action.type === 'LABEL_TYPE_FETCH_DONE')		 		{
		return {
			...state,
			fetching: false,
			labelTypes: action.labelTypes,
			fetchError: null,
		};
	}
	if (action.type === 'LABEL_TYPE_INPUT_ERROR')		 		{
		return {
			...state,
			inputError: action.error,
		};
	}
	if (action.type === 'LABEL_TYPE_FETCH_ERROR')		 		{
		return {
			...state,
			fetchError: action.error,
			fetching: false,
		};
	}
	return state;
}
