import { STOCK_FETCH_DONE, STOCK_FETCH_FAILED, STOCK_FETCH_START } from './actions';
const initialState = {
	stock: [],
	fetching: false,
	fetchError: null,
	inputError: null,
};

export default function stockReducer(state = initialState, action) {
	if (action.type === STOCK_FETCH_START) {
		return {
			...state,
			fetching: true,
			inputError: null,
		};
	}
	if (action.type === STOCK_FETCH_DONE) {
		return {
			...state,
			fetching: false,
			stock: action.stock,
			fetchError: null,
		};
	}

	if (action.type === STOCK_FETCH_FAILED) {
		return {
			...state,
			fetchError: action.error,
			fetching: false,
		};
	}
	return state;
}
