import { REGISTER_FETCH_DONE, REGISTER_FETCH_ERROR, REGISTER_FETCH_INPUT_ERROR, REGISTER_FETCH_START } from './actions';

const initialState = {
	registers: [],
	fetching: false,
	fetchError: null,
	inputError: null,
};

export default function registerReducer(state = initialState, action) {
	if (action.type === REGISTER_FETCH_START)		 		{
		return {
			...state,
			fetching: true,
			inputError: null,
		};
	}
	if (action.type === REGISTER_FETCH_DONE)		 		{
		return {
			...state,
			fetching: false,
			registers: action.registers,
			fetchError: null,
		};
	}
	if (action.type === REGISTER_FETCH_INPUT_ERROR)		 		{
		return {
			...state,
			inputError: action.error,
		};
	}
	if (action.type === REGISTER_FETCH_ERROR)		 		{
		return {
			...state,
			fetchError: action.error,
			fetching: false,
		};
	}
	return state;
}
