import { combineReducers } from "redux";
import { booleanField, replaceField, reSetField } from "../tools/subReducers";

export default combineReducers({
	registers: replaceField('REGISTER_FETCH_DONE', [], 'registers'),
	fetching: booleanField({
		REGISTER_FETCH_START: true,
		REGISTER_FETCH_DONE: false,
		REGISTER_FETCH_ERROR: false,
	}, false),
	fetchError: reSetField('REGISTER_FETCH_ERROR', 'REGISTER_FETCH_DONE', null, 'error'),
	inputError: reSetField('REGISTER_INPUT_ERROR', 'REGISTER_FETCH_START', null, 'error'),
	populated: booleanField({ REGISTER_FETCH_DONE: true }, false),
});
