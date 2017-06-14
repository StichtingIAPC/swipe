const initialState = {
	currencies: null,
	fetching: false,
	inputError: null,
	fetchError: null,
};

export function currencies(state = initialState, action) {
	if (action.type === 'CURRENCY_FETCH_START') {
		return {
			...state,
			fetching: true,
			inputError: null,
		};
	}
	if (action.type === 'CURRENCY_FETCH_DONE') {
		return {
			...state,
			fetching: false,
			currencies: action.currencies.map(currency => ({
				...currency,
				denomination_set: currency.denomination_set.sort((a, b) => Number(a.amount) - Number(b.amount)),
			})),
			fetchError: null,
		};
	}

	if (action.type === 'CURRENCY_INPUT_ERROR') 		{
		return {
			...state,
			inputError: action.error,
		};
	}
	if (action.type === 'CURRENCY_FETCH_ERROR') 		{
		return {
			...state,
			fetching: false,
			fetchError: action.error,
		};
	}
	return state;
}

export default currencies;
