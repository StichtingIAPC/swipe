const initialState = {
	VATPeriods: [],
	fetching: false,
	inputError: null,
	fetchError: null,
};

export function VATPeriods(state = initialState, action) {
	if (action.type === 'VAT_PERIOD_FETCH_START') {
		return {
			...state,
			fetching: true,
			inputError: null,
		};
	}
	if (action.type === 'VAT_PERIOD_FETCH_DONE') {
		return {
			...state,
			fetching: false,
			VATPeriods: action.VATPeriods,
			fetchError: null,
		};
	}

	if (action.type === 'VAT_PERIOD_INPUT_ERROR') return { ...state, inputError: action.error };
	if (action.type === 'VAT_PERIOD_FETCH_ERROR') return { ...state, fetching: false, fetchError: action.error };
	return state;
}

export default VATPeriods;
