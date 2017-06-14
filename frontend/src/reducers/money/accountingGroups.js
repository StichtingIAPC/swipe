import { combineReducers } from "redux";
import { booleanField, replaceField, reSetField } from "../tools/subReducers";

export default combineReducers({
	accountingGroups: replaceField('ACCOUNTING_GROUP_FETCH_DONE', [], 'accountingGroups'),
	fetching: booleanField({
		ACCOUNTING_GROUP_FETCH_START: true,
		ACCOUNTING_GROUP_FETCH_DONE: false,
		ACCOUNTING_GROUP_FETCH_ERROR: false,
	}, false),
	fetchError: reSetField('ACCOUNTING_GROUP_FETCH_ERROR', 'ACCOUNTING_GROUP_FETCH_DONE', null, 'error'),
	inputError: reSetField('ACCOUNTING_GROUP_INPUT_ERROR', 'ACCOUNTING_GROUP_FETCH_START', null, 'error'),
	populated: booleanField({ ACCOUNTING_GROUP_FETCH_DONE: true }, false),
});
