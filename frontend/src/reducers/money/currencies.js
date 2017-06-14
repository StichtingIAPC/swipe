import { combineReducers } from 'redux';
import { booleanField, replaceField, reSetField } from '../tools/subReducers';

export default combineReducers({
	currencies: replaceField('CURRENCY_FETCH_DONE', [], 'currencies'),
	fetching: booleanField({
		CURRENCY_FETCH_START: true,
		CURRENCY_FETCH_DONE: false,
		CURRENCY_FETCH_ERROR: false,
	}, false),
	fetchError: reSetField('CURRENCY_FETCH_ERROR', 'CURRENCY_FETCH_DONE', null, 'error'),
	inputError: reSetField('CURRENCY_INPUT_ERROR', 'CURRENCY_FETCH_START', null, 'error'),
	populated: booleanField({ CURRENCY_FETCH_DONE: true }, false),
});
