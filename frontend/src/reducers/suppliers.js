const initialState = {
	suppliers: [],
	fetching: false,
	fetchError: null,
	inputError: null,
};

export default function supplierReducer(state = initialState, action) {
	if (action.type === 'SUPPLIER_FETCH_START')
		return { ...state, fetching: true, inputError: null };
	if (action.type === 'SUPPLIER_FETCH_DONE')
		return { ...state, fetching: false, suppliers: action.suppliers, fetchError: null };
	if (action.type === 'SUPPLIER_INPUT_ERROR')
		return { ...state, inputError: action.error };
	if (action.type === 'SUPPLIER_FETCH_ERROR')
		return { ...state, fetchError: action.error, fetching: false };
	return state;
}
