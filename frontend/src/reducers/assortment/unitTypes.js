import { booleanField, replaceField, reSetField } from "../tools/subReducers";
import { combineReducers } from "redux";

export default combineReducers({
	unitTypes: replaceField('UNIT_TYPE_FETCH_DONE', [], 'unitTypes'),
	fetching: booleanField({
		UNIT_TYPE_FETCH_START: true,
		UNIT_TYPE_FETCH_DONE: false,
		UNIT_TYPE_FETCH_ERROR: false,
	}, false),
	fetchError: reSetField('UNIT_TYPE_FETCH_ERROR', 'UNIT_TYPE_FETCH_DONE', null, 'error'),
	inputError: reSetField('UNIT_TYPE_INPUT_ERROR', 'UNIT_TYPE_FETCH_START', null, 'error'),
	populated: booleanField({ UNIT_TYPE_FETCH_DONE: true }, false),
});
