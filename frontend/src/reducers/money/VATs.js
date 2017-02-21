const initialState = {
	VATs: [],
	fetching: false,
	inputError: null,
	fetchError: null,
};

export function VATs(state = initialState, action) {
	if (action.type === 'VAT_FETCH_START') {
		return {
			...state,
			fetching: true,
			inputError: null,
		};
	}
	if (action.type === 'VAT_FETCH_DONE') {
		return {
			...state,
			fetching: false,
			VATs: action.VATs.map(VAT => ({
				...VAT,
				vatperiod_set: VAT.vatperiod_set.sort((a, b) => new Date(a.begin_date).getTime() - new Date(b.begin_date).getTime()),
			})),
			fetchError: null,
		};
	}

	if (action.type === 'VAT_INPUT_ERROR') return { ...state, inputError: action.error };
	if (action.type === 'VAT_FETCH_ERROR') return { ...state, fetching: false, fetchError: action.error };
	return state;
}

export default VATs;
