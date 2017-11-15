const initialState = {
	stock: [],
	fetching: false,
	fetchError: null,
	inputError: null,
};

export default function stockReducer(state = initialState, action) {
	if (action.type === 'STOCK_FETCH_START')		 		{
		return {
			...state,
			fetching: true,
			inputError: null,
		};
	}
	if (action.type === 'STOCK_FETCH_DONE')		 		{
		return {
			...state,
			fetching: false,
			stock: action.stock,
			fetchError: null,
		};
	}

	if (action.type === 'STOCK_FETCH_ERROR')		 		{
		return {
			...state,
			fetchError: action.error,
			fetching: false,
		};
	}
	return state;
}
