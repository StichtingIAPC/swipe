import { combineReducers } from 'redux';
import { setFieldReducer, booleanControlReducer, collectReducers, resetFieldReducer } from '../../../tools/reducerComponents';

export default combineReducers({
	registers: setFieldReducer([
		'REGISTER_FETCH_DONE',
	], [], 'registers'),
	fetching: booleanControlReducer({
		REGISTER_FETCH_START: true,
		REGISTER_FETCH_DONE: false,
		REGISTER_FETCH_ERROR: false,
	}, false),
	fetchError: collectReducers(
		setFieldReducer([
			'REGISTER_FETCH_ERROR',
		], null, 'error'),
		resetFieldReducer([
			'REGISTER_FETCH_DONE',
		], null),
	),
	inputError: collectReducers(
		setFieldReducer([
			'REGISTER_INPUT_ERROR',
		], null, 'error'),
		resetFieldReducer([
			'REGISTER_FETCH_START',
		], null),
	),
	populated: booleanControlReducer({
		REGISTER_FETCH_DONE: true,
	}, false),
});
