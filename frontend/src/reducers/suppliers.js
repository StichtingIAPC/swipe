const initialState = {
	suppliers: [],
	fetching: false,
};

export default function supplierReducer(state = initialState, action) {
	if (action.type === 'SUPPLIER_FETCH_START') return { ...state, fetching: true };
	if (action.type === 'SUPPLIER_FETCH_DONE') return { ...state, fetching: false, suppliers: action.suppliers };
	return state;
}
