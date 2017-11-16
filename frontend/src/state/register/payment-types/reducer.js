const initialState = {
	paymentTypes: [],
	fetching: false,
	fetchError: null,
	inputError: null,
};

export default function paymentTypeReducer(state = initialState, action) {
	if (action.type === 'PAYMENT_TYPE_FETCH_START')		 		{
		return {
			...state,
			fetching: true,
			inputError: null,
		};
	}
	if (action.type === 'PAYMENT_TYPE_FETCH_DONE')		 		{
		return {
			...state,
			fetching: false,
			paymentTypes: action.paymentTypes,
			fetchError: null,
		};
	}
	if (action.type === 'PAYMENT_TYPE_INPUT_ERROR')		 		{
		return {
			...state,
			inputError: action.error,
		};
	}
	if (action.type === 'PAYMENT_TYPE_FETCH_ERROR')		 		{
		return {
			...state,
			fetchError: action.error,
			fetching: false,
		};
	}
	return state;
}
