import { combineReducers } from 'redux';
import {
	booleanControlReducer,
	collectReducers, objectControlReducer, resetFieldReducer,
	setFieldReducer,
} from '../../../tools/reducerComponents';

const defaultCurrency = {
	iso: '',
	name: '',
	digits: 2,
	symbol: '',
	denomination_set: [],
};

export default combineReducers({
	currencies: setFieldReducer([
		'money/currencies/FETCH_ALL_DONE',
	], [], 'currencies'),
	activeObject: collectReducers(
		resetFieldReducer([
			'money/currencies/NEW_CURRENCY',
		], defaultCurrency),
		objectControlReducer([
			'money/currencies/SET_FIELD',
		], defaultCurrency),
		setFieldReducer([
			'money/currencies/FETCH_DONE',
		], defaultCurrency, 'currency')
	),
	loading: booleanControlReducer({
		'money/currencies/FETCH_ALL': true,
		'money/currencies/FETCH_ALL_FINALLY': false,
	}, false),
	populated: booleanControlReducer({
		'money/currencies/FETCH_ALL_DONE': true,
	}, false),
	error: setFieldReducer([
		'money/currencies/FETCH_ALL_FAILED',
		'money/currencies/FETCH_FAILED',
		'money/currencies/CREATE_FAILED',
		'money/currencies/UPDATE_FAILED',
		'money/currencies/DELETE_FAILED',
	], null, 'reason'),
});
