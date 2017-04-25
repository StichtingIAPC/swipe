const initialState = {
	unitTypes: null,
	fetching: false,
	fetchError: null,
	inputError: null,
};

export default function unitTypeReducer(state = initialState, action) {
	if (action.type === 'UNIT_TYPE_FETCH_START')
		return { ...state, fetching: true, inputError: null };
	if (action.type === 'UNIT_TYPE_FETCH_DONE')
		return { ...state, fetching: false, unitTypes: action.unitTypes, fetchError: null };
	if (action.type === 'UNIT_TYPE_INPUT_ERROR')
		return { ...state, inputError: action.error };
	if (action.type === 'UNIT_TYPE_FETCH_ERROR')
		return { ...state, fetchError: action.error, fetching: false };
	return state;
}
