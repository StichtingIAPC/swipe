import { booleanField, replaceField, reSetField } from "../tools/subReducers";
import { combineReducers } from "redux";

export default combineReducers({
	labelTypes: replaceField('LABEL_TYPE_FETCH_DONE', [], 'labelTypes'),
	fetching: booleanField({
		LABEL_TYPE_FETCH_START: true,
		LABEL_TYPE_FETCH_DONE: false,
		LABEL_TYPE_FETCH_ERROR: false,
	}, false),
	fetchError: reSetField('LABEL_TYPE_FETCH_ERROR', 'LABEL_TYPE_FETCH_DONE', null, 'error'),
	inputError: reSetField('LABEL_TYPE_INPUT_ERROR', 'LABEL_TYPE_FETCH_START', null, 'error'),
	populated: booleanField({ LABEL_TYPE_FETCH_DONE: true }, false),
});
