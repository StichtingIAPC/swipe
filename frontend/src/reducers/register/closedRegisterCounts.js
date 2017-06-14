import { combineReducers } from 'redux';
import { booleanField, replaceField, reSetField } from '../tools/subReducers';

export default combineReducers({
	closedRegisterCounts: replaceField('REGISTERCOUNT_FETCH_CLOSED_REGISTERCOUNTS_DONE', [], 'registerCounts'),
	fetching: booleanField({
		REGISTERCOUNT_FETCH_CLOSED_REGISTERCOUNTS: true,
		REGISTERCOUNT_FETCH_CLOSED_REGISTERCOUNTS_DONE: false,
		REGISTERCOUNT_CLOSED_REGISTER_FETCH_ERROR: false,
	}, false),
	fetchError: reSetField('REGISTERCOUNT_CLOSED_REGISTER_FETCH_ERROR', 'REGISTERCOUNT_FETCH_CLOSED_REGISTERCOUNTS_DONE', null, 'error'),
	inputError: reSetField('REGISTERCOUNT_CLOSED_REGISTER_INPUT_ERROR', 'REGISTERCOUNT_FETCH_CLOSED_REGISTERCOUNTS', null, 'error'),
	populated: booleanField({ REGISTERCOUNT_FETCH_CLOSED_REGISTERCOUNTS_DONE: true }, false),
});
